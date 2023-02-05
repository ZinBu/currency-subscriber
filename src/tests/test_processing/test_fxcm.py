from unittest import mock

from managers import currency_manager
import pytest
from sqlalchemy import select

from database.db import async_session
from database.models.currency import CurrencyHistory
from processing.currencies import fxcm
from processing.currencies.structs import FxcmItem
from processing.exceptions import CurrencyParseError
from tests.test_processing import dataset


async def test_currencies_parser():
    result = fxcm._parse_javascript_response(dataset.FXCM_RESPONSE)
    assert isinstance(result[0], FxcmItem)

    with pytest.raises(CurrencyParseError):
        fxcm._parse_javascript_response('FXCM_RESPONSE')


async def test_fxcm_update(monkeypatch):

    mock_currencies_data = mock.MagicMock(text=dataset.FXCM_RESPONSE)
    monkeypatch.setattr(fxcm, "_request_currencies_data", mock.AsyncMock(return_value=mock_currencies_data))
    monkeypatch.setattr(fxcm, "get_required_pairs_symbols_map", mock.AsyncMock(return_value=dataset.PAIRS_MAP))

    await fxcm.update()

    async with async_session() as session:
        currency_history = (await session.execute(select(CurrencyHistory))).scalars().all()
        assert len(currency_history) == len(dataset.PAIRS_MAP)

        dataset_values = dataset.PAIRS_MAP.values()
        for ch in currency_history:
            assert ch.currency_id in dataset_values
            # Check currency manager too
            assert currency_manager.get_currency_point(ch.currency_id)
