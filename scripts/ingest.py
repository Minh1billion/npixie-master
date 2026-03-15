import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = os.getenv("QDRANT_PORT", 6333)
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "npixie_lore")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
LORE_FILE = os.getenv("LORE_FILE", "data/lore/LORE.md")

# Load Lore
print("LORE LOADING...")
with open(LORE_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Chunking text from Lore
def chunk_text(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

print("CHUNKING LORE...")
chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
print(f"    LORE CHUNKED INTO {len(chunks)} CHUNKS")

# Embedding chunks
print("EMBEDDING CHUNKS...")
model = SentenceTransformer(EMBEDDING_MODEL)
vectors = model.encode(chunks, show_progress_bar=True)

# Save to qdrant
print("SAVING TO QDRANT...")
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Create collection if it doesn't exist
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=vectors.shape[1], distance=Distance.COSINE),
)

# Upload points
points = [
    PointStruct(
        id=str(uuid.uuid4()),
        vector=vectors[i].tolist(),
        payload={"text": chunks[i], "source": "LORE.md"},
    )
    for i in range(len(chunks))
]

client.upsert(collection_name=COLLECTION_NAME, points=points)
print(f"    {len(chunks)} CHUNKS UPLOADED TO QDRANT")

print("INGEST COMPLETE")