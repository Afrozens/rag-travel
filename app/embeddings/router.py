from fastapi import APIRouter

from app.embeddings.schemas.embeddings import EmbedRequest, EmbedResponse

router = APIRouter()

# Este modulo no expone endpoints HTTP publicos por defecto.
# Se incluye un placeholder para health/debug si es necesario en el futuro.
