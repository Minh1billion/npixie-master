import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from rag.embedder import embed

load_dotenv()

QDRANT_HOST     = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT     = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "npixie_lore")
TOP_K           = int(os.getenv("TOP_K", 3))

_client: QdrantClient | None = None

def get_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    return _client

def retrieve(query: str) -> list[str]:
    """Find the most relevant chunks for a given query."""
    query_vector = embed(query)

    response = get_client().query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=TOP_K,
    )

    return [hit.payload["text"] for hit in response.points]


if __name__ == "__main__":
    question = "What is the Grand Bazaar?"
    chunks = retrieve(question)

    print(f"🔍 Query: {question}\n")
    for i, chunk in enumerate(chunks):
        print(f"── Chunk {i+1} ──────────────────")
        print(chunk)
        print()