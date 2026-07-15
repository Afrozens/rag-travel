from pydantic import BaseModel


class LLMRequest(BaseModel):
    prompt: str
    system_prompt: str | None = None
    temperature: float = 0.7
    max_output_tokens: int = 2048


class LLMResponse(BaseModel):
    text: str
    finish_reason: str | None = None


class StreamChunk(BaseModel):
    chunk: str
    done: bool = False
