from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.logging import get_logger

from api.routes.chat import router as chat_router
from api.routes.health import router as health_router
from api.routes.admin import router as admin_router
from api.routes.specxel import router as specxel_router

logger = get_logger("api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    from rag.embedder import get_embedding_model
    from rag.reranker import get_reranker_model
    from rag.generator import get_client
    from rag.supabase_client import get_supabase
    from specxel.pipeline import get_classify_model
    get_embedding_model()
    get_reranker_model()
    get_client()
    get_supabase()
    get_classify_model()
    logger.info("Npixie API ready!")

    yield

    logger.info("Npixie API shutting down...")

app = FastAPI(title="Npixie RAG API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(health_router)
app.include_router(admin_router)
app.include_router(specxel_router)