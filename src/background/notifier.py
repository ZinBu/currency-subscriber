import asyncio

from structs.schemas.currency import Action
from managers import connection_manager
from structs.choices import AllActions


async def background_subscribers_notifier() -> None:
    while True:
        for subscriber in connection_manager.subscribers.values():
            point = connection_manager.actual_currencies.get_currency_point(subscriber.asset_id)
            if point.time != subscriber.previous_point_time:
                subscriber.previous_point_time = point.time
                user_action = Action(
                    action=AllActions.POINT,
                    message=point,
                )
                await connection_manager.send_message(user_action.dict(), subscriber.websocket)
        await asyncio.sleep(.3)
