import peewee

from src.auth import models
from src.database import db


class Group(peewee.Model):
    name = peewee.CharField(primary_key=True, index=True)
    coach = peewee.ForeignKeyField(models.User, backref="groups")
    price = peewee.IntegerField()
    monday_start = peewee.DateTimeField(null=True)
    monday_end = peewee.DateTimeField(null=True)
    tuesday_start = peewee.DateTimeField(null=True)
    tuesday_end = peewee.DateTimeField(null=True)
    wednesday_start = peewee.DateTimeField(null=True)
    wednesday_end = peewee.DateTimeField(null=True)
    thursday_start = peewee.DateTimeField(null=True)
    thursday_end = peewee.DateTimeField(null=True)
    friday_start = peewee.DateTimeField(null=True)
    friday_end = peewee.DateTimeField(null=True)
    saturday_start = peewee.DateTimeField(null=True)
    saturday_end = peewee.DateTimeField(null=True)
    sunday_start = peewee.DateTimeField(null=True)
    sunday_end = peewee.DateTimeField(null=True)

    class Meta:
        database = db


