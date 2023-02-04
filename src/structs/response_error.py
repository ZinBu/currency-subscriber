from pydantic.dataclasses import dataclass


@dataclass
class ResponseError:
    message: str
    code: int
    error: bool = True
