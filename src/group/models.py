import uuid

import peewee

from src.auth import models
from src.database import db


class Group(peewee.Model):
    name = peewee.CharField(primary_key=True, index=True)
    coach = peewee.ForeignKeyField(models.User, backref="groups")
    price = peewee.IntegerField()
    monday_start = peewee.TimeField(null=True)
    monday_end = peewee.TimeField(null=True)
    tuesday_start = peewee.TimeField(null=True)
    tuesday_end = peewee.TimeField(null=True)
    wednesday_start = peewee.TimeField(null=True)
    wednesday_end = peewee.TimeField(null=True)
    thursday_start = peewee.TimeField(null=True)
    thursday_end = peewee.TimeField(null=True)
    friday_start = peewee.TimeField(null=True)
    friday_end = peewee.TimeField(null=True)
    saturday_start = peewee.TimeField(null=True)
    saturday_end = peewee.TimeField(null=True)
    sunday_start = peewee.TimeField(null=True)
    sunday_end = peewee.TimeField(null=True)

    class Meta:
        database = db
