from enum import Enum
from typing import Any

import peewee
from pydantic import BaseModel
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


class UserBase(BaseModel):
    phone_number: str
    name: str
    surname: str
    patronymic: str | None = None
    role: Role


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
