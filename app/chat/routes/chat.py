from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session
from app.core.guards.auth import get_current_user
from app.chat.schemas.chat import ChatRequest, ChatResponse
from app.chat.services.chat_service import ChatService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Enviar mensaje al chatbot RAG (respuesta completa, no streaming).
    """
    service = ChatService()
    return await service.chat(request, user_id, session)


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Chat con respuesta en streaming (SSE).
    """
    service = ChatService()
    return await service.chat_stream(request, user_id, session)
