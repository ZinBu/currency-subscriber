import datetime
import typing
from unittest import mock

import pytest
from sqlalchemy import select

from database.db import async_session
from database.models.currency import Currency, CurrencyHistory
from processing.actions_adapter import ActionAdapter
from structs.choices import AllActions
from structs.schemas.actions import Action


def _get_raw_action_response(assets: list) -> dict:
    return {
        "action": "assets",
        "message": {
            "assets": assets
        }
    }


async def _test_action_adapter(action: Action) -> tuple[dict, mock.MagicMock]:
    manager_mock = mock.MagicMock()
    proxy_adapter = ActionAdapter(
        client_id=1,
        manager=manager_mock,
        websocket=mock.MagicMock(),
        user_action=action
    )
    return await proxy_adapter.perform_action(), manager_mock


async def test_action_adapter_asset():
    action = Action(
        action=AllActions.ASSETS,
        message={}
    )

    response, _ = await _test_action_adapter(action)

    # Get the all assets
    async with async_session() as session:
        assets = (await session.execute(select(Currency))).scalars().all()

    assert response == _get_raw_action_response([dict(id=x.id, name=x.symbol) for x in assets])


@pytest.fixture
async def create_initial_points_history() -> typing.Coroutine:
    dtn = datetime.datetime.utcnow()
    # Get the first asset
    async with async_session() as session:
        asset = (await session.execute(select(Currency))).scalars().first()
        history = [
            CurrencyHistory(
                value=15,
                timestamp=dtn,
                currency_id=asset.id
            ),
            CurrencyHistory(
                value=1,
                timestamp=dtn,
                currency_id=asset.id
            ),
        ]
        session.add_all(history)
        await session.commit()
    yield


async def test_action_adapter_subscribe(create_initial_points_history):
    # Get the first asset
    async with async_session() as session:
        asset = (await session.execute(select(Currency))).scalars().first()

    action = Action(
        action=AllActions.SUBSCRIBE,
        message=dict(assetId=asset.id)
    )
    response, manager_mock = await _test_action_adapter(action)

    # Check that user has been subscribed
    manager_mock.subscribe.assert_called()

    # Get point's history
    async with async_session() as session:
        history = (await session.execute(select(CurrencyHistory))).scalars().all()
    points = response['message']['points']
    assert len(points) == len(history)
