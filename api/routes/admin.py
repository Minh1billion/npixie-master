import os
import yaml
import shutil
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from api.schemas import NPCPayload

router = APIRouter(prefix="/admin")

NPCS_DIR  = "./data/lore/npcs"
LORE_DIR  = "./data/lore"

# NPC endpoints 

@router.get("/npcs")
def list_npcs():
    """List all NPCs."""
    files = [f.replace(".yaml", "") for f in os.listdir(NPCS_DIR) if f.endswith(".yaml")]
    return {"npcs": files}

@router.get("/npcs/{npc_id}")
def get_npc(npc_id: str):
    """Get a single NPC by id."""
    path = os.path.join(NPCS_DIR, f"{npc_id}.yaml")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"NPC '{npc_id}' not found")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@router.post("/npcs")
def create_npc(npc: NPCPayload):
    """Create a new NPC."""
    path = os.path.join(NPCS_DIR, f"{npc.id}.yaml")
    if os.path.exists(path):
        raise HTTPException(status_code=409, detail=f"NPC '{npc.id}' already exists")
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(npc.model_dump(), f, allow_unicode=True)
    return {"message": f"NPC '{npc.id}' created"}

@router.put("/npcs/{npc_id}")
def update_npc(npc_id: str, npc: NPCPayload):
    """Update an existing NPC."""
    path = os.path.join(NPCS_DIR, f"{npc_id}.yaml")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"NPC '{npc_id}' not found")
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(npc.model_dump(), f, allow_unicode=True)
    return {"message": f"NPC '{npc_id}' updated"}

@router.delete("/npcs/{npc_id}")
def delete_npc(npc_id: str):
    """Delete an NPC."""
    path = os.path.join(NPCS_DIR, f"{npc_id}.yaml")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"NPC '{npc_id}' not found")
    os.remove(path)
    return {"message": f"NPC '{npc_id}' deleted"}

# Docs endpoints

@router.get("/docs")
def list_docs():
    """List all lore documents."""
    files = [f for f in os.listdir(LORE_DIR) if f.endswith(".md")]
    return {"docs": files}

@router.post("/docs/upload")
def upload_doc(file: UploadFile = File(...)):
    """Upload a new lore document."""
    if not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Only .md files are allowed")
    path = os.path.join(LORE_DIR, file.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": f"'{file.filename}' uploaded"}

@router.delete("/docs/{filename}")
def delete_doc(filename: str):
    """Delete a lore document."""
    path = os.path.join(LORE_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"'{filename}' not found")
    os.remove(path)
    return {"message": f"'{filename}' deleted"}

# Ingest endpoint 

@router.post("/ingest")
def trigger_ingest():
    """Re-embed all lore documents into Qdrant."""
    import subprocess
    result = subprocess.run(
        ["python", "scripts/ingest.py"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr)
    return {"message": "Ingest complete", "output": result.stdout}