import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

_model: SentenceTransformer | None = None

def get_embedding_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
        print("Embedding model ready!")
    return _model

def embed(text: str) -> list[float]:
    return get_embedding_model().encode(text).tolist()