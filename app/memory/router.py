from fastapi import APIRouter

from app.memory.schemas.memory import ConversationMessage, ConversationHistory

router = APIRouter()

# Este modulo no expone endpoints HTTP publicos por defecto.
# Placeholder para debug/health futuro.
