from pydantic import BaseModel
from typing import Any


class ConversationMessage(BaseModel):
    role: str
    content: str
    timestamp: float | None = None


class ConversationHistory(BaseModel):
    conversation_id: str
    messages: list[ConversationMessage]
    ttl: int = 3600
