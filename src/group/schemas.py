from datetime import datetime
from typing import Any

import peewee
from pydantic import BaseModel, Field
from pydantic.v1.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class Time(BaseModel):
    start: datetime
    end: datetime


class GroupCreate(BaseModel):
    name: str = Field(examples=["АТ-01"])
    price: int = Field(examples=[250])
    days: list[Time | None] = Field(min_items=7, max_items=7)


class Group(GroupCreate):
    coach_id: int
