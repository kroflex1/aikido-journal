from enum import Enum
from typing import Any

import peewee
from pydantic import BaseModel, Field, ConfigDict
from pydantic.v1.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class ChildCreate(BaseModel):
    name: str = Field(examples=["Valera"])
    surname: str = Field(examples=["Tereshkov"])
    patronymic: str | None = Field(examples=["Maximovich"])


class Child(ChildCreate):
    id: int
    parent_id: int | None = Field(default=None)
    group_name_id: str | None = Field(default=None)

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
