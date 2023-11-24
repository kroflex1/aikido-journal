from datetime import datetime
from enum import Enum
from typing import Any

import peewee
from pydantic import BaseModel, Field
from pydantic.v1.utils import GetterDict


class Role(str, Enum):
    coach = 'coach'
    parent = 'parent'
    student = 'student'


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
    name: str
    price: int
    days: list[Time | None]


class Group(GroupCreate):
    coach_id: int
