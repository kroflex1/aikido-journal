from typing import Any

import peewee
from pydantic import BaseModel, Field
from pydantic.v1.utils import GetterDict
from src.auth import schemas as user_schemas
from src.child import schemas as child_schemas
from src.group import schemas as group_schemas


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class Parent(user_schemas.User):
    children: list[child_schemas.Child] | None


class ChildGroupInf(BaseModel):
    group_name: str = Field(examples=["HF-101"])
    group_price: int = Field(examples=[250])
    coach_name: str | None
    coach_surname: str | None
    coach_patronymic: str | None
    coach_phone_number: str | None
    schedule: list[group_schemas.Time | None] = Field(min_items=7, max_items=7)


class ChildSchedule(BaseModel):
    name: str = Field(examples=["Valera"])
    surname: str = Field(examples=["Tereshkov"])
    patronymic: str | None = Field(examples=["Maximovich"])
    group_inf: ChildGroupInf | None


class ChildAttendance(BaseModel):
    name: str = Field(examples=["Valera"])
    surname: str = Field(examples=["Tereshkov"])
    patronymic: str | None = Field(examples=["Maximovich"])
    attendance: group_schemas.ChildVisitInf | None
    schedule: list[group_schemas.DayInf] | None 
