from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    coach = 'coach'
    parent = 'parent'
    student = 'student'


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