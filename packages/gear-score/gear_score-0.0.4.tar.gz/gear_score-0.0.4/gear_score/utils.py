from typing import List

from gear_score.models import Item
from gear_score.getters import LocalDbGetter, PublicDbGetter


async def get_items_from_local_or_remote(*args: int) -> List[Item]:
    """
    :param args: list of items ids to be queried
    :return:
    """
    items = []
    failed_items = []

    # ROUND 1: look in local DB
    local_getter = LocalDbGetter()
    local_results = await local_getter.get(*args, many=True, raise_exceptions=False)
    for result in local_results:
        if isinstance(result, Item):
            items.append(result)
        else:
            failed_items.append(result)

    if failed_items:
        remote_getter = PublicDbGetter()
        remote_results = await remote_getter.get(
            *[i.id for i in failed_items],
            many=True,
            raise_exceptions=False,
            save_to_db=True
        )
        items += remote_results

    return items


def count_gs(*args: Item) -> int:
    _gs = 0
    for item in args:
        _gs += int(item.gs)

    return _gs
