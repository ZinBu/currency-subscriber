import datetime
import json

import httpx

from database.models.currency import CurrencyHistory
from proccessing import exceptions
from .structs import FxcmItem, FxcmItemList
from .utils import get_required_pairs_symbols_map, update_pairs

CURRENCY_URL = 'https://ratesjson.fxcm.com/DataDisplayer'
TIMEOUT_S = 2.

_PREFIX = 'null('
_POSTFIX = ');\n'


async def update() -> None:
    dtn, currencies = await _request_currencies()
    required_pairs_symbols_map = await get_required_pairs_symbols_map()
    filtered_and_instanced_currencies = [
        CurrencyHistory(
            value=item.value,
            timestamp=dtn,
            currency_id=required_pairs_symbols_map[item.symbol]
        )
        for item in currencies
        if item.symbol in required_pairs_symbols_map
    ]
    await update_pairs(filtered_and_instanced_currencies)


async def _request_currencies() -> tuple[datetime.datetime, list[FxcmItem]]:
    dtn = datetime.datetime.utcnow()
    async with httpx.AsyncClient() as client:
        response = await client.get(CURRENCY_URL, timeout=TIMEOUT_S)
    return dtn, _parse_javascript_response(response.text)


def _parse_javascript_response(text: str) -> list[FxcmItem]:
    if text.startswith(_PREFIX) and text.endswith(_POSTFIX):
        return FxcmItemList(**json.loads(text[len(_PREFIX):-len(_POSTFIX)])).Rates

    raise exceptions.CurrencyParseError()
