import asyncio
import logging
from dataclasses import asdict
from typing import Callable

import starlette.exceptions
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

from exceptions import AppException
from structs import ResponseError

logger = logging.getLogger(__name__)


# TODO Кажется лучше вынести в мидлваре
class RouteWithExceptionHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                response: Response = await original_route_handler(request)
            except (HTTPException, starlette.exceptions.HTTPException) as e:
                value = ResponseError(
                    message=e.detail,
                    code=e.code if hasattr(e, 'code') else -2
                )
                response = JSONResponse(status_code=e.status_code, content=asdict(value))
            except asyncio.TimeoutError as e:
                logger.exception(e)
                value = ResponseError(
                    message='Timeout for external services. Try again',
                    code=e.code if hasattr(e, 'code') else -2  # type: ignore
                )
                response = JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=asdict(value))
            except AppException as e:
                logger.exception(e)
                value = ResponseError(
                    message=str(e),
                    code=e.code if hasattr(e, 'code') else -2
                )
                response = JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=asdict(value))
            except (ValueError, KeyError) as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                logger.exception(e)
                value = ResponseError(
                    message='Unknown error while processing request',
                    code=-1
                )
                response = JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=asdict(value))

            return response

        return custom_route_handler
