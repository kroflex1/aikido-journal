from typing import Annotated

from fastapi import APIRouter, status, Header, Form
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from . import crud, schemas, models
from src.dependencies import get_db
from .utilities import TokenManager

router = APIRouter(
    prefix="/users",
    tags=["User"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_by_token(token: str = Header(alias='user-auth-token'), dependencies=[Depends(get_db)]) -> models.User:
    user_id: int = TokenManager.get_user_id_from_token(token)
    return crud.get_user_by_id(user_id)


@router.post("/create", response_model=schemas.Token, dependencies=[Depends(get_db)],
             status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_phone_number(phone_number=user.phone_number)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already registered")
    db_user = crud.create_user(user=user)
    return schemas.Token(token=TokenManager.create_token(db_user.id, db_user.role))


@router.post("/login", response_model=schemas.Token, dependencies=[Depends(get_db)])
def login(phone_number: Annotated[str, Form()], password: Annotated[str, Form()]):
    db_user = crud.get_user_by_phone_number_and_password(phone_number=phone_number, password=password)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid phone number or password")
    return schemas.Token(token=TokenManager.create_token(db_user.id, db_user.role))

# @router.get("/me", response_model=schemas.User)
# def get_information_about_me(token: str = Header(alias='user-auth-token'), dependencies=[Depends(get_db)]):
#     return
