from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    npc: str = "nara"

class ChatResponse(BaseModel):
    npc  : str
    reply: str