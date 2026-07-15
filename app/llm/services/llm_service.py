from app.llm.schemas.llm import LLMRequest, LLMResponse, StreamChunk


class LLMService:
    """
    Cliente async para Google Gemini con streaming SSE.

    TODO: Implementar logica de negocio:
    1. Configurar google.generativeai.
    2. Enviar mensajes con streaming.
    3. Yield de chunks para SSE.
    """

    async def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError("LLMService.generate() no implementado todavia.")

    async def generate_stream(self, request: LLMRequest):
        raise NotImplementedError("LLMService.generate_stream() no implementado todavia.")
