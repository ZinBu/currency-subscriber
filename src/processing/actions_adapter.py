import dataclasses
from typing import Optional

from fastapi import WebSocket

from managers import ConnectionManager
from structs.schemas.base import BasePydanticModel
from structs.schemas.currency import Assets, PointHistory, Point
from structs.schemas.actions import Action, SubscribeAction
from processing.currencies.utils import get_assets, get_currency_history_values, get_last_currency_history_value

from structs.choices import ALLOWED_ACTIONS, AllActions
from structs.subscriber import Subscriber


@dataclasses.dataclass
class ActionAdapter:
    client_id: int
    user_action: Action
    manager: ConnectionManager
    websocket: WebSocket

    async def perform_action(self) -> dict:
        response = await self.select_executor_by_action()
        return response.dict()

    async def select_executor_by_action(self) -> Action:
        if self.user_action.action not in ALLOWED_ACTIONS:
            return self.create_response({'error': 'Not allowed action'})
        elif self.user_action.action == AllActions.ASSETS:
            message = await self.get_assets_available_for_user()
            return self.create_response(message)
        elif self.user_action.action == AllActions.SUBSCRIBE:
            user_subscribe_action = SubscribeAction(**self.user_action.dict())
            asset_id = user_subscribe_action.asset_id
            point_history = await self.get_point_history(asset_id)
            subscriber = Subscriber(
                client_id=self.client_id,
                asset_id=asset_id,
                websocket=self.websocket,
                previous_point_time=point_history.points[-1].time if point_history.points else None
            )
            self.manager.subscribe(subscriber)
            return self.create_response(point_history)

    def create_response(self, message: BasePydanticModel | dict, new_action_name: Optional[str] = None) -> Action:
        return Action(
            action=new_action_name or self.user_action.action,
            message=message
        )

    @staticmethod
    async def get_assets_available_for_user() -> Assets:
        assets = await get_assets()
        return Assets(**dict(assets=assets))

    @staticmethod
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

    @staticmethod
    async def get_last_point(asset_id: int) -> Point:
        last_point = await get_last_currency_history_value(asset_id)
        return Point(
            assetName=last_point.currency.symbol,
            time=last_point.timestamp,
            assetId=last_point.currency.id,
            value=last_point.value,
        )
