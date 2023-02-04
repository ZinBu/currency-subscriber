import logging
import typing

from fastapi import APIRouter, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_session
from database.models.crud.crud_controllers import CurrencyCrud
from exceptions.orm import IntegrityException
from structs import ResponseError
from .. import RouteWithExceptionHandler, tags

logger = logging.getLogger(__name__)


router = APIRouter(
    tags=[tags.EVENTS],
    prefix='/api/events',
    route_class=RouteWithExceptionHandler,
)

