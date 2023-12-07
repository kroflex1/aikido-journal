from . import schemas, models


def create_child(child: schemas.ChildCreate) -> models.Child:
    db_child = models.Child(name=child.name, surname=child.surname, patronymic=child.patronymic)
    db_child.save(force_insert=True)
    return db_child


def get_all_children() -> list[models.Child]:
    return [child for child in models.Child.select()]


def get_children_at_group(group_name: str) -> list[models.Child]:
    return [child for child in models.Child.select().where(models.Child.group_name== group_name)]


def get_children_without_parent() -> list[models.Child]:
    return [child for child in models.Child.select().where(models.Child.parent == None)]

def get_children_without_group() -> list[models.Child]:
    return [child for child in models.Child.select().where(models.Child.group_name == None)]


def remove_child(id: int):
    db_child = get_child_by_id(id)
    db_child.delete_instance()


def get_child_by_name(name: str, surname: str, patronymic: str) -> models.Child | None:
    if patronymic is None:
        child_db = models.Child.get_or_none((models.Child.name == name) & (models.Child.surname == surname))
    else:
        child_db = models.Child.get_or_none(
            (models.Child.name == name) & (models.Child.surname == surname) & (models.Child.patronymic == patronymic))
    return child_db


def get_child_by_id(id: int) -> models.Child | None:
    child_db = models.Child.get_or_none(models.Child.id == id)
    return child_db
