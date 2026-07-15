from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    """
    Orquesta el pipeline RAG completo para el modulo chat.

    TODO: Implementar logica de negocio:
    1. Intent & Date Parsing.
    2. Parallel retrieval (vector search + purchases + history).
    3. Prompt augmentation.
    4. Generation (streaming).
    """

    async def chat(
        self,
        request: ChatRequest,
        user_id: str,
        session: AsyncSession,
    ) -> ChatResponse:
        raise NotImplementedError("ChatService.chat() no implementado todavia.")

    async def chat_stream(
        self,
        request: ChatRequest,
        user_id: str,
        session: AsyncSession,
    ):
        raise NotImplementedError("ChatService.chat_stream() no implementado todavia.")
