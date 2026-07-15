from fastapi import APIRouter

from app.search.routes import search as search_routes

router = APIRouter()
router.include_router(search_routes.router, prefix="/v1")
