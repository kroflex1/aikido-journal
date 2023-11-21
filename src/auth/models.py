import enum

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base
import uuid


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, nullable=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String, nullable=True)
    role = Column(String)
    hashed_password = Column(String)
