from pydantic import BaseModel
from typing import Any


class SearchFilter(BaseModel):
    start_date: str | None = None
    end_date: str | None = None
    agency: str | None = None
    destination: str | None = None
    category: str | None = None
    min_price: float | None = None
    max_price: float | None = None


class SearchRequest(BaseModel):
    query: str
    filters: SearchFilter | None = None
    top_k: int = 10


class TripResult(BaseModel):
    trip_id: str
    title: str
    destination: str
    agency: str
    start_date: str
    end_date: str
    price: float
    currency: str
    similarity: float
    content: str | None = None
    meta_data: dict[str, Any] | None = None


class SearchResponse(BaseModel):
    results: list[TripResult]
    total: int
    query: str
