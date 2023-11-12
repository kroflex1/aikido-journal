from datetime import datetime, time
from enum import Enum
from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class UserBase(BaseModel):
    id: UUID
    name: str = Field(examples=["Игорь"])
    surname: str = Field(examples=["Медный"])
    patronymic: str | None = Field(default=None, examples=["Сергеевич"])
    phone_number: str = Field(examples=["+79562454324"])


class UserIn(BaseModel):
    phone_number: str = Field(examples=["+79562454324"])
    password: str = Field(examples=["somePassword"])


class Parent(UserBase):
    debt: int


class ChildCreate(BaseModel):
    name: str
    surname: str
    patronymic: str | None
    parent_id: UUID


class Child(BaseModel):
    name: str
    surname: str
    patronymic: str | None
    parent: Parent
    group_name: str | None


class Group(BaseModel):
    name: str
    coach: UserBase
    monday: time | None
    tuesday: time | None
    wednesday: time | None
    thursday: time | None
    friday: time | None
    saturday: time | None
    sunday: time | None
    children: list[Child]


class VisitInformation(BaseModel):
    group_name: str
    child_name: str
    child_surname: str
    child_patronymic: str | None
    day: datetime.date


@app.post("/register/", response_model=UserBase, tags=["user"], status_code=status.HTTP_201_CREATED)
async def register(user: UserBase):
    return user


@app.post("/login/", response_model=UserBase, tags=["user"], status_code=status.HTTP_202_ACCEPTED)
async def login(user: UserIn):
    return user


@app.post("/register/group", response_model=Group, tags=["group"], status_code=status.HTTP_201_CREATED)
async def register_new_group(group: Group):
    return


@app.post("/group/{group_name}/add-child", tags=["group"], status_code=status.HTTP_200_OK)
async def add_child_to_group(group_name: str):
    return


@app.get("/group/{group_name}", response_model=Group, tags=["group"], status_code=status.HTTP_200_OK)
async def get_group_information(group_name: str):
    return


@app.get("/group/mark-visit", tags=["group"], status_code=status.HTTP_200_OK)
async def mark_child_visit(group_name: str, visit_information: VisitInformation):
    return


@app.get("/group/{group_name}/mark-child-visit", tags=["group"], status_code=status.HTTP_200_OK)
async def mark_child_visit(visit_information: VisitInformation):
    return


@app.post("/register/child", response_model=Child, tags=["children"], status_code=status.HTTP_201_CREATED)
async def register_new_child(child_information: ChildCreate):
    return child_information
