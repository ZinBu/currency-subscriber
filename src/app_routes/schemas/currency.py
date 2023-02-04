import datetime
from decimal import Decimal

from app_routes.schemas.base import BasePydanticModel


class CurrencyScheme(BasePydanticModel):
    id: int
    symbol: str


class CurrencyHistoryScheme(BasePydanticModel):
    value: Decimal
    timestamp: datetime.datetime
    currency_id: int

    # @validator('deadline')
    # def comment_must_contain_space(cls, value: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
    #     if value and not value.tzinfo:
    #         raise ValidationError('deadline must contain TZ info.')
    #     return value