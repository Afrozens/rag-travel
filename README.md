# RAG-Travel

> Asistente de viajes inteligente basado en **RAG (Retrieval-Augmented Generation)** con respuestas en streaming. Responde **únicamente con base en datos reales** de viajes disponibles y el historial de compras del usuario autenticado.

---

## 1. Visión General

Sistema RAG para asesoramiento de viajes personalizado. Un usuario autenticado interactúa con un chatbot que, en lugar de alucinar, responde **estrictamente con base en datos reales** de viajes disponibles e historial de compras del usuario.

### Flujo de Usuario Clave

1. Usuario autenticado ve el botón **"Ver viajes de este mes"**.
2. Al interactuar, el frontend envía el mensaje al backend.
3. El backend:
   - Recupera viajes del mes desde la base vectorial (pgvector).
   - Recupera el historial de compras del usuario desde los datos ingestados.
   - Construye un contexto enriquecido y se lo pasa al LLM (Google Gemini).
   - El LLM responde de forma natural, **evitando recomendar viajes que el usuario ya compró**.
4. El usuario puede hacer preguntas de seguimiento de forma conversacional.
5. Las respuestas llegan en **streaming** (efecto máquina de escribir).

---

## 2. Arquitectura Basada en Proyectos de Referencia

De `search-api` e `ingestion-api` se adoptan los siguientes patrones probados:

| Patrón | Descripción | Aplicación en RAG-Travel |
|--------|-------------|--------------------------|
| **Lifespans** | `AsyncExitStack` para inicializar DB, vector store, servicios de AI en orden. | Inicializar pgvector, Redis, Jina client, Gemini client. |
| **Dependency Injection** | FastAPI `Depends()` para inyectar servicios y repositorios. | Inyectar `ChatService`, `EmbeddingService`, `TripRepository`. |
| **Repository Pattern** | Capa de abstracción para acceso a datos. | `TripRepository`, `PurchaseRepository`. |
| **Service Layer** | Lógica de negocio desacoplada de HTTP. | `ChatService` (orquesta RAG), `IngestService` (pipeline de embeddings). |
| **Hybrid Search** | Búsqueda vectorial + keyword fusionada con RRF. | Búsqueda semántica de viajes + filtros por fecha/agencia. |
| **StandardResponseDto** | Wrapper uniforme de respuestas API. | `StandardResponseDto[ChatResponse]`. |

---

## 3. Stack Tecnológico

| Capa | Tecnología | Justificación |
|------|-----------|---------------|
| **Framework** | FastAPI | Async nativo, DI robusto, auto-docs. |
| **Embeddings** | `jina-embeddings-v4` | 3.8B params, **2048 dims**, multimodal y multilingüe. Ideal para texto de viajes. |
| **Vector DB** | PostgreSQL + `pgvector` | Permite filtros metadata + vector search en una sola query. |
| **LLM** | Google Gemini (AI Studio) | API simple con key, streaming nativo, multilingüe. |
| **Chat History** | Redis | TTL nativo para auto-cleanup por inactividad, in-memory speed. |
| **Auth** | JWT Bearer (OAuth2) | Extrae `user_id` del token. |
| **Async HTTP** | `httpx` | Cliente async para Jina API. |
| **Streaming** | SSE (Server-Sent Events) | Efecto máquina de escribir para respuestas del LLM. |

---

## 4. Estructura de Módulos FastAPI

Cada módulo sigue la estructura: **`constants.py`, `router.py`, `schema.py`, `controller.py`, `service.py`**.

