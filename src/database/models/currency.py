from sqlalchemy import Column, String, DECIMAL, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from ..base import OnDeleteForeignKeyActions
from ..db import SQLModel


class Currency(SQLModel):
    symbol = Column(String(20), nullable=False)


class CurrencyHistory(SQLModel):
    value = Column(DECIMAL(), nullable=False)
    timestamp = Column(DateTime(timezone=False), nullable=True)

    currency_id = Column(BigInteger, ForeignKey('currency.id', ondelete=OnDeleteForeignKeyActions.SET_NULL))
    currency = relationship('Currency', backref='history')
