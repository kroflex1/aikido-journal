from typing import Annotated

from fastapi import APIRouter, status
from fastapi import Depends, HTTPException

from src.auth import models
from src.auth.router import get_current_user
from src.dependencies import get_db
from . import crud, schemas

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
             status_code=status.HTTP_201_CREATED, response_model=schemas.Group)
async def create_group(group: schemas.GroupCreate):
    db_group = crud.get_group_by_name(group_name=group.name)
    if db_group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Group with this name has already been created")
    db_group = crud.create_group(group_create=group, coach_id=1)
    return db_group
