from fastapi import HTTPException, status

from . import schemas, models
from datetime import datetime, date


def create_child(child: schemas.ChildCreate) -> models.Child:
    db_child = models.Child(name=child.name, surname=child.surname, patronymic=child.patronymic)
    db_child.save(force_insert=True)
    return db_child


def get_all_children() -> list[models.Child]:
    return [child for child in models.Child.select()]


def get_children_at_group(group_name: str) -> list[models.Child]:
    return [child for child in models.Child.select().where(models.Child.group_name == group_name)]


def get_children_without_parent() -> list[models.Child]:
    return [child for child in models.Child.select().where(models.Child.parent == None)]


def get_children_without_group() -> list[models.Child]:
    return [child for child in models.Child.select().where(models.Child.group_name == None)]


def remove_child(id: int):
    db_child = get_child_by_id(id)
    qry = models.ChildAttendance.delete().where(models.ChildAttendance.child_id == db_child.id)
    qry.execute()
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


def mark_visit(child_id: int, date_visit: date, price: int) -> models.ChildAttendance:
    child_db = get_child_by_id(child_id)
    if child_db is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no child with this id")
    db_attendance = models.ChildAttendance.get_or_none(
        (models.ChildAttendance.id == id) & (models.ChildAttendance.date_visit == date_visit))
    if db_attendance is not None:
        remove_visit(child_id, date_visit)
    db_attendance = models.ChildAttendance(child=child_db, date_visit=date_visit, price=price)
    db_attendance.save(force_insert=True)
    return db_attendance


def remove_visit(child_id: int, date_visit: date):
    child_db = get_child_by_id(child_id)
    if child_db is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no child with this id")

    q = models.ChildAttendance.delete().where(
        (models.ChildAttendance.date_visit == date_visit) & (models.ChildAttendance.child == child_db))
    q.execute()


def is_visit_at_date(child_id: int, date: date):
    child_db = get_child_by_id(child_id)
    if child_db is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no child with this id")
    db_attendance = models.ChildAttendance.get_or_none(
        (models.ChildAttendance.child == child_db) & (models.ChildAttendance.date_visit == date))
    return db_attendance is not None


def get_number_of_visits(child_id: int) -> int:
    child_db = get_child_by_id(child_id)
    if child_db is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no child with this id")
    return len(list(child_db.visits))


def get_payment_arrears(child_id: int) -> int:
    child_db = get_child_by_id(child_id)
    if child_db is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no child with this id")
    payment_arrears = 0
    for visit in list(child_db.visits):
        payment_arrears += visit.price
    return payment_arrears
