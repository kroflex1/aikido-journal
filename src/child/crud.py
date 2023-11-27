from . import schemas, models


def create_child(child: schemas.ChildCreate) -> models.Child:
    db_child = models.Child(name=child.name, surname=child.surname, patronymic=child.patronymic)
    db_child.save(force_insert=True)
    return db_child


def get_all_children() -> list[models.Child]:
    return [child for child in models.Child.select()]


def remove_child(id: int):
    db_child = get_child_by_id(id)
    db_child.delete_instance()


def get_child_by_name(name: str, surname: str, patronymic: str) -> models.Child | None:
    if patronymic is None:
        child_db = models.Child.get_or_none(models.Child.name == name and models.Child.surname == surname)
    else:
        child_db = models.Child.get_or_none(
            models.Child.name == name and models.Child.surname == surname and models.Child.patronymic == patronymic)
    return child_db


def get_child_by_id(id: int) -> models.Child | None:
    child_db = models.Child.get_or_none(models.Child.id == id)
    return child_db
