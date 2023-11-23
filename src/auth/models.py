import uuid

import peewee

from src.database import db


class User(peewee.Model):
    phone_number = peewee.CharField(unique=True, null=True, index=True)
    hashed_password = peewee.CharField(index=True)
    role = peewee.CharField()
    name = peewee.CharField(index=True)
    surname = peewee.CharField()
    patronymic = peewee.CharField(null=True)

    class Meta:
        database = db
