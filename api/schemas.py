from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    npc    : str | None = None

class ChatResponse(BaseModel):
    npc  : str
    reply: str
    packs: list[dict] = []

class NPCPayload(BaseModel):
    id           : str
    name         : str
    title        : str
    domain       : list[str]
    personality  : str
    voice_style  : str
    greeting     : str
    system_prompt: str
    
class ClassifyRequest(BaseModel):
    image_url: str
    sprite_id: str

class ClassifyResponse(BaseModel):
    sprite_id: str
    is_pixelart: bool
    confidence: float