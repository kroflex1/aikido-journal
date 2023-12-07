from typing import Annotated

from fastapi import APIRouter, status
from fastapi import Depends, HTTPException

from src.auth import models
from src.auth.router import get_current_user
from src.dependencies import get_db
from src.child import crud as child_crud
from . import crud, schemas
from .utilities import get_days_as_list_from_group_model, convert_group_model_to_schema

router = APIRouter(
    prefix="/groups",
    tags=["Group"])


async def is_coach(current_user: Annotated[models.User, Depends(get_current_user)]) -> models.User:
    lack_of_access_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Only coach can execute this request",
    )
    if current_user.role == 'coach':
        return current_user
    raise lack_of_access_exception


@router.post("/create", dependencies=[Depends(get_db)],
             status_code=status.HTTP_201_CREATED, response_model=schemas.GroupInf)
async def create_group(group: schemas.GroupCreate, coach: Annotated[models.User, Depends(is_coach)]):
    db_group = crud.get_group_by_name(group_name=group.name)
    if db_group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Group with this name has already been created")
    db_group = crud.create_group(group_create=group, coach_id=coach.id)
    return convert_group_model_to_schema(db_group)


@router.get("/get/{group_name}", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK, response_model=schemas.GroupInf)
async def get_information_about_group(group_name: str, coach: Annotated[models.User, Depends(is_coach)]):
    db_group = crud.get_group_by_name(group_name=group_name)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no group with this name")
    return schemas.GroupInf(name=db_group.name, price=db_group.price, coach_id=coach.id,
                            days=get_days_as_list_from_group_model(db_group))


@router.get("/remove/{group_name}", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK)
async def remove_group(group_name: str, strcoach: Annotated[models.User, Depends(is_coach)]):
    crud.remove_group(group_name)
    return "Group has been successfully remove"


@router.get("/{group_name}/add_child/{child_id}", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK)
async def add_child_to_group(group_name: str, child_id: int, coach: Annotated[models.User, Depends(is_coach)]):
    db_group = crud.get_group_by_name(group_name=group_name)
    db_child = child_crud.get_child_by_id(child_id)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no group with this name")
    if db_child is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no child with this id")
    if db_child.group_name is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This child is already in the group '{db_child.group_name.name}'")
    db_child.group_name = db_group
    db_child.save()
    return "Child has been successfully added to the group"


@router.get("/{group_name}/remove_child/{child_id}", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK)
async def remove_child_from_group(group_name: str, child_id: int, coach: Annotated[models.User, Depends(is_coach)]):
    db_group = crud.get_group_by_name(group_name=group_name)
    db_child = child_crud.get_child_by_id(child_id)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no group with this name")
    if db_child is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no child with this id")
    if db_child.group_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This child does not belong to any group")
    if db_child.group_name.name != db_group.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This child is in another group '{db_child.group_name.name}'")
    db_child.group_name = None
    db_child.save()
    return "Child has been successfully remove from group"


@router.get("/leads", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK, description="Returns the names of the groups led by coach",
            response_model=list[schemas.GroupInf])
async def get_groups_that_led_by_coach(coach: Annotated[models.User, Depends(is_coach)]):
    result = []
    for db_group in crud.get_groups_that_led_by_coach(coach):
        result.append(convert_group_model_to_schema(db_group))
    return result
