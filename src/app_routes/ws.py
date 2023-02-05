import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from managers import connection_manager as manager
from processing.actions_adapter import ActionAdapter
from structs.schemas.actions import Action

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await manager.recieve_message(websocket)
            proxy_adapter = ActionAdapter(
                client_id=client_id,
                manager=manager,
                websocket=websocket,
                user_action=Action(**data)
            )
            response = await proxy_adapter.perform_action()
            await manager.send_message(response, websocket)

    except WebSocketDisconnect:
        manager.unsubscribe(client_id)
