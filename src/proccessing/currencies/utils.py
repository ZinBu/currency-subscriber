import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.db import async_session
from database.crud.controllers import CurrencyCrud
from database.models.currency import CurrencyHistory, Currency


async def get_required_pairs_symbols_map() -> dict[str, int]:
    assets = await get_assets()
    return {x.symbol: x.id for x in assets}


async def update_currency_history(pairs: list[CurrencyHistory]) -> None:
    async with async_session() as session:
        await CurrencyCrud(session).bulk_create(pairs)


async def get_assets() -> list[Currency]:
    async with async_session() as session:
        return await CurrencyCrud(session).get_all()


async def get_currency_history_values(asset_id: int, for_last_m: int = 30) -> list[CurrencyHistory]:
    time_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=for_last_m)
    async with async_session() as session:
        result = await session.execute(
            select(CurrencyHistory)
            .options(joinedload(CurrencyHistory.currency, innerjoin=True))
            .where(CurrencyHistory.currency_id == asset_id and CurrencyHistory.timestamp >= time_limit)
            .order_by(CurrencyHistory.timestamp.asc())
        )
        return result.scalars().all()


async def get_last_currency_history_value(asset_id: int) -> CurrencyHistory:
    async with async_session() as session:
        result = await session.execute(
            select(CurrencyHistory)
            .options(joinedload(CurrencyHistory.currency, innerjoin=True))
            .where(CurrencyHistory.currency_id == asset_id)
            .order_by(CurrencyHistory.timestamp.desc())
        )
        return result.scalars().first()
