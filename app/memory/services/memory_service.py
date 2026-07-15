from app.memory.repositories.memory_repository import MemoryRepository
from app.memory.schemas.memory import ConversationMessage, ConversationHistory


class MemoryService:
    """
    Servicio de gestion de sesiones de conversacion en Redis.

    TODO: Implementar logica de negocio:
    1. Obtener historial por conversation_id.
    2. Agregar mensajes con TTL.
    3. Gestionar limites de mensajes.
    """

    def __init__(self, repository: MemoryRepository | None = None):
        self.repository = repository or MemoryRepository()

    async def get_history(self, conversation_id: str, limit: int = 20) -> list[ConversationMessage]:
        return await self.repository.get_history(conversation_id, limit)

    async def add_message(self, conversation_id: str, message: ConversationMessage):
        return await self.repository.add_message(conversation_id, message)

    async def delete_conversation(self, conversation_id: str):
        return await self.repository.delete_conversation(conversation_id)
