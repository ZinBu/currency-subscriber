from database.db import async_session
from database.models.crud.crud_controllers import CurrencyCrud
from database.models.currency import CurrencyHistory


async def get_required_pairs_symbols_map() -> dict[str, int]:
    async with async_session() as session:
        result = await CurrencyCrud(session).get_all()
    return {x.symbol: x.id for x in result}


async def update_pairs(pairs: list[CurrencyHistory]) -> None:
    async with async_session() as session:
        await CurrencyCrud(session).bulk_create(pairs)
