from datetime import datetime

from pydantic import Field, validator

from structs.schemas.base import BasePydanticModel


class AssetItem(BasePydanticModel):
    id: int
    name: str = Field(alias='symbol')


class Assets(BasePydanticModel):
    assets: list[AssetItem]


class Point(BasePydanticModel):
    assetName: str
    time: int | datetime
    assetId: int
    value: float

    @validator('time')
    def transform_datetime_to_timestamp(cls, value: datetime) -> int:
        return int(value.timestamp())


class PointHistory(BasePydanticModel):
    points: list[Point]
