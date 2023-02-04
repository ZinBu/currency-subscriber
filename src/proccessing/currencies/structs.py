from pydantic import Field

from decimal import Decimal

from app_routes.schemas.base import BasePydanticModel


class FxcmItem(BasePydanticModel):
    symbol: str = Field(alias='Symbol')
    bid: int = Field(alias='Bid')
    ask: int = Field(alias='Ask')

    @property
    def value(self) -> Decimal:
        return (Decimal(self.bid) + Decimal(self.ask)) / 2


class FxcmItemList(BasePydanticModel):
    Rates: list[FxcmItem]
