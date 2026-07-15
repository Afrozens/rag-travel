import os

from fastapi import Depends
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Server
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    reload: bool = os.getenv("RELOAD", "true").lower() == "true"

    # PostgreSQL
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_user: str = os.getenv("DB_USER", "rag_travel")
    db_password: str = os.getenv("DB_PASSWORD", "secret")
    db_name: str = os.getenv("DB_NAME", "rag_travel")

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_chat_ttl: int = int(os.getenv("REDIS_CHAT_TTL", "3600"))
    redis_chat_max_messages: int = int(os.getenv("REDIS_CHAT_MAX_MESSAGES", "20"))

    # Jina AI
    jina_api_key: str = os.getenv("JINA_API_KEY", "")
    jina_embedding_model: str = os.getenv("JINA_EMBEDDING_MODEL", "jina-embeddings-v4")
    jina_embedding_dimensions: int = int(os.getenv("JINA_EMBEDDING_DIMENSIONS", "2048"))

    # Google Gemini
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    gemini_temperature: float = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
    gemini_max_output_tokens: int = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "2048"))

    # Auth
    jwt_secret: str = os.getenv("JWT_SECRET", "super-secret-key")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_hours: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

    # RAG Config
    rag_top_k: int = int(os.getenv("RAG_TOP_K", "10"))
    rag_similarity_threshold: float = float(os.getenv("RAG_SIMILARITY_THRESHOLD", "0.75"))


# Singleton global (se puede sobreescribir en tests)
_settings = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
