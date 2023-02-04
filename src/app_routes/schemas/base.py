from typing import Optional

from pydantic import BaseModel, Field


class BasePydanticModel(BaseModel):
    class Config:
        orm_mode = True


class Position(BasePydanticModel):
    lat: float = Field(description='Широта')
    lng: float = Field(description='Долгота')


class PositionRequiredField(BasePydanticModel):
    position: Position = Field(description='Координаты')


class PositionNullableField(BasePydanticModel):
    position: Optional[Position] = Field(description='Координаты', default=None)
