from fastapi import FastAPI
from api.routes.chat import router as chat_router
from api.routes.health import router as health_router
from api.routes.admin import router as admin_router

app = FastAPI(title="Npixie RAG API")

app.include_router(chat_router)
app.include_router(health_router)
app.include_router(admin_router)

@app.on_event("startup")
async def startup():
    from rag.embedder import get_model
    from rag.generator import get_client
    get_model()
    get_client()
    print("Npixie API ready!")