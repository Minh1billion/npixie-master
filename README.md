# 🧚 Npixie — RAG Bot for Pixelara

Npixie is a RAG-powered chatbot for **Pixelara** — a fantasy marketplace where game developers find asset packs. The bot speaks through NPC characters rooted in the world's lore, powered by **Groq API** and **Qdrant**.

---

## 🗂️ Project Structure

```
npixie-master/
├── scripts/
│   ├── sql/
│   │   ├── category_seed.sql      # Seed categories
│   │   └── sprite_and_pack_seed.sql  # Seed sprites + asset packs
│   ├── download_model.py          # Download embedding model
│   └── ingest.py                  # Embed lore into Qdrant
├── data/
│   └── lore/
│       ├── LORE.md                # World lore (Pixelara, Fae, Bazaar)
│       └── npcs/
│           ├── nara.yaml          # Lorekeeper (default)
│           ├── zolt.yaml          # Combat specialist
│           ├── lyra.yaml          # Environment specialist
│           ├── vexis.yaml         # UI/Magic specialist
│           └── echo.yaml          # Audio specialist
├── rag/
│   ├── embedder.py                # Singleton embedding model
│   ├── retriever.py               # Query Qdrant for relevant chunks
│   ├── generator.py               # Generate answer via Groq API
│   ├── pipeline.py                # Full RAG pipeline + NPC auto-detect
│   ├── pack_search.py             # Query Supabase for asset packs
│   └── supabase_client.py         # Supabase singleton client
├── api/
│   ├── main.py                    # FastAPI entrypoint
│   ├── schemas.py                 # Request/Response models
│   └── routes/
│       ├── chat.py                # POST /chat
│       ├── health.py              # GET /health
│       └── admin.py               # Admin CRUD endpoints
├── docker/
│   └── Dockerfile.api
├── docker-compose.yml
├── requirements.txt
└── .env
```

---

## ⚙️ Setup

### 1. Clone & create virtual environment

```bash
git clone https://github.com/yourname/npixie-master.git
cd npixie-master
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env` file

```bash
cp .env.example .env
```

Fill in the required values:

```env
# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=npixie_lore

# Embedding
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Groq
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# RAG
DEFAULT_NPC=nara
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K=3
```

---

## 🗄️ Database Setup (Supabase)

### Step 1 — Create a test user

Run this SQL in the **Supabase SQL Editor**:

```sql
-- Create a test user for seeding
INSERT INTO users (
  id,
  full_name,
  username,
  email,
  password,
  role,
  is_active,
  is_verified,
  created_at,
  updated_at
) VALUES (
  'b61d3ee9-1799-4378-8746-2b5204db711d',
  'Npixie Seed User',
  'npixie_seed',
  'seed@npixie.dev',
  '$2a$10$dummyhashedpasswordforseeding000000000000000',
  'ADMIN',
  true,
  true,
  now(),
  now()
) ON CONFLICT (id) DO NOTHING;
```

### Step 2 — Seed categories

Run `scripts/sql/category_seed.sql` in the Supabase SQL Editor.

This creates 34 categories covering all game asset types:
- Environment: Tilesets, Terrain, Backgrounds, Dungeon, Buildings, Ruins, Nature
- Characters: Characters, Enemies, Animals, Dragons, Undead, Vehicles
- Combat: Combat, Weapons, Projectiles
- Fantasy: Fantasy, Spells, Potions, Effects
- Props: Props, Icons
- UI: UI Elements, Fonts, Animations, Cutscenes
- Audio: Music, SFX, Ambient
- Genres: RPG, Platformer, Top-down, Side-scroller, Asset Packs

### Step 3 — Seed sprites and asset packs

Run `scripts/sql/sprite_and_pack_seed.sql` in the Supabase SQL Editor.

This creates 20 sprites and 4 NPC-themed asset packs:

| Pack | NPC | Contents |
|---|---|---|
| Zolt's Combat Arsenal | Zolt | Warriors, axes, projectiles, orc enemies, platformer heroes |
| Lyra's World Builder | Lyra | Forest tilesets, terrain, backgrounds, ruins, castles |
| Vexis Arcane UI Tome | Vexis | HUD frames, spell icons, effects, pixel fonts, portals |
| Echo's Audio Sanctum | Echo | Battle music, dungeon ambience, combat SFX, spell sounds |

---

## 🚀 Running the project

### Option A — Local

**Step 1 — Start Qdrant**
```bash
docker run -d -p 6333:6333 qdrant/qdrant
```

**Step 2 — Embed lore into Qdrant**
```bash
python scripts/ingest.py
```

**Step 3 — Start API**
```bash
uvicorn api.main:app --reload
```

### Option B — Docker Compose

```bash
docker-compose up --build
```

> ⚠️ After first run with Docker Compose, run ingest manually:
> ```bash
> python scripts/ingest.py
> ```

---

## 🧪 Testing the API

Swagger UI:
```
http://localhost:8000/docs
```

### Test NPC auto-detection

Each message is automatically routed to the most relevant NPC based on keywords:

```bash
# Zolt — combat keywords
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need combat sprites for my action game"}'

# Lyra — environment keywords
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to build a forest world with nice backgrounds"}'

# Vexis — UI/magic keywords
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need a UI kit with spell icons for my RPG"}'

# Echo — audio keywords
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Looking for battle music and ambient sounds"}'

# Nara — general / lore
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Pixelara"}'
```

### Force a specific NPC

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What packs do you recommend?", "npc": "zolt"}'
```

Response:
```json
{
  "npc": "Zolt",
  "reply": "Strong packs don't ask for permission...",
  "packs": [
    {
      "id": "...",
      "name": "Zolt's Combat Arsenal",
      "description": "The ultimate combat pack...",
      "price": 12.99,
      "image_url": "https://..."
    }
  ]
}
```

---

## 🧚 NPC System

Each NPC is a `.yaml` file in `data/lore/npcs/`. The default NPC is **Nara — The Lorekeeper**.

| NPC | Personality | Domain | Keywords |
|---|---|---|---|
| `nara` | Wise, poetic narrator | Lore, guidance, general | _(default)_ |
| `zolt` | Blunt, energetic warrior | Combat, action, platformer | combat, weapon, fight, enemy |
| `lyra` | Calm, nature-loving artist | Environments, tilesets | environment, nature, tileset, forest |
| `vexis` | Precise, arcane archivist | UI, icons, magic effects | ui, icon, spell, effect, magic |
| `echo` | Dreamy sound weaver | Music, SFX, audio | music, sound, audio, sfx, ambient |

To add a new NPC, create `data/lore/npcs/[name].yaml` following the `nara.yaml` template and add its keywords to `KEYWORD_NPC_MAP` in `rag/pipeline.py`.

---

## 📦 Tech Stack

| Layer | Tech |
|---|---|
| LLM | Groq API (llama-3.1-8b-instant) |
| Vector DB | Qdrant |
| Embedding | sentence-transformers/all-MiniLM-L6-v2 |
| Marketplace DB | Supabase (PostgreSQL) |
| API | FastAPI |
| Container | Docker + Docker Compose |