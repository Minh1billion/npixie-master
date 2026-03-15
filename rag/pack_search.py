from rag.supabase_client import get_supabase

# Map NPC domain - categories
NPC_CATEGORY_MAP = {
    "nara"  : [],  # all categories
    "zolt"  : ["combat", "weapons", "projectiles", "platformer", "enemies"],
    "lyra"  : ["tilesets", "terrain", "nature", "backgrounds", "buildings", "ruins"],
    "vexis" : ["ui-elements", "icons", "spells", "effects", "fonts"],
    "echo"  : ["music", "sfx", "ambient"],
}

def search_packs(query: str, npc_id: str, limit: int = 3) -> list[dict]:
    """Search asset packs from Supabase filtered by NPC domain."""
    sb = get_supabase()

    # Get category slugs for this NPC
    category_slugs = NPC_CATEGORY_MAP.get(npc_id, [])

    # Get category IDs from slugs
    if category_slugs:
        cat_response = sb.table("categories") \
            .select("id, slug") \
            .in_("slug", category_slugs) \
            .execute()
        category_ids = [c["id"] for c in cat_response.data]
    else:
        category_ids = []

    # Search packs by name matching query
    pack_query = sb.table("asset_pack") \
        .select("id, name, description, price, image_url") \
        .ilike("name", f"%{query}%") \
        .is_("deleted_at", "null") \
        .limit(limit)

    packs = pack_query.execute().data

    # If no name match, fallback to category filter
    if not packs and category_ids:
        # Get pack IDs via sprites - categories
        sprite_cats = sb.table("sprite_categories") \
            .select("sprite_id") \
            .in_("category_id", category_ids) \
            .execute()

        sprite_ids = [s["sprite_id"] for s in sprite_cats.data]

        if sprite_ids:
            pack_sprites = sb.table("asset_pack_sprites") \
                .select("asset_pack_id") \
                .in_("sprite_id", sprite_ids) \
                .execute()

            pack_ids = list(set([p["asset_pack_id"] for p in pack_sprites.data]))

            if pack_ids:
                packs = sb.table("asset_pack") \
                    .select("id, name, description, price, image_url") \
                    .in_("id", pack_ids) \
                    .is_("deleted_at", "null") \
                    .limit(limit) \
                    .execute().data

    return packs


def format_packs_for_prompt(packs: list[dict]) -> str:
    """Format pack list into string for LLM context."""
    if not packs:
            return "IMPORTANT: There are currently NO asset packs available in the marketplace. Do NOT recommend or mention any specific pack names. Only speak generally about what kinds of assets would help, and invite the user to check back later."

    lines = ["Here are some relevant asset packs from the Pixelara marketplace:\n"]
    for p in packs:
        price = f"${p['price']}" if p.get("price") else "Free"
        desc  = p.get("description") or "No description available."
        lines.append(f"- **{p['name']}** ({price}): {desc}")

    return "\n".join(lines)