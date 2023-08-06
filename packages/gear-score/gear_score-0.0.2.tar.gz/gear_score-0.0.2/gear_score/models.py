from pydantic import BaseModel
from typing import Optional

from sqlalchemy import Column, Integer, String

from gear_score import coefficients
from gear_score.enums import RarityEnum, SlotEnum
from gear_score.db import Base as SqliteBase


class Item(BaseModel):
    """Simple representation of an item"""

    level: int
    id: int
    name: str
    rarity: RarityEnum
    slot: SlotEnum
    gs: Optional[int]

    def __init__(self, **kwargs):
        """Custom init is needed as pydantic doesn't adequately work
        with native python getters & setters"""
        super().__init__(**kwargs)

        gs = kwargs.get("gs") or self._count_gs()
        setattr(self, "gs", gs)

    def _count_gs(self):
        gear_score = (
            (self._level - self._gs_scale[self._rarity]["subtrahend"])
            / self._gs_scale[self._rarity]["divisor"]
            * self._quality_coefficient
            * self._slot_coefficient
        )
        if gear_score < 0:
            gear_score = 0
        return gear_score

    @property
    def _quality_coefficient(self) -> float:
        """Quality coefficient differs depending on item rarity"""
        _scale_modifier = 1
        _constant_scale = 1.8618
        if self.rarity == RarityEnum.legendary:
            _scale_modifier = 1.3
        elif self.rarity in (RarityEnum.poor, RarityEnum.common):
            _scale_modifier = 0.005

        return _scale_modifier * _constant_scale

    @property
    def _slot_coefficient(self) -> float:
        """Different coefficient for each slot"""
        return coefficients.SLOT_COEFFICIENTS[self.slot]

    @property
    def _rarity(self) -> RarityEnum:
        """GS formulae uses mutated item rarity"""
        _formulae_rarity_mapping = {
            RarityEnum.poor: RarityEnum.uncommon,
            RarityEnum.common: RarityEnum.uncommon,
            RarityEnum.legendary: RarityEnum.epic,
            RarityEnum.heirloom: RarityEnum.rare,
        }
        return _formulae_rarity_mapping.get(self.rarity, self.rarity)

    @property
    def _level(self) -> float:
        """All heirloom items have fixed item level"""
        _level = self.level
        if self.rarity == RarityEnum.heirloom:
            _level = 187.05
        return _level

    @property
    def _gs_scale(self) -> dict:
        _gs_scale = coefficients.GS_COEFFICIENTS["LOW_LEVEL"]
        if self._level > 120:
            _gs_scale = coefficients.GS_COEFFICIENTS["HIGH_LEVEL"]

        return _gs_scale

    class Config:
        orm_mode = True


class FailedItem(BaseModel):
    """Returned by getters for items that were not found by
    PublicDbGetter and LocalDbGetter if raise_exceptions=False"""
    id: int

    @property
    def gs(self) -> float:
        return 0.0


class DbItem(SqliteBase):
    __tablename__ = "item"
    """SqlAlchemy representation of an item"""
    id = Column(Integer, primary_key=True)
    name = Column(String)
    level = Column(Integer)
    rarity = Column(Integer)
    slot = Column(Integer)
    gs = Column(Integer)
