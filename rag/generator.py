import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

_client: Groq | None = None

def get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        print("Groq client ready!")
    return _client

def generate(query: str, chunks: list[str], npc_prompt: str) -> str:
    """Generate a response from Groq given query, context chunks, and NPC prompt."""
    context = "\n\n".join(chunks)

    response = get_client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": npc_prompt},
            {
                "role": "user",
                "content": f"""Use the following lore to answer the question.

--- LORE ---
{context}
--- END LORE ---

Question: {query}"""
            }
        ],
        max_tokens=256,
        temperature=0.7,
    )

    return response.choices[0].message.content