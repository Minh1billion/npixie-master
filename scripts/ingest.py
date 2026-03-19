import os
import sys
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.embedder import embed, get_model

load_dotenv()

QDRANT_HOST     = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT     = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "npixie_lore")
CHUNK_SIZE      = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP   = int(os.getenv("CHUNK_OVERLAP", 50))
LORE_FILE       = "./data/lore/LORE.md"

print("📖 Loading lore file...")
with open(LORE_FILE, "r", encoding="utf-8") as f:
    text = f.read()

def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks

chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

print("🔢 Embedding chunks...")
get_model()
vectors = [embed(chunk) for chunk in chunks]

print("💾 Saving to Qdrant...")
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=len(vectors[0]),
        distance=Distance.COSINE
    ),
)

points = [
    PointStruct(
        id=str(uuid.uuid4()),
        vector=vectors[i],
        payload={"text": chunks[i], "source": "LORE.md"}
    )
    for i in range(len(chunks))
]

client.upsert(collection_name=COLLECTION_NAME, points=points)
print(f"✅ Done! {len(points)} chunks saved to '{COLLECTION_NAME}'")