from passlib.context import CryptContext

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(user_id: int) -> models.User:
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_phone_number(phone_number: str) -> models.User:
    return models.User.filter(models.User.phone_number == phone_number).first()


def get_user_by_phone_number_and_password(phone_number: str, password: str) -> models.User:
    db_user: models.User = get_user_by_phone_number(phone_number)
    if db_user is not None and pwd_context.verify(password, db_user.hashed_password):
        return db_user
    else:
        raise ValueError("Invalid phone number or password")


def create_user(user: schemas.UserCreate) -> models.User:
    fake_hashed_password = pwd_context.hash(user.password)
    db_user = models.User(phone_number=user.phone_number, name=user.phone_number, surname=user.surname,
                          patronymic=user.patronymic, role=user.role, hashed_password=fake_hashed_password)

    db_user.save()
    return db_user
