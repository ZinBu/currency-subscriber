import asyncio

from processing.currencies.updater import update_currencies


async def currency_updater():
    """
    Update currencies every 1 second.
    It's better doing in a separate framework like Celery,
    because it gives more flexibility and does not affect negatively in case of process scaling.
    """
    while True:
        await update_currencies()
        await asyncio.sleep(0.7)
