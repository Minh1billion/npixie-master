from rag.supabase_client import get_supabase

NPC_CATEGORY_MAP = {
    "nara"  : [],
    "zolt"  : ["combat", "weapons", "projectiles", "platformer", "enemies"],
    "lyra"  : ["tilesets", "terrain", "nature", "backgrounds", "buildings", "ruins"],
    "vexis" : ["ui-elements", "icons", "spells", "effects", "fonts"],
    "echo"  : ["music", "sfx", "ambient"],
}

NPC_NAME_KEYWORDS = {
    "nara"  : [],
    "zolt"  : ["zolt", "combat", "warrior", "weapon", "fight"],
    "lyra"  : ["lyra", "world", "nature", "environment", "grove"],
    "vexis" : ["vexis", "arcane", "ui", "icon", "spell"],
    "echo"  : ["echo", "audio", "sound", "music", "sfx"],
}

def search_packs(query: str, npc_id: str, limit: int = 3) -> list[dict]:
    sb = get_supabase()

    category_slugs = NPC_CATEGORY_MAP.get(npc_id, [])

    if category_slugs:
        cat_response = sb.table("categories") \
            .select("id, slug") \
            .in_("slug", category_slugs) \
            .execute()
        category_ids = [c["id"] for c in cat_response.data]
    else:
        category_ids = []

    # 1. Match by pack name
    packs = sb.table("asset_pack") \
        .select("id, name, description, price, image_url") \
        .ilike("name", f"%{query}%") \
        .is_("deleted_at", None) \
        .limit(limit) \
        .execute().data

    # 2. Match by description
    if not packs:
        packs = sb.table("asset_pack") \
            .select("id, name, description, price, image_url") \
            .ilike("description", f"%{query}%") \
            .is_("deleted_at", None) \
            .limit(limit) \
            .execute().data

    # 3. Fallback: category filter via sprite_categories
    if not packs and category_ids:
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
                    .is_("deleted_at", None) \
                    .limit(limit) \
                    .execute().data

    # 4. Fallback: match by NPC name keywords in pack name
    if not packs:
        npc_keywords = NPC_NAME_KEYWORDS.get(npc_id, [])
        for keyword in npc_keywords:
            packs = sb.table("asset_pack") \
                .select("id, name, description, price, image_url") \
                .ilike("name", f"%{keyword}%") \
                .is_("deleted_at", None) \
                .limit(limit) \
                .execute().data
            if packs:
                break

    # 5. Last resort: return all non-deleted packs up to limit
    if not packs:
        packs = sb.table("asset_pack") \
            .select("id, name, description, price, image_url") \
            .is_("deleted_at", None) \
            .limit(limit) \
            .execute().data

    return packs


def format_packs_for_prompt(packs: list[dict]) -> str:
    if not packs:
        return "IMPORTANT: There are currently NO asset packs available in the marketplace. Do NOT recommend or mention any specific pack names. Only speak generally about what kinds of assets would help, and invite the user to check back later."

    lines = ["Here are some relevant asset packs from the Pixelara marketplace:\n"]
    for p in packs:
        price = f"${p['price']}" if p.get("price") else "Free"
        desc  = p.get("description") or "No description available."
        lines.append(f"- **{p['name']}** ({price}): {desc}")

    return "\n".join(lines)