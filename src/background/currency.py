import asyncio

from proccessing.currencies.updater import update_currencies


async def currency_updater():
    """Update currencies every 1 second"""
    while True:
        await update_currencies()
        await asyncio.sleep(0.7)
