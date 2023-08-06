import asyncio
import aiohttp

from abc import ABC, abstractmethod
from xml.etree import ElementTree
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from .models import Item, FailedItem, DbItem
from .exceptions import ItemObtainingFailed
from .db import Engine
from .config import settings


class BaseGetter(ABC):
    _default_error_msg = "Failed to get item info:"

    @abstractmethod
    def get(self, item_id: int) -> Item:
        pass


class PublicDbGetter(BaseGetter):
    """Interface to get item info from public DB"""
    # TODO: add logging
    public_db_url = settings.public_db_url

    def __init__(self, public_db_url: str = None):
        if public_db_url:
            self.public_db_url = public_db_url

    async def get(self, *args: int, many: bool = False, save_to_db: bool = False, raise_exceptions: bool = True)-> Item:
        """
        :param args: list of integers with items ids
        :param many: set to true if you want to process multiple items at once
        :param save_to_db: set to true if you want to save item to local db
        :param raise_exceptions: if set to False returns instance of FailedItem instead of raising an exception
        :return: Item
        """
        item_obj = None
        if many:
            return await asyncio.gather(*[self.get(i, save_to_db=save_to_db, raise_exceptions=raise_exceptions) for i in args])

        if len(args) > 1 and not many:
            raise ValueError("set 'many=True' if you need to process more than 1 item!")

        item_id = args[0]
        _request_payload = {
            'item': args[0],
            'xml': 'yesplease'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.public_db_url, params=_request_payload) as resp:
                public_db_response = await resp.text()
                response_status = resp.status

        if not response_status == 200:
            if raise_exceptions:
                raise ItemObtainingFailed(f"{self._default_error_msg} incorrect response from public db")
            item_obj = FailedItem(id=item_id)

        item_obj = item_obj or self._get_item_from_xml(item_id, public_db_response, raise_exceptions=raise_exceptions)

        if save_to_db:
            await self._save_to_db(item_obj)

        return item_obj

    def _get_item_from_xml(self, item_id: int, raw_xml_string: str, raise_exceptions: bool = True) -> Item:
        item_obj = None
        root_xml_node = ElementTree.fromstring(raw_xml_string)

        item_xml_node = root_xml_node.find('item')
        if not item_xml_node:
            if raise_exceptions:
                raise ItemObtainingFailed(f"{self._default_error_msg} {root_xml_node.find('error').text}")
            item_obj = FailedItem(id=item_id)

        if not item_obj:
            rarity_id = item_xml_node.find('quality').attrib['id']
            item_level = item_xml_node.find('level').text
            item_slot = item_xml_node.find('inventorySlot').attrib['id']
            item_name = item_xml_node.find('name').text
            try:
                item_obj = Item(
                    rarity=rarity_id,
                    level=item_level,
                    slot=item_slot,
                    id=item_id,
                    name=item_name
                )
            except ValidationError:
                if raise_exceptions:
                    raise ItemObtainingFailed(f"{self._default_error_msg} unserializable item")
                item_obj = FailedItem(id=item_id)
        return item_obj

    async def _save_to_db(self, item: Item):
        if isinstance(item, FailedItem):
            return

        async_session = sessionmaker(
            Engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as db_session:
            item_in_db = await db_session.execute(select(DbItem).filter(DbItem.id == item.id))
            if not item_in_db.scalars().all():
                db_item = DbItem(**item.__dict__)
                db_session.add(db_item)
                await db_session.commit()


class LocalDbGetter(BaseGetter):
    """Interface to get item from local db"""
    async def get(self, *args: int, many: bool = False, raise_exceptions: bool = True) -> Item:
        """
        :param args: list of integers with items ids
        :param many: set to true if you want to process multiple items at once
        :param raise_exceptions: if set to False returns instance of FailedItem instead of raising an exception
        :return:
        """
        item_obj = None

        if many:
            return await asyncio.gather(*[self.get(i, raise_exceptions=raise_exceptions) for i in args])

        if len(args) > 1 and not many:
            raise ValueError("set 'many=True' if you need to process more than 1 item!")

        item_id = args[0]
        async_session = sessionmaker(
            Engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as db_session:
            query_result = await db_session.execute(select(DbItem).filter(DbItem.id == item_id))
            db_item = query_result.scalars().first()
            if not db_item:
                if raise_exceptions:
                    raise ItemObtainingFailed(f"{self._default_error_msg} item is not present in local DB")
                item_obj = FailedItem(id=item_id)

        item_obj = item_obj or Item(**db_item.__dict__)
        return item_obj
