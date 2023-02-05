import datetime
from dataclasses import dataclass
from typing import Optional

from starlette.websockets import WebSocket


@dataclass
class Subscriber:
    client_id: int
    asset_id: int
    websocket: WebSocket
    previous_point_time: Optional[datetime.datetime] = None
