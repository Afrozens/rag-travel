from app.memory.schemas.memory import ConversationMessage, ConversationHistory


class MemoryRepository:
    """
    Repositorio de conversaciones en Redis.

    TODO: Implementar logica de negocio:
    1. get_history(conversation_id, limit).
    2. add_message(conversation_id, role, content).
    3. delete_conversation(conversation_id).
    """

    async def get_history(self, conversation_id: str, limit: int = 20) -> list[ConversationMessage]:
        raise NotImplementedError("MemoryRepository.get_history() no implementado todavia.")

    async def add_message(self, conversation_id: str, message: ConversationMessage):
        raise NotImplementedError("MemoryRepository.add_message() no implementado todavia.")

    async def delete_conversation(self, conversation_id: str):
        raise NotImplementedError("MemoryRepository.delete_conversation() no implementado todavia.")
