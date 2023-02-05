import logging

from . import fxcm

logger = logging.getLogger(__name__)


async def update_currencies() -> None:
    try:
        await fxcm.update()
    except Exception as error:
        logger.error(error)
