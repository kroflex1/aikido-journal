from typing import Any

import peewee
from pydantic.v1.utils import GetterDict
from src.auth import schemas as user_schemas
from src.child import schemas as child_schemas

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res




