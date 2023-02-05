import dataclasses

from starlette.websockets import WebSocket

from structs.schemas.currency import Point
from structs.subscriber import Subscriber


@dataclasses.dataclass
class CurrencyManager:
    # TODO Cache system should be here (like redis or memcached) if we are going to scale system.
    actual_currencies: dict[int, Point] = dataclasses.field(default_factory=dict)

    def set_or_update_currency_point(self, point: Point) -> None:
        self.actual_currencies[point.assetId] = point

    def get_currency_point(self, asset_id: int) -> Point:
        return self.actual_currencies[asset_id]


@dataclasses.dataclass
class ConnectionManager:
    actual_currencies: CurrencyManager
    subscribers: dict[int, Subscriber] = dataclasses.field(default_factory=dict)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()

    async def send_message(self, message: dict, websocket: WebSocket) -> None:
        await websocket.send_json(message)

    async def recieve_message(self, websocket: WebSocket) -> dict:
        return await websocket.receive_json()

    def subscribe(self, subscriber: Subscriber) -> None:
        self.subscribers[subscriber.client_id] = subscriber

    def unsubscribe(self, client_id: int) -> None:
        if client_id in self.subscribers:
            del self.subscribers[client_id]


currency_manager = CurrencyManager()
connection_manager = ConnectionManager(actual_currencies=currency_manager)
