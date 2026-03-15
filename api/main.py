from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.chat import router as chat_router
from api.routes.health import router as health_router
from api.routes.admin import router as admin_router

app = FastAPI(title="Npixie RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(health_router)
app.include_router(admin_router)

@app.on_event("startup")
async def startup():
    from rag.embedder import get_model
    from rag.generator import get_client
    from rag.supabase_client import get_supabase
    get_model()
    get_client()
    get_supabase()
    print("Npixie API ready!")