from fastapi import APIRouter
from api.schemas import ChatRequest, ChatResponse
from rag.pipeline import chat

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    result = chat(query=req.message, npc_id=req.npc)
    return ChatResponse(npc=result["npc"], reply=result["reply"], packs=result["packs"])