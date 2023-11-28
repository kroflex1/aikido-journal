import peewee

from src.auth import models
from src.group import models as group_models
from src.database import db


class Child(peewee.Model):
    parent = peewee.ForeignKeyField(models.User, null=True, index=True, backref="children")
    group_name = peewee.ForeignKeyField(group_models.Group, null=True, index=True, backref="children",
                                        column_name="group_name")
    name = peewee.CharField()
    surname = peewee.CharField()
    patronymic = peewee.CharField()

    class Meta:
        database = db
        constraints = [peewee.SQL('UNIQUE (name, surname, patronymic)')]
