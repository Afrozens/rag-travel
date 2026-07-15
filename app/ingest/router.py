from fastapi import APIRouter

from app.ingest.routes import ingest as ingest_routes

router = APIRouter()
router.include_router(ingest_routes.router, prefix="/v1")
