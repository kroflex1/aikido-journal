from http.client import HTTPException
from fastapi import status
from src.auth import crud as user_crud
from src.child import crud as child_crud
from src.auth import models as user_models
from src.child import models as child_models


def add_child_to_parent(parent_id: int, child_id: int) -> user_models.User:
    db_parent = user_crud.get_user_by_id(parent_id)
    db_child = child_crud.get_child_by_id(child_id)
    if db_parent is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no parent with this id")
    if db_child is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no child with this id")
    if db_parent.role != "parent":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Child can only be added to a user with the 'parent' role")
    db_child.parent = db_parent
    db_child.save()
    return db_parent


def get_children(parent_id: int) -> list[child_models.Child]:
    db_parent = user_crud.get_user_by_id(parent_id)
    db_children = list(db_parent.children)
    return db_children


def get_all_parents() -> list[user_models.User]:
    return [parent for parent in user_models.User.select().where(user_models.User.role == "parent")]
