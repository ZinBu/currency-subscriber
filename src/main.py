import asyncio
import logging

from fastapi import FastAPI

from app_routes import client, ws
from background.currency import currency_updater
from background.notifier import background_subscribers_notifier
from database.init_db_data import init_data_in_db
from settings import settings
from database.db import init_db

logger = logging.getLogger(__name__)


app = FastAPI(
    version='1.0.0',
    title=settings.app_name
)

app.include_router(ws.router)
app.include_router(client.router)


@app.on_event('startup')
async def startup_event() -> None:
    logger.info('Start')
    await init_db()
    await init_data_in_db()
    logger.info('Start background task.')
    asyncio.create_task(currency_updater())
    asyncio.create_task(background_subscribers_notifier())
