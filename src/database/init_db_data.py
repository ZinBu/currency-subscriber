from database.crud.controllers import CurrencyCrud
from database.db import async_session

INIT_CURRENCIES = [
    'EURUSD',
    'USDJPY',
    'GBPUSD',
    'AUDUSD',
    'USDCAD',
]


async def init_data_in_db() -> None:
    async with async_session() as session:
        data = [dict(symbol=symbol) for symbol in INIT_CURRENCIES]
        await CurrencyCrud(session).bulk_create(data)
