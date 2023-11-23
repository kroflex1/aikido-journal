from contextvars import ContextVar
from config import DB_HOST, DB_PORT, DB_PASS, DB_USER, DB_NAME

import peewee

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = peewee.PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASS,
                               host=DB_HOST, port=DB_PORT)

db._state = PeeweeConnectionState()
