from src.group import schemas, models
from src.auth import models as user_models


def get_group_by_name(group_name: str) -> models.Group:
    return models.Group.get(models.Group.name == group_name)


def get_names_of_groups_that_lead_by_coach(coach_db: user_models.User):
    return [group.name for group in list(coach_db.groups)]


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
