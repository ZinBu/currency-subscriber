from database import Currency
from .base_crud import BaseOrmCrudTool


class CurrencyCrud(BaseOrmCrudTool):
    model = Currency
