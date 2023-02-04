import asyncio
import logging

from fastapi import FastAPI

from app_routes.api import ws
from background.currency import currency_updater
from database.init_db_data import init_data_in_db
from settings import settings
from database.db import init_db

logger = logging.getLogger(__name__)


app = FastAPI(
    version='1.0.0',
    title=settings.app_name
)

app.include_router(ws.router)


@app.on_event('startup')
async def startup_event() -> None:
    logger.info('Start')
    await init_db()
    await init_data_in_db()
    logger.info('Start background task.')
    asyncio.create_task(currency_updater())
