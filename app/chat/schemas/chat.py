from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    referenced_trips: list[str] = []
    conversation_id: str | None = None


class StreamChunk(BaseModel):
    chunk: str
    done: bool = False
    referenced_trips: list[str] | None = None
