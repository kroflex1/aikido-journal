from datetime import date, timedelta
from typing import Annotated

from fastapi import APIRouter, status, Body
from fastapi import Depends, HTTPException

from src.auth import models
from src.auth.router import get_current_user
from src.child import crud as child_crud
from src.child import schemas as child_schemas
from src.dependencies import get_db
from . import crud, schemas
from .utilities import get_days_as_list_from_group_model, convert_group_model_to_schema, \
    convert_child_model_to_child_attendance_inf_schema

router = APIRouter(
    prefix="/groups",
    tags=["Group"])


async def is_coach(current_user: Annotated[models.User, Depends(get_current_user)]) -> models.User:
    lack_of_access_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Only coach can execute this request",
    )
    if current_user.role == 'coach':
        return current_user
    raise lack_of_access_exception


@router.post("/create", dependencies=[Depends(get_db)],
             status_code=status.HTTP_201_CREATED, response_model=schemas.GroupInf)
async def create_group(group: schemas.GroupCreate, coach: Annotated[models.User, Depends(is_coach)]):
    db_group = crud.get_group_by_name(group_name=group.name)
    if db_group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Group with this name has already been created")
    db_group = crud.create_group(group_create=group, coach_id=coach.id)
    return convert_group_model_to_schema(db_group)


@router.get("/get/{group_name}", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK, response_model=schemas.GroupInf)
async def get_information_about_group(group_name: str, coach: Annotated[models.User, Depends(is_coach)]):
    db_group = crud.get_group_by_name(group_name=group_name)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no group with this name")
    return schemas.GroupInf(name=db_group.name, price=db_group.price, coach_id=coach.id,
                            days=get_days_as_list_from_group_model(db_group))


@router.get("/leads", dependencies=[Depends(get_db)],
            status_code=status.HTTP_200_OK, description="Returns the names of the groups led by coach",
            response_model=list[schemas.GroupInf])
async def get_groups_that_led_by_coach(coach: Annotated[models.User, Depends(is_coach)]):
    result = []
    for db_group in crud.get_groups_that_led_by_coach(coach):
        result.append(convert_group_model_to_schema(db_group))
    return result


@router.post("/remove/{group_name}", dependencies=[Depends(get_db)],
             status_code=status.HTTP_200_OK)
async def remove_group(group_name: str, coach: Annotated[models.User, Depends(is_coach)]):
    crud.remove_group(group_name)
    return "Group has been successfully remove"


@router.post("/{group_name}/add_child/{child_id}", dependencies=[Depends(get_db)],
             status_code=status.HTTP_200_OK, response_model=child_schemas.Child)
async def add_child_to_group(group_name: str, child_id: int, coach: Annotated[models.User, Depends(is_coach)]):
    db_group = crud.get_group_by_name(group_name=group_name)
    db_child = child_crud.get_child_by_id(child_id)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no group with this name")
    if db_child is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no child with this id")
    if db_child.group_name is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This child is already in the group '{db_child.group_name.name}'")
    db_child.group_name = db_group
    db_child.save()
    return db_child


@router.post("/{group_name}/remove_child/{child_id}", dependencies=[Depends(get_db)],
             status_code=status.HTTP_200_OK, response_model=child_schemas.Child)
async def remove_child_from_group(group_name: str, child_id: int, coach: Annotated[models.User, Depends(is_coach)]):
    db_group = crud.get_group_by_name(group_name=group_name)
    db_child = child_crud.get_child_by_id(child_id)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no group with this name")
    if db_child is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no child with this id")
    if db_child.group_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This child does not belong to any group")
    if db_child.group_name.name != db_group.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This child is in another group '{db_child.group_name.name}'")
    db_child.group_name = None
    db_child.save()
    return db_child


@router.post("/{group_name}/set_parameters", dependencies=[Depends(get_db)],
             status_code=status.HTTP_200_OK, response_model=schemas.GroupInf)
async def set_new_parameters_for_group(group_name: str, new_group_parameters: schemas.GroupChange,
                                       coach: Annotated[models.User, Depends(is_coach)]):
    db_group = crud.get_group_by_name(group_name)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no group with this name")
    db_group = crud.set_new_parameters(group_name, new_group_parameters)
    return convert_group_model_to_schema(db_group)


@router.post("/{group_name}/fill_attendance/{start_date}", dependencies=[Depends(get_db)],
             status_code=status.HTTP_200_OK,
             response_model=schemas.Attendance)
async def fill_attendance(group_name: str, start_date: date, attendance_create: schemas.AttendanceCreate,
                          coach: Annotated[models.User, Depends(is_coach)]):
    db_group = crud.get_group_by_name(group_name)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no group with this name")
    group_schema = convert_group_model_to_schema(db_group)
    for child_attendance in attendance_create.children_attendance:
        for day_inf in child_attendance.attendance:
            mark_child_visit(group_schema, child_attendance.id, day_inf)
    return get_attendance(db_group.name, start_date=start_date)


@router.post("/{group_name}/get_attendance/{start_date}", dependencies=[Depends(get_db)],
             status_code=status.HTTP_200_OK, response_model=schemas.Attendance)
async def get_attendance_for_group(group_name: str, start_date: date,
                                   coach: Annotated[models.User, Depends(is_coach)]):
    return get_attendance(group_name, start_date)

def get_attendance(group_name: str, start_date: date) -> schemas.Attendance:
    db_group = crud.get_group_by_name(group_name)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no group with this name")

    children_attendance = []
    for db_child in list(db_group.children):
        child_attendance = []
        current_day = start_date
        for i in range(7):
            is_training = child_crud.is_visit_at_date(db_child.id, current_day)
            child_attendance.append(schemas.DayInf(date=current_day, is_training=is_training))
            current_day = current_day + timedelta(days=1)
        children_attendance.append(convert_child_model_to_child_attendance_inf_schema(db_child, child_attendance))

    schedule = []
    current_day = start_date
    times = get_days_as_list_from_group_model(db_group)
    for i in range(7):
        schedule.append(schemas.DayInf(date=current_day, is_training=times[i] is not None))
        current_day = current_day + timedelta(days=1)

    return schemas.Attendance(group_name=db_group.name, children_attendance=children_attendance, schedule=schedule)


def mark_child_visit(group: schemas.GroupInf, child_id: int, visit_inf: schemas.DayInf):
    day_of_week = date.weekday(visit_inf.date)
    if group.days[day_of_week] is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The group has no classes on {day_of_week + 1} day of the week")
    if visit_inf.is_training:
        child_crud.mark_visit(child_id=child_id, date_visit=visit_inf.date)
    else:
        child_crud.remove_visit(child_id=child_id, date_visit=visit_inf.date)
