from structs.schemas.currency import Assets, PointHistory, Point
from proccessing.currencies.utils import get_assets, get_currency_history_values, get_last_currency_history_value


async def get_assets_available_for_user() -> Assets:
    assets = await get_assets()
    return Assets(**dict(assets=assets))


async def get_point_history(asset_id: int) -> PointHistory:
    history = await get_currency_history_values(asset_id)
    return PointHistory(
        points=[
            Point(
                assetName=h.currency.symbol,
                time=h.timestamp,
                assetId=h.currency.id,
                value=h.value,
            )
            for h in history
        ]
    )


async def get_last_point(asset_id: int) -> Point:
    last_point = await get_last_currency_history_value(asset_id)
    return Point(
        assetName=last_point.currency.symbol,
        time=last_point.timestamp,
        assetId=last_point.currency.id,
        value=last_point.value,
    )
