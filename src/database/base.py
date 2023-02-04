import datetime

from sqlalchemy import Column, BigInteger, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr


class OnDeleteForeignKeyActions:
    SET_NULL = 'SET NULL'
    CASCADE = 'CASCADE'


class BaseSQLModel:
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False)

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
