from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from src.auth import crud as user_crud
from src.auth import models as user_models
from src.auth.router import get_current_user
from src.child import crud as child_crud
from src.dependencies import get_db
from src.group import crud as group_crud
from src.group import utilities as group_utilities
from src.group.router import is_coach
from . import crud, schemas

router = APIRouter(
    prefix="/parents",
    tags=["Parent"])


async def is_parent(current_user: Annotated[user_models.User, Depends(get_current_user)]) -> user_models.User:
    lack_of_access_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Only parent can execute this request",
    )
    if current_user.role == 'parent':
        return current_user
    raise lack_of_access_exception


async def is_parent_or_coach(current_user: Annotated[user_models.User, Depends(get_current_user)]) -> user_models.User:
    lack_of_access_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Only parent or coach can execute this request",
    )
    if current_user.role == 'parent' or current_user.role == 'coach':
        return current_user
    raise lack_of_access_exception


@router.get("/{parent_id}/add_child/{child_id}", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK, response_model=schemas.Parent)
async def add_child_to_parent(parent_id: int, child_id: int, coach: Annotated[user_models.User, Depends(is_coach)]):
    db_parent = user_crud.get_user_by_id(parent_id)
    db_child = child_crud.get_child_by_id(child_id)
    if db_parent is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no parent with this id")
    if db_child is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no child with this id")
    if db_parent.role != "parent":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Child can only be added to a user with the 'parent' role")
    if db_child.parent is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Child already has a parent")
    db_child.parent = db_parent
    db_child.save()
    return db_parent


@router.get("/{parent_id}/remove_child/{child_id}", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK)
async def add_child_to_parent(parent_id: int, child_id: int, coach: Annotated[user_models.User, Depends(is_coach)]):
    db_parent = user_crud.get_user_by_id(parent_id)
    db_child = child_crud.get_child_by_id(child_id)
    if db_parent is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no parent with this id")
    if db_child is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no child with this id")
    if db_parent.role != "parent":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Child can only be added to a user with the 'parent' role")
    if db_child.parent is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This child does not have a parent")
    if db_child.parent.id != db_parent.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This child has a different parent by id {db_child.parent.id}")
    db_child.parent = None
    db_child.save()
    return "Child has been successfully remove from parent"


@router.get("/get_children_schedule", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK)
async def get_children_schedule(parent: Annotated[user_models.User, Depends(is_parent)]):
    db_parent = user_crud.get_user_by_id(parent)
    if db_parent is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no parent with this id")
    result = []
    db_children = crud.get_children(parent.id)
    for db_child in db_children:
        group_schema = None
        if db_child.group_name_id is not None:
            group_schema = schemas.ChildGroupInf()
            db_group = group_crud.get_group_by_name(db_child.group_name_id)
            coach = db_group.coach

            group_schema.group_name = db_group.name
            group_schema.group_price = db_group.price
            group_schema.coach_name = coach.name
            group_schema.coach_surname = coach.surname
            group_schema.coach_patronymic = coach.patronymic
            group_schema.coach_phone_number = coach.phone_number
            group_schema.schedule = group_utilities.get_days_as_list_from_group_model(db_group)

        result.append(
            schemas.ChildSchedule(name=db_child.name, surname=db_child.surname, patronymic=db_child.patronymic,
                                  group_inf=group_schema))
    return result


@router.get("/all", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK, response_model=list[schemas.Parent])
async def get_all_parents(coach: Annotated[user_models.User, Depends(is_coach)]):
    return crud.get_all_parents()
