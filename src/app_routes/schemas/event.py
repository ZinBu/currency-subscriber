import datetime
from enum import Enum
from typing import Optional

from pydantic import Field, validator, ValidationError

from .base import PositionRequiredField


class EventTypes(str, Enum):
    asap = 'asap'
    normal = 'normal'


class EventIn(PositionRequiredField):
    type: EventTypes = Field(description='Тип события')
    comment: str = Field(max_length=255, description='Общий комментарий')
    deadline: Optional[datetime.datetime] = Field(description='Время, до которого желательно оказать помощь')

    @validator('deadline')
    def comment_must_contain_space(cls, value: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        if value and not value.tzinfo:
            raise ValidationError('deadline must contain TZ info.')
        return value


class EventOut(EventIn):
    id: int
