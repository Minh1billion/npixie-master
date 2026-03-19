import os
from dotenv import load_dotenv
from sentence_transformers import CrossEncoder

load_dotenv()

RERANKER_MODEL = os.getenv("RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
RERANKER_TOP_K = int(os.getenv("RERANKER_TOP_K", 3))

_model: CrossEncoder | None = None


def get_reranker_model() -> CrossEncoder:
    global _model
    if _model is None:
        print(f"Loading reranker model: {RERANKER_MODEL}")
        _model = CrossEncoder(RERANKER_MODEL)
        print("Reranker model ready!")
    return _model


def rerank(query: str, chunks: list[str], top_k: int = RERANKER_TOP_K) -> list[str]:
    if not chunks:
        return []

    model = get_reranker_model()
    pairs = [(query, chunk) for chunk in chunks]
    scores = model.predict(pairs)
    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)

    return [chunk for _, chunk in ranked[:top_k]]