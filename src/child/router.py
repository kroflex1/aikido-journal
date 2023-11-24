from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from . import schemas, models, crud

from src.dependencies import get_db

router = APIRouter(
    prefix="/childs",
    tags=["Child"])


@router.post("/create", dependencies=[Depends(get_db)],
             status_code=status.HTTP_201_CREATED, response_model=schemas.Child)
async def create_group(child: schemas.ChildCreate):
    db_child = crud.get_child_by_name(name=child.name, surname=child.surname, patronymic=child.patronymic)
    if db_child:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Child with given name, surname and patronymic already exists")
    db_child = crud.create_child(child)
    return db_child
