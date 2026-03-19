import os
import yaml
from dotenv import load_dotenv
from rag.retriever import retrieve
from rag.reranker import rerank
from rag.generator import generate
from rag.pack_search import search_packs, format_packs_for_prompt

load_dotenv()

DEFAULT_NPC    = os.getenv("DEFAULT_NPC", "nara")
NPCS_DIR       = "./data/lore/npcs"
RETRIEVE_TOP_K = int(os.getenv("TOP_K", 10))
RERANK_TOP_K   = int(os.getenv("RERANKER_TOP_K", 3))

KEYWORD_NPC_MAP = {
    "zolt"  : ["combat", "weapon", "fight", "attack", "enemy", "platformer", "action"],
    "lyra"  : ["environment", "nature", "tileset", "background", "forest", "world", "terrain"],
    "vexis" : ["ui", "icon", "spell", "effect", "interface", "magic", "hud"],
    "echo"  : ["music", "sound", "audio", "sfx", "ambient", "soundtrack"],
}

def detect_npc(query: str) -> str:
    query_lower = query.lower()
    for npc_id, keywords in KEYWORD_NPC_MAP.items():
        if any(kw in query_lower for kw in keywords):
            return npc_id
    return DEFAULT_NPC

def load_npc(npc_id: str) -> dict:
    path = os.path.join(NPCS_DIR, f"{npc_id}.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def chat(query: str, npc_id: str = None) -> dict:
    npc_id = npc_id or detect_npc(query)
    npc = load_npc(npc_id)

    chunks = retrieve(query, top_k=RETRIEVE_TOP_K)
    chunks = rerank(query, chunks, top_k=RERANK_TOP_K)

    packs = search_packs(query, npc_id)
    pack_context = format_packs_for_prompt(packs)

    full_context = "\n\n".join(chunks) + "\n\n" + pack_context

    answer = generate(query, [full_context], npc["system_prompt"])

    return {
        "npc"  : npc["name"],
        "reply": answer,
        "packs": packs,
    }

if __name__ == "__main__":
    import time
    question = "I want to build a forest world with nice backgrounds."
    t0 = time.time()
    result = chat(question)
    t1 = time.time()

    print(f"🌙 {result['npc']}:")
    print(result["reply"])
    print(f"\n📦 Packs found: {len(result['packs'])}")
    print(f"⏱️  Total: {t1 - t0:.2f}s")