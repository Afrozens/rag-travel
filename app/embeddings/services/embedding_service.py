from app.embeddings.schemas.embeddings import EmbedRequest, EmbedResponse


class EmbeddingService:
    """
    Cliente async para Jina Embeddings v4.

    TODO: Implementar logica de negocio:
    1. Llamar a api.jina.ai/v1/embeddings con httpx.
    2. Manejar rate limits y errores.
    3. Cache opcional de embeddings.
    """

    async def embed(self, request: EmbedRequest) -> EmbedResponse:
        raise NotImplementedError("EmbeddingService.embed() no implementado todavia.")
