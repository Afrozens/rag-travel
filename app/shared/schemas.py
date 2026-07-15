from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class StandardResponseDto(BaseModel, Generic[T]):
    success: bool = True
    data: T | None = None
    message: str | None = None
    error: str | None = None


class Pagination(BaseModel):
    page: int = 1
    limit: int = 20
    total: int = 0
