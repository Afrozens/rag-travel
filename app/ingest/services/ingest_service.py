from sqlalchemy.ext.asyncio import AsyncSession

from app.ingest.schemas.ingest import TripIngestRequest, PurchaseIngestRequest, IngestResponse


class IngestService:
    """
    Pipeline de ingestion de viajes y compras.

    TODO: Implementar logica de negocio:
    1. Validar schema del JSON.
    2. Chunking de descripciones largas.
    3. Generacion de embeddings con Jina.
    4. Upsert a PostgreSQL + pgvector.
    """

    async def ingest_trips(
        self,
        request: TripIngestRequest,
        session: AsyncSession,
    ) -> IngestResponse:
        raise NotImplementedError("IngestService.ingest_trips() no implementado todavia.")

    async def ingest_purchases(
        self,
        request: PurchaseIngestRequest,
        session: AsyncSession,
    ) -> IngestResponse:
        raise NotImplementedError("IngestService.ingest_purchases() no implementado todavia.")
