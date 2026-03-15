# 🧚 Npixie — RAG Bot for Pixelara

Npixie is a RAG-powered chatbot for **Pixelara** — a fantasy marketplace where game developers find asset packs. The bot speaks through NPC characters rooted in the world's lore, powered by **Groq API** and **Qdrant**.

---

## 🗂️ Project Structure

```
npixie-master/
├── scripts/
│   ├── download_model.py    # Download embedding model from HuggingFace
│   └── ingest.py            # Embed lore into Qdrant
├── data/
│   └── lore/
│       ├── LORE.md          # World lore (Pixelara, Fae, Bazaar)
│       └── npcs/
│           └── nara.yaml    # Default NPC — Nara the Lorekeeper
├── rag/
│   ├── embedder.py          # Singleton embedding model
│   ├── retriever.py         # Query Qdrant for relevant chunks
│   ├── generator.py         # Generate answer via Groq API
│   └── pipeline.py          # Full RAG pipeline
├── api/
│   ├── main.py              # FastAPI entrypoint
│   ├── schemas.py           # Request/Response models
│   └── routes/
│       ├── chat.py          # POST /chat
│       └── health.py        # GET /health
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

Fill in your `GROQ_API_KEY`.

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

---

## 🧪 Testing the API

Swagger UI:
```
http://localhost:8000/docs
```

curl:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the Grand Bazaar?", "npc": "nara"}'
```

Response:
```json
{
  "npc": "Nara",
  "reply": "The Grand Bazaar is the beating heart of Pixelara..."
}
```

---

## 🧚 NPC System

Each NPC is a `.yaml` file in `data/lore/npcs/`. The default NPC is **Nara — The Lorekeeper**.

| NPC | Personality | Domain |
|---|---|---|
| `nara` | Wise, poetic narrator | Lore, guidance, general |
| `zolt` | Blunt, energetic warrior | Combat, action, platformer |
| `lyra` | Calm, nature-loving artist | Environments, tilesets |
| `vexis` | Precise, arcane archivist | UI, icons, magic effects |
| `echo` | Dreamy sound weaver | Music, SFX, audio |

To add a new NPC, create `data/lore/npcs/[name].yaml` following the `nara.yaml` template.

---

## 📦 Tech Stack

| Layer | Tech |
|---|---|
| LLM | Groq API (llama-3.1-8b-instant) |
| Vector DB | Qdrant |
| Embedding | sentence-transformers/all-MiniLM-L6-v2 |
| API | FastAPI |
| Container | Docker + Docker Compose |