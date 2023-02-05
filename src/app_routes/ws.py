import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from managers import connection_manager as manager
from proccessing.actions import get_assets_available_for_user, get_point_history
from structs.choices import ALLOWED_ACTIONS, AllActions
from structs.subscriber import Subscriber
from structs.schemas.currency import Action

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await manager.recieve_message(websocket)
            user_action = Action(**data)
            if user_action.action not in ALLOWED_ACTIONS:
                user_action.message = {'error': 'Not allowed action'}
                await manager.send_message(user_action.dict(), websocket)
            elif user_action.action == AllActions.ASSETS:
                user_action.message = await get_assets_available_for_user()
                await manager.send_message(user_action.dict(), websocket)
            elif user_action.action == AllActions.SUBSCRIBE:
                asset_id = user_action.asset_id
                point_history = await get_point_history(asset_id)
                user_action.message = point_history
                await manager.send_message(user_action.dict(), websocket)
                subscriber = Subscriber(
                    client_id=client_id,
                    asset_id=asset_id,
                    websocket=websocket,
                    previous_point_time=point_history.points[-1].time if point_history.points else None
                )
                manager.subscribe(subscriber)

    except WebSocketDisconnect:
        manager.unsubscribe(client_id)
