from fastapi import APIRouter

from app.llm.schemas.llm import LLMRequest, LLMResponse, StreamChunk

router = APIRouter()

# Este modulo no expone endpoints HTTP publicos por defecto.
# Placeholder para health/debug futuro.
