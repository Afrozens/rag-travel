from pydantic import BaseModel


class TripIngestRequest(BaseModel):
    trips: list[dict]


class PurchaseIngestRequest(BaseModel):
    purchases: list[dict]


class IngestResponse(BaseModel):
    ingested_count: int
    message: str
