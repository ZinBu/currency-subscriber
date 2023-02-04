from sqlalchemy import Column, String

from ..db import SQLModel


class User(SQLModel):
    name = Column(String(50), nullable=True)
    surname = Column(String(50), nullable=True)
