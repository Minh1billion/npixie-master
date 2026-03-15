import os
import yaml
from dotenv import load_dotenv
from rag.retriever import retrieve
from rag.generator import generate

load_dotenv()

DEFAULT_NPC = os.getenv("DEFAULT_NPC", "nara")
NPCS_DIR    = "./data/lore/npcs"

def load_npc(npc_id: str) -> dict:
    """Load NPC from yaml file"""
    path = os.path.join(NPCS_DIR, f"{npc_id}.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    
def chat(query: str, npc_id: str = None) -> dict:
    """Chat with NPC"""
    # Load NPC
    npc = load_npc(npc_id or DEFAULT_NPC)
    
    # Retrieve chunks
    chunks = retrieve(query)
    
    # Generate answer
    answer = generate(query, chunks, npc["system_prompt"])
    
    return {
        "npc" : npc["name"],
        "reply": answer
    }
    
if __name__ == "__main__":
    import time

    question = "Who is Nara?"

    t0     = time.time()
    result = chat(question)
    t1     = time.time()

    print(f"🌙 {result['npc']}:")
    print(result["reply"])
    print(f"\n⏱️  Total: {t1 - t0:.2f}s")
    