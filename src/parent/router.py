from fastapi import APIRouter, Depends, status

from src.dependencies import get_db
from src.auth import schemas as user_schemas
router = APIRouter(
    prefix="/parents",
    tags=["Parent"])

@router.get("/{parent_id}", dependencies=[Depends(get_db)],
             status_code=status.HTTP_200_OK, response_model=user_schemas.User)
async def get_parent(child: schemas.ChildCreate, coach: Annotated[user_models.User, Depends(is_coach)]):
    db_child = crud.get_child_by_name(name=child.name, surname=child.surname, patronymic=child.patronymic)
    if db_child:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Child with given name, surname and patronymic already exists")
    db_child = crud.create_child(child)
    return db_child