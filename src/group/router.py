from typing import Annotated

from fastapi import APIRouter, status
from fastapi import Depends, HTTPException

from src.auth import models
from src.auth.router import get_current_user
from src.dependencies import get_db
from . import crud, schemas
from .utilities import get_days_as_list_from_group_model

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
    return schemas.GroupInf(name=db_group.name, price=db_group.price, coach_id=coach.id,
                            days=get_days_as_list_from_group_model(db_group))


@router.get("/inf/{group_name}", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK, response_model=schemas.GroupInf)
async def get_information_about_group(group_name: str, coach: Annotated[models.User, Depends(is_coach)]):
    db_group = crud.get_group_by_name(group_name=group_name)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no group with this name")
    return schemas.GroupInf(name=db_group.name, price=db_group.price, coach_id=coach.id,
                            days=get_days_as_list_from_group_model(db_group))


@router.get("/leads", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK, description="Returns the names of the groups led by coach",
            response_model=list[str])
async def get_available_groups(coach: Annotated[models.User, Depends(is_coach)]):
    return crud.get_names_of_groups_that_lead_by_coach(coach)
