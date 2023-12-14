from . import models, schemas
from src.child import crud as child_crud
from src.child import schemas as child_schemas
from src.child import models as child_models
from datetime import date


def convert_group_model_to_schema(db_group: models.Group) -> schemas.GroupInf:
    children_at_group = child_crud.get_children_at_group(db_group.name)
    children_schemas = [
        child_schemas.Child(id=db_child.id,
                            parent_id=db_child.parent_id,
                            group_name_id=db_child.group_name_id,
                            name=db_child.name,
                            surname=db_child.surname,
                            patronymic=db_child.patronymic) for
        db_child in children_at_group]
    return schemas.GroupInf(name=db_group.name, price=db_group.price, coach_id=db_group.coach.id,
                            days=get_days_as_list_from_group_model(db_group), children=children_schemas)


def convert_child_model_to_child_attendance_inf_schema(db_child: child_models.Child,
                                                       attendance: list[schemas.DayInf]) -> schemas.ChildVisitInf:
    child_schema = schemas.ChildVisitInf(id=db_child.id, name=db_child.name, surname=db_child.surname,
                                         patronymic=db_child.patronymic,
                                         parent_id=db_child.parent_id,
                                         group_name_id=db_child.group_name_id,
                                         attendance=attendance)
    return child_schema


def get_days_as_list_from_group_model(group: models.Group) -> list[schemas.Time]:
    result = []
    if group.monday_start is not None:
        result.append(schemas.Time(start=group.monday_start, end=group.monday_end))
    else:
        result.append(None)

    if group.tuesday_start is not None:
        result.append(schemas.Time(start=group.tuesday_start, end=group.tuesday_end))
    else:
        result.append(None)

    if group.wednesday_start is not None:
        result.append(schemas.Time(start=group.wednesday_start, end=group.wednesday_end))
    else:
        result.append(None)

    if group.thursday_start is not None:
        result.append(schemas.Time(start=group.thursday_start, end=group.thursday_end))
    else:
        result.append(None)

    if group.friday_start is not None:
        result.append(schemas.Time(start=group.friday_start, end=group.friday_end))
    else:
        result.append(None)

    if group.saturday_start is not None:
        result.append(schemas.Time(start=group.saturday_start, end=group.saturday_end))
    else:
        result.append(None)

    if group.sunday_start is not None:
        result.append(schemas.Time(start=group.sunday_start, end=group.sunday_end))
    else:
        result.append(None)
    return result
