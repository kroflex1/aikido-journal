from enum import Enum
from typing import Any

import peewee
from pydantic import BaseModel, Field
from pydantic.v1.utils import GetterDict


class Role(str, Enum):
    coach = 'coach'
    parent = 'parent'


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class Token(BaseModel):
    access_token: str = Field(example="eyJhbGciOiJIU.eyJleHAiOiIxMjM0NTY3.-Wp-D4EWy79DFM", alias="accessToken")
    token_type: str = Field(example="bearer", alias="tokenType")


class UserBase(BaseModel):
    phone_number: str = Field("+79127564382", alias="phoneNumber")
    name: str = Field("Vova")
    surname: str = Field("Bersov")
    patronymic: str | None = Field(default=None, examples=["Alexanrov"])
    role: Role

    class Config:
        use_enum_values = True


class UserCreate(UserBase):
    password: str = Field("somepassword")


class UserIn(BaseModel):
    phone_number: str = Field("+79127564382", alias="phoneNumber")
    password: str = Field("somepassword")


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
