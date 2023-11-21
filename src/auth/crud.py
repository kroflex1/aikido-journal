from . import models, schemas


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_phone_number(phone_number: str):
    return models.User.filter(models.User.phone_number == phone_number).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_user(user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(phone_number=user.phone_number, name=user.phone_number, surname=user.surname,
                          patronymic=user.patronymic, role=user.role, hashed_password=fake_hashed_password)
    db_user.save()
    return db_user
