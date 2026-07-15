from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine
from app.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: None)
    yield
    await engine.dispose()


app = FastAPI(title="RAG-Travel", version="0.1.0", lifespan=lifespan)
app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