```
rag_travel/
├── __main__.py                  # Entry point: uvicorn bootstrap
├── main.py                      # FastAPI app + lifespan orchestration
├── router.py                    # Aggregator: include_router(chat, ingest, search)
├── core/
│   ├── config.py                # Pydantic BaseSettings (.env)
│   ├── dependencies.py          # DI comunes: DB session, HTTP clients, Redis
│   ├── lifespan.py              # AsyncExitStack: init pgvector, Redis, Jina, Gemini
│   └── guards/
│       └── auth.py              # JWT dependency: get_current_user()
│
├── chat/                        # ⭐ Módulo principal: Chat RAG
│   ├── constants.py             # System prompts, RAG config, max tokens
│   ├── router.py                # POST /chat, POST /chat/stream
│   ├── schema.py                # ChatRequest, ChatResponse, MessageRole, StreamChunk
│   ├── controller.py            # HTTP layer: auth, validate, delegate
│   └── service.py               # Orchestración del pipeline RAG completo + streaming
│
├── ingest/                      # 📥 Ingesta de datos
│   ├── constants.py             # Batch size, chunking config
│   ├── router.py                # POST /ingest/trips, POST /ingest/purchases
│   ├── schema.py                # TripIngestRequest, PurchaseIngestRequest
│   ├── controller.py            # Validación auth/API key
│   └── service.py               # Pipeline: chunk → embed (Jina) → store (pgvector)
│
├── search/                      # 🔍 Búsqueda vectorial
│   ├── constants.py             # Top-k, similarity threshold
│   ├── router.py                # POST /search/trips (debug)
│   ├── schema.py                # SearchRequest, SearchResponse, SearchFilter
│   ├── controller.py            # HTTP layer
│   └── service.py               # Vector search con metadata filters
│
├── embeddings/                  # 🧠 Cliente Jina Embeddings v4
│   ├── constants.py             # Model name, dimensions (2048), base URL
│   ├── schema.py                # EmbedRequest, EmbedResponse
│   └── service.py               # Async client para api.jina.ai/v1/embeddings
│
├── llm/                         # 🤖 Cliente Google Gemini
│   ├── constants.py             # Model name, temperature, max tokens
│   ├── schema.py                # LLMRequest, LLMResponse, StreamChunk
│   └── service.py               # Async client para Gemini con streaming SSE
│
├── memory/                      # 💬 Memoria de conversación (Redis)
│   ├── constants.py             # TTL default (3600s), max messages
│   ├── schema.py                # ConversationMessage, ConversationHistory
│   ├── repository.py            # RedisConversationRepository: get, add, delete
│   └── service.py               # ConversationService: gestión de sesiones
│
└── shared/
    ├── schemas.py               # StandardResponseDto, Pagination
    └── exceptions.py            # Custom exceptions: ChatError, IngestError, etc.
```

---

## 5. Flujo de Datos Detallado

### 5.1 Ingesta de Viajes y Compras

```
[Admin/API] → POST /ingest/trips (JSON)
    ↓
[IngestController] valida auth/admin
    ↓
[IngestService] Pipeline:
    1. Valida schema del JSON de viajes
    2. Chunking: Divide descripciones largas en chunks semánticos
    3. Embedding: Llama a JinaEmbeddingService.embed_text()
       - Model: jina-embeddings-v4
       - Task: retrieval.passage
       - Output: 2048-dim vectors
    4. Storage:
       - PostgreSQL: upsert tabla `trips` (datos estructurados)
       - pgvector: upsert tabla `trip_embeddings` (id, trip_id, embedding, content, metadata)
    5. Retorna count ingestado

[Admin/API] → POST /ingest/purchases (JSON)
    ↓
    1. Valida schema del JSON de compras
    2. Upsert en PostgreSQL tabla `purchases` (user_id, trip_id, trip_title, purchased_at)
    3. NO genera embeddings (datos estructurados puros)
```

### 5.2 Chat RAG con Streaming

```
[Frontend] → POST /chat/stream { message: "Ver viajes de este mes", user_id: "jwt-sub" }
    ↓
[ChatController] extrae user_id del JWT
    ↓
[ChatService] RAG Pipeline:
    1. Intent & Date Parsing:
       - "este mes" → filtro dinámico: start_date BETWEEN 2024-07-01 AND 2024-07-31
    
    2. Retrieval (Parallel):
       a. Vector Search:
          - Embed query con Jina (task: retrieval.query)
          - Query pgvector: similarity search + filtro de fechas
          - Top-k = 10
       b. User Context:
          - Query PostgreSQL: SELECT * FROM purchases WHERE user_id = ?
       c. Chat History:
          - Query Redis: LRANGE chat:conv:{conversation_id} 0 19
    
    3. Augmentation:
       - Construye prompt con:
         • System prompt (chat/constants.py): "Eres un asesor de viajes..."
         • Contexto: Lista de viajes disponibles (con fechas, precio, agencia)
         • Restricción: "El usuario ya compró: [París 2023, Roma 2024]. NO recomiendes estos."
         • Historial de chat reciente desde Redis
         • User message actual
    
    4. Generation (Streaming):
       - Llama a Gemini con streaming (SSE)
       - Cada chunk del LLM se envía inmediatamente al frontend
       - Se guarda la respuesta completa en Redis al finalizar
    
    5. Response:
       - Stream finaliza con evento especial: { done: true, referenced_trips: [...] }
```

---

## 6. Esquema de Datos de Ejemplo (JSON de Viajes)

El formato que recibirá el endpoint de ingestión:

```json
{
  "trips": [
    {
      "id": "trip-001",
      "title": "Escapada a París",
      "destination": "París, Francia",
      "agency": "Viajes EuroStar",
      "start_date": "2024-07-15",
      "end_date": "2024-07-20",
      "price": 1200.00,
      "currency": "EUR",
      "description": "Tour guiado por la Torre Eiffel, Museo del Louvre y paseo por el Sena...",
      "category": "cultural",
      "tags": ["romántico", "europa", "verano", "parejas"]
    },
    {
      "id": "trip-002",
      "title": "Aventura en Costa Rica",
      "destination": "San José, Costa Rica",
      "agency": "EcoTravel CR",
      "start_date": "2024-07-08",
      "end_date": "2024-07-14",
      "price": 950.00,
      "currency": "USD",
      "description": "Volcanes, playas y selva tropical con guías expertos...",
      "category": "aventura",
      "tags": ["naturaleza", "américa", "familia"]
    }
  ]
}
```

