from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    npc: str = "nara"

class ChatResponse(BaseModel):
    npc  : str
    reply: str
    
class NPCPayload(BaseModel):
    id        : str
    name      : str
    title     : str
    domain    : list[str]
    personality: str
    voice_style: str
    greeting  : str
    system_prompt: str