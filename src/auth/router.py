from fastapi import APIRouter
from fastapi import Depends, HTTPException

from . import crud, schemas
from .dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["User"])


@router.post("/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, dependencies=[Depends(get_db)]):
    db_user = crud.get_user_by_phone_number(phone_number=user.phone_number)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return crud.create_user(user=user)


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, dependencies=[Depends(get_db)]):
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
