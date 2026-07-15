from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session
from app.ingest.schemas.ingest import TripIngestRequest, PurchaseIngestRequest, IngestResponse
from app.ingest.services.ingest_service import IngestService

router = APIRouter()


@router.post("/ingest/trips", response_model=IngestResponse)
async def ingest_trips(
    request: TripIngestRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Ingestar catalogo de viajes (trips + embeddings).
    """
    service = IngestService()
    return await service.ingest_trips(request, session)


@router.post("/ingest/purchases", response_model=IngestResponse)
async def ingest_purchases(
    request: PurchaseIngestRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Ingestar compras de usuarios (estructurado, sin embeddings).
    """
    service = IngestService()
    return await service.ingest_purchases(request, session)
