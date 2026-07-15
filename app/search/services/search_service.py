from sqlalchemy.ext.asyncio import AsyncSession

from app.search.schemas.search import SearchRequest, SearchResponse


class SearchService:
    """
    Servicio de busqueda vectorial con filtros de metadata.

    TODO: Implementar logica de negocio:
    1. Embed query con Jina.
    2. Query pgvector con similarity search + filtros JSONB.
    3. Retornar resultados enriquecidos.
    """

    async def search(
        self,
        request: SearchRequest,
        session: AsyncSession,
    ) -> SearchResponse:
        raise NotImplementedError("SearchService.search() no implementado todavia.")
