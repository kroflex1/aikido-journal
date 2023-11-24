from typing import Annotated

from fastapi import APIRouter, status
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.dependencies import get_db
from . import crud, schemas, models
from .utilities import TokenManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
router = APIRouter(
    prefix="/users",
    tags=["User"])


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    TokenManager.check_token(token)
    user_id: int = TokenManager.get_user_id_from_token(token)
    user = crud.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user


@router.post("/register", dependencies=[Depends(get_db)],
             status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
async def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_phone_number(phone_number=user.phone_number)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already registered")
    db_user = crud.create_user(user=user)
    return schemas.Token(access_token=TokenManager.create_token(db_user.id, db_user.role), token_type="bearer")


@router.post("/login", dependencies=[Depends(get_db)], response_model=schemas.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db_user = crud.get_user_by_phone_number_and_password(phone_number=form_data.username, password=form_data.password)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid phone number or password")
    return schemas.Token(access_token=TokenManager.create_token(db_user.id, db_user.role), token_type="bearer")


@router.get("/me", response_model=schemas.User, dependencies=[Depends(get_db)])
async def get_inf_about_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user
