from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from src.auth import crud as user_crud
from src.auth import models as user_models
from src.child import crud as child_crud
from src.dependencies import get_db
from src.group.router import is_coach
from . import crud, schemas

router = APIRouter(
    prefix="/parents",
    tags=["Parent"])


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


@router.get("/all", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK, response_model=list[schemas.Parent])
async def get_all_parents(coach: Annotated[user_models.User, Depends(is_coach)]):
    return crud.get_all_parents()
