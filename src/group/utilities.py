from . import models, schemas


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
