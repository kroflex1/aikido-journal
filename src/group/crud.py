from fastapi import HTTPException, status

from src.auth import models as user_models
from src.group import schemas, models


def get_group_by_name(group_name: str) -> models.Group | None:
    return models.Group.get_or_none(models.Group.name == group_name)


def get_groups_that_led_by_coach(coach_db: user_models.User) -> list[models.Group]:
    return [group for group in list(coach_db.groups)]


def set_new_price_for_group(group_name: str, price: int):
    db_group = get_group_by_name(group_name)
    db_group.price = price
    db_group.save()


def set_new_parameters(group_name: str, group_change: schemas.GroupChange) -> models.Group:
    db_group = get_group_by_name(group_name)
    if group_change.price is not None:
        db_group.price = group_change.price
        db_group.save()
    if group_change.days is not None:
        set_days_for_group(db_group, group_change.days)
        db_group.save()
    if group_change.name is not None and group_name != group_change.name:
        children = list(db_group.children)
        for child in children:
            child.group_name = None
            child.save()
        models.Group.update(name=group_change.name).where(models.Group.name == group_name).execute()
        db_group = get_group_by_name(group_change.name)
        for child in children:
            child.group_name = db_group
            child.save()
    db_group.save()
    return db_group


def remove_group(group_name: str):
    db_group = models.Group.get_or_none(models.Group.name == group_name)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no group with this name")
    db_children = list(db_group.children)
    for db_child in db_children:
        db_child.group_name = None
        db_child.save()
    db_group.delete_instance()


def create_group(group_create: schemas.GroupCreate, coach_id: int) -> models.Group:
    monday_start = None
    monday_end = None
    tuesday_start = None
    tuesday_end = None
    wednesday_start = None
    wednesday_end = None
    thursday_start = None
    thursday_end = None
    friday_start = None
    friday_end = None
    saturday_start = None
    saturday_end = None
    sunday_start = None
    sunday_end = None
    if group_create.days[0] is not None:
        monday_start = group_create.days[0].start
        monday_end = group_create.days[0].end
    if group_create.days[1] is not None:
        tuesday_start = group_create.days[1].start
        tuesday_end = group_create.days[1].end
    if group_create.days[2] is not None:
        wednesday_start = group_create.days[2].start
        wednesday_end = group_create.days[2].end
    if group_create.days[3] is not None:
        thursday_start = group_create.days[3].start
        thursday_end = group_create.days[3].end
    if group_create.days[4] is not None:
        friday_start = group_create.days[4].start
        friday_end = group_create.days[4].end
    if group_create.days[5] is not None:
        saturday_start = group_create.days[5].start
        saturday_end = group_create.days[5].end
    if group_create.days[6] is not None:
        sunday_start = group_create.days[6].start
        sunday_end = group_create.days[6].end

    db_group = models.Group(name=group_create.name, price=group_create.price, coach=coach_id,
                            monday_start=monday_start, monday_end=monday_end,
                            tuesday_start=tuesday_start, tuesday_end=tuesday_end,
                            wednesday_start=wednesday_start, wednesday_end=wednesday_end,
                            thursday_start=thursday_start, thursday_end=thursday_end,
                            friday_start=friday_start, friday_end=friday_end,
                            saturday_start=saturday_start, saturday_end=saturday_end,
                            sunday_start=sunday_start, sunday_end=sunday_end)
    db_group.save(force_insert=True)
    return db_group


def set_days_for_group(db_group: models.Group, days: list[schemas.Time | None]):
    db_group.monday_start = days[0].start if days[0] is not None else None
    db_group.monday_end = days[0].end if days[0] is not None else None

    db_group.tuesday_start = days[1].start if days[1] is not None else None
    db_group.tuesday_end = days[1].end if days[1] is not None else None

    db_group.wednesday_start = days[2].start if days[2] is not None else None
    db_group.wednesday_end = days[2].end if days[2] is not None else None

    db_group.thursday_start = days[3].start if days[3] is not None else None
    db_group.thursday_end = days[3].end if days[3] is not None else None

    db_group.friday_start = days[4].start if days[4] is not None else None
    db_group.friday_end = days[4].end if days[4] is not None else None

    db_group.saturday_start = days[5].start if days[5] is not None else None
    db_group.saturday_end = days[5].end if days[5] is not None else None

    db_group.sunday_start = days[6].start if days[6] is not None else None
    db_group.sunday_end = days[6].end if days[6] is not None else None