Y el historial de compras del usuario:

```json
{
  "purchases": [
    {
      "user_id": "user-123",
      "trip_id": "trip-099",
      "trip_title": "Roma Histórica",
      "purchased_at": "2024-03-10",
      "destination": "Roma, Italia"
    }
  ]
}
```

---

## 7. Componentes Clave en Detalle

### 7.1 Jina Embeddings v4 (`embeddings/service.py`)

```python
class JinaEmbeddingService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.jina.ai/v1/embeddings"
        self.model = "jina-embeddings-v4"  # 3.8B params, 2048 dims
        self.dimensions = 2048

    async def embed(
        self,
        texts: list[str],
        task: str = "retrieval.query"  # o "retrieval.passage"
    ) -> list[list[float]]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "input": texts,
                    "task": task,
                    "normalized": True,  # para cosine similarity
                }
            )
            return [item["embedding"] for item in response.json()["data"]]
```

**Nota**: `jina-embeddings-v4` soporta `late_chunking` y `return_multivector` para retrieval avanzado, pero para el MVP usaremos embeddings single-vector estándar.

### 7.2 Vector Search con pgvector (`search/service.py`)

Tabla en PostgreSQL:

```sql
CREATE TABLE trip_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id VARCHAR NOT NULL,
    content TEXT NOT NULL,           -- texto chunkado del viaje
    embedding VECTOR(2048),          -- pgvector
    metadata JSONB,                  -- { agency, dates, price, destination }
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índice HNSW para búsqueda rápida
CREATE INDEX ON trip_embeddings USING hnsw (embedding vector_cosine_ops);

-- Índice para filtros de fecha
CREATE INDEX idx_trip_embeddings_dates ON trip_embeddings USING gin (
    (metadata -> 'start_date'), (metadata -> 'end_date')
);
```

Query de búsqueda híbrida:

```sql
SELECT trip_id, content, metadata, 1 - (embedding <=> $query_embedding) AS similarity
FROM trip_embeddings
WHERE metadata->>'start_date' BETWEEN $month_start AND $month_end
  AND 1 - (embedding <=> $query_embedding) > $threshold
ORDER BY embedding <=> $query_embedding
LIMIT $top_k;
```

### 7.3 Google Gemini con Streaming (`llm/service.py`)

```python
import google.generativeai as genai

class GeminiService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def generate_stream(self, prompt: str, system_prompt: str = None):
        config = genai.GenerationConfig(temperature=0.7, max_output_tokens=2048)
        
        if system_prompt:
            chat = self.model.start_chat(history=[{"role": "user", "parts": [system_prompt]}])
        else:
            chat = self.model.start_chat()
        
        response = chat.send_message(prompt, stream=True, generation_config=config)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
```

### 7.4 Redis Chat History (`memory/repository.py`)

```python
import redis.asyncio as redis
import json

class RedisConversationRepository:
    def __init__(self, redis_client: redis.Redis, ttl: int = 3600):
        self.redis = redis_client
        self.ttl = ttl

    async def get_history(self, conversation_id: str, limit: int = 20) -> list[dict]:
        key = f"chat:conv:{conversation_id}"
        messages = await self.redis.lrange(key, 0, limit - 1)
        return [json.loads(m) for m in messages]

    async def add_message(self, conversation_id: str, role: str, content: str):
        key = f"chat:conv:{conversation_id}"
        message = json.dumps({"role": role, "content": content, "timestamp": time.time()})
        await self.redis.lpush(key, message)
        await self.redis.expire(key, self.ttl)

    async def delete_conversation(self, conversation_id: str):
        await self.redis.delete(f"chat:conv:{conversation_id}")
```

### 7.5 Prompt del Sistema (`chat/constants.py`)

```python
SYSTEM_PROMPT = """Eres un asesor de viajes experto y amigable.

Reglas:
1. Responde ÚNICAMENTE con base en los viajes disponibles proporcionados en el contexto.
2. NO recomiendes viajes que el usuario ya haya comprado (se indican explícitamente).
3. Si el usuario pregunta por "este mes", filtra por las fechas del contexto.
4. Sé conversacional, natural y entusiasta.
5. Si no hay viajes disponibles, dilo honestamente.
6. Mantén el contexto de la conversación previa para respuestas coherentes.

Contexto de viajes disponibles:
{available_trips}

Viajes ya comprados por el usuario (NO recomendar):
{purchased_trips}

Historial reciente de la conversación:
{chat_history}
"""

RAG_TOP_K = 10
RAG_SIMILARITY_THRESHOLD = 0.75
CHAT_MAX_HISTORY = 20
STREAM_DELIMITER = "\n\n"
```

