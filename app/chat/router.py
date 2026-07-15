from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session
from app.chat.routes import chat as chat_routes

router = APIRouter()
router.include_router(chat_routes.router, prefix="/v1")
