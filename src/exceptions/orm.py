from fastapi import HTTPException
from starlette import status


class NotFoundException(HTTPException):
    def __init__(self, detail: str = 'Object not found.'):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class IntegrityException(HTTPException):
    def __init__(self, detail: str = 'Not acceptable error.'):
        super().__init__(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=detail)