---

## 8. Configuración de Entorno (.env)

```bash
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true
RELOAD=true

# PostgreSQL (relacional + vectorial)
DB_HOST=localhost
DB_PORT=5432
DB_USER=rag_travel
DB_PASSWORD=secret
DB_NAME=rag_travel

# Redis (chat history)
REDIS_URL=redis://localhost:6379/0
REDIS_CHAT_TTL=3600
REDIS_CHAT_MAX_MESSAGES=20

# Jina AI
JINA_API_KEY=jina_xxxxxxxx
JINA_EMBEDDING_MODEL=jina-embeddings-v4
JINA_EMBEDDING_DIMENSIONS=2048

# Google Gemini (AI Studio)
GEMINI_API_KEY=AIxxxxxxxx
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_OUTPUT_TOKENS=2048

# Auth
JWT_SECRET=super-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# RAG Config
RAG_TOP_K=10
RAG_SIMILARITY_THRESHOLD=0.75
```

---

## 9. Endpoints API Principales

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `POST` | `/v1/chat` | Enviar mensaje al chatbot RAG (respuesta completa) | JWT |
| `POST` | `/v1/chat/stream` | Chat con respuesta en **streaming** (SSE) | JWT |
| `POST` | `/v1/ingest/trips` | Ingestar catálogo de viajes | Admin/API Key |
| `POST` | `/v1/ingest/purchases` | Ingestar compras de usuarios | Admin/API Key |
| `POST` | `/v1/search/trips` | Búsqueda vectorial debug | JWT |
| `GET`  | `/health` | Health check (DB + Redis + servicios) | None |

### Ejemplo de llamada al chat streaming

```bash
curl -N -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -X POST http://localhost:8000/v1/chat/stream \
  -d '{
    "message": "Ver viajes de este mes",
    "conversation_id": "conv-uuid-123"
  }'
```

Response (SSE):
```
data: {"chunk": "¡Hola! Este mes tenemos", "done": false}

data: {"chunk": " varias opciones interesantes", "done": false}

data: {"chunk": ". Te recomiendo 'Escapada a París'", "done": false}

data: {"chunk": " del 15-20 julio por €1,200.", "done": false}

data: {"chunk": "", "done": true, "referenced_trips": ["trip-001"]}
```

---

## 10. Roadmap de Implementación

### Fase 1: Infraestructura Base
- [ ] Setup FastAPI con lifespan (`AsyncExitStack`) y DI.
- [ ] Configuración Pydantic BaseSettings (`core/config.py`).
- [ ] Conexión PostgreSQL + pgvector.
- [ ] Conexión Redis.
- [ ] Guards JWT básico (`core/guards/auth.py`).

### Fase 2: Embeddings & Ingesta
- [ ] Módulo `embeddings` con Jina v4 client.
- [ ] Módulo `ingest` con pipeline completo:
  - Chunking de descripciones.
  - Generación de embeddings.
  - Upsert a PostgreSQL + pgvector.
- [ ] Endpoints `POST /ingest/trips` y `POST /ingest/purchases`.

### Fase 3: Chat RAG
- [ ] Módulo `search` con vector search + metadata filters.
- [ ] Módulo `llm` con Gemini client y streaming.
- [ ] Módulo `memory` con Redis chat history.
- [ ] Módulo `chat` con orquestación RAG completa:
  - Date parsing ("este mes" → filtros dinámicos).
  - Parallel retrieval (vector search + purchases + history).
  - Prompt augmentation.
  - Streaming response.
- [ ] Endpoints `POST /chat` y `POST /chat/stream`.

### Fase 4: Testing & Optimización
- [ ] Tests unitarios de services.
- [ ] Tests de integración de endpoints.
- [ ] Benchmark de latencia de búsqueda vectorial.
- [ ] Ajuste de thresholds y top-k.

---

## 11. Consideraciones de Diseño

1. **Datos externos**: Los datos de viajes y compras se reciben vía JSON en endpoints POST. En el futuro se migrará a consumir el otro server vía HTTP client.
2. **Auto-cleanup**: Redis maneja TTL automático por conversación. Si no hay actividad en 1 hora, la sesión se pierde (comportamiento deseado).
3. **Streaming**: El frontend debe manejar SSE correctamente. El backend cierra el stream cuando el LLM termina o cuando hay error.
4. **Idempotencia**: Los endpoints de ingestión deben ser idempotentes (upsert por `trip_id` y `purchase_id`).
5. **Seguridad**: El system prompt nunca se expone al frontend. La lógica de exclusión de comprados es server-side.

---

**Versión del plan**: 1.0
**Última actualización**: 2024-07
