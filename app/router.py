from fastapi import APIRouter

from app.chat.router import router as chat_router
from app.ingest.router import router as ingest_router
from app.search.router import router as search_router

api_router = APIRouter()
api_router.include_router(chat_router)
api_router.include_router(ingest_router)
api_router.include_router(search_router)
