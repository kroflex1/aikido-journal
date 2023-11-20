import enum

from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID

from . import enums
from app.database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    phone_number = Column(String, unique=True, nullable=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String, nullable=True)
    role = Column(Enum(enums.Role))
    hashed_password = Column(String)
