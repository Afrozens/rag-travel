from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session
from app.core.guards.auth import get_current_user
from app.search.schemas.search import SearchRequest, SearchResponse
from app.search.services.search_service import SearchService

router = APIRouter()


@router.post("/search/trips", response_model=SearchResponse)
async def search_trips(
    request: SearchRequest,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Busqueda vectorial debug de viajes con filtros de metadata.
    """
    service = SearchService()
    return await service.search(request, session)
