from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from src.auth import models as user_models
from src.dependencies import get_db
from src.group.router import is_coach
from . import schemas, crud

router = APIRouter(
    prefix="/children",
    tags=["Child"])


def get_child_by_id(child_id: int):
    db_child = crud.get_child_by_id(child_id)
    if db_child is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is no child with this id")
    return db_child


@router.post("/create", dependencies=[Depends(get_db)],
             status_code=status.HTTP_201_CREATED, response_model=schemas.Child)
async def create_child(child: schemas.ChildCreate, coach: Annotated[user_models.User, Depends(is_coach)]):
    db_child = crud.get_child_by_name(name=child.name, surname=child.surname, patronymic=child.patronymic)
    if db_child:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Child with given name, surname and patronymic already exists")
    db_child = crud.create_child(child)
    return db_child


@router.post("/remove/{child_id}", dependencies=[Depends(get_db)],
             status_code=status.HTTP_200_OK)
async def delete_child(child_id: int, coach: Annotated[user_models.User, Depends(is_coach)]):
    get_child_by_id(child_id=child_id)
    crud.remove_child(child_id)
    return "Child successfully deleted"


@router.get("/get/{child_id}", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK, response_model=schemas.Child)
async def get_child(child_id: int, coach: Annotated[user_models.User, Depends(is_coach)]):
    return get_child_by_id(child_id=child_id)


@router.get("/all", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK, response_model=list[schemas.Child])
async def get_all_children(coach: Annotated[user_models.User, Depends(is_coach)]):
    return crud.get_all_children()

@router.get("/children_without_parent", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK, response_model=list[schemas.Child])
async def get_children_without_parent(coach: Annotated[user_models.User, Depends(is_coach)]):
    return crud.get_children_without_parent()
