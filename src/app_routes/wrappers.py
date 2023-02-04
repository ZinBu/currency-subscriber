from typing import Any, Callable

from exceptions import NotFoundException


def object_existence_required(func: Callable) -> Any:
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = await func(*args, **kwargs)
        if not result:
            raise NotFoundException()
        return result
    return wrapper
