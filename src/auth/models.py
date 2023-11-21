import peewee

from src.database import db


class User(peewee.Model):
    phone_number = peewee.CharField(unique=True, null=True, index=True)
    name = peewee.CharField()
    surname = peewee.CharField
    patronymic = peewee.CharField(null=True)
    role = peewee.CharField
    hashed_password = peewee.CharField()

    class Meta:
        database = db
