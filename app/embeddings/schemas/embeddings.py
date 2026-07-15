from pydantic import BaseModel


class EmbedRequest(BaseModel):
    texts: list[str]
    task: str = "retrieval.passage"  # o "retrieval.query"
    normalized: bool = True


class EmbedResponse(BaseModel):
    embeddings: list[list[float]]
    model: str
    dimensions: int
