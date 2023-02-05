import datetime
import json

import httpx

from structs.schemas.currency import Point
from database.models.currency import CurrencyHistory
from managers import currency_manager
from processing import exceptions
from .structs import FxcmItem, FxcmItemList
from .utils import get_required_pairs_symbols_map, update_currency_history

CURRENCY_URL = 'https://ratesjson.fxcm.com/DataDisplayer'
TIMEOUT_S = 2.

_PREFIX = 'null('
_POSTFIX = ');'


async def update() -> None:
    dtn, currencies = await _request_currencies()
    required_pairs_symbols_map = await get_required_pairs_symbols_map()
    filtered_and_instanced_currencies = _update_currency_manager_and_get_history_objects(
        dtn,
        currencies,
        required_pairs_symbols_map,
    )
    await update_currency_history(filtered_and_instanced_currencies)


async def _request_currencies() -> tuple[datetime.datetime, list[FxcmItem]]:
    dtn = datetime.datetime.utcnow()
    response = await _request_currencies_data()
    return dtn, _parse_javascript_response(response.text)


async def _request_currencies_data() -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.get(CURRENCY_URL, timeout=TIMEOUT_S)
        response.raise_for_status()
        return response


def _parse_javascript_response(text: str) -> list[FxcmItem]:
    """Probably, here could be better to avoid serialization and return the raw data"""
    text = text.strip()
    if text.startswith(_PREFIX) and text.endswith(_POSTFIX):
        return FxcmItemList(**json.loads(text[len(_PREFIX):-len(_POSTFIX)])).Rates

    raise exceptions.CurrencyParseError()


def _update_currency_manager_and_get_history_objects(
        dtn: datetime.datetime,
        currencies: list[FxcmItem],
        required_pairs_symbols_map: dict[str, int]
) -> list[CurrencyHistory]:
    filtered_and_instanced_currencies = []
    for item in currencies:
        if item.symbol in required_pairs_symbols_map:
            filtered_and_instanced_currencies.append(
                CurrencyHistory(
                    value=item.value,
                    timestamp=dtn,
                    currency_id=required_pairs_symbols_map[item.symbol]
                )
            )
            currency_manager.set_or_update_currency_point(
                Point(
                    assetName=item.symbol,
                    time=dtn,
                    assetId=required_pairs_symbols_map[item.symbol],
                    value=item.value,
                )
            )
    return filtered_and_instanced_currencies
