class RagTravelException(Exception):
    """Base exception for RAG-Travel domain errors."""
    pass


class ChatError(RagTravelException):
    """Raised when the chat RAG pipeline fails."""
    pass


class IngestError(RagTravelException):
    """Raised when data ingestion fails."""
    pass


class SearchError(RagTravelException):
    """Raised when vector search fails."""
    pass


class EmbeddingError(RagTravelException):
    """Raised when embedding generation fails."""
    pass


class LLMError(RagTravelException):
    """Raised when LLM generation fails."""
    pass


class MemoryError(RagTravelException):
    """Raised when chat history storage/retrieval fails."""
    pass


class AuthError(RagTravelException):
    """Raised on authentication/authorization failures."""
    pass
