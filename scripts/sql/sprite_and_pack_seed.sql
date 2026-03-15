DO $$
DECLARE
  user_id UUID := 'b61d3ee9-1799-4378-8746-2b5204db711d';

  -- Categories
  cat_combat UUID; cat_weapons UUID; cat_projectiles UUID;
  cat_enemies UUID; cat_platformer UUID; cat_characters UUID;
  cat_tilesets UUID; cat_terrain UUID; cat_nature UUID;
  cat_backgrounds UUID; cat_buildings UUID; cat_ruins UUID;
  cat_ui UUID; cat_icons UUID; cat_spells UUID;
  cat_effects UUID; cat_fonts UUID;
  cat_music UUID; cat_sfx UUID; cat_ambient UUID;

  -- Sprites — Zolt (combat)
  z1 UUID; z2 UUID; z3 UUID; z4 UUID; z5 UUID;

  -- Sprites — Lyra (environment)
  l1 UUID; l2 UUID; l3 UUID; l4 UUID; l5 UUID;

  -- Sprites — Vexis (ui/magic)
  v1 UUID; v2 UUID; v3 UUID; v4 UUID; v5 UUID;

  -- Sprites — Echo (audio)
  e1 UUID; e2 UUID; e3 UUID; e4 UUID; e5 UUID;

  -- Packs
  pz UUID; pl UUID; pv UUID; pe UUID;

  ph VARCHAR := 'https://res.cloudinary.com/dc18ql4cw/image/upload/v1773558971/placeholder_loetox.png';
  ph_id VARCHAR := 'placeholder_loetox';

BEGIN
  -- Get categories
  SELECT id INTO cat_combat FROM categories WHERE slug = 'combat';
  SELECT id INTO cat_weapons FROM categories WHERE slug = 'weapons';
  SELECT id INTO cat_projectiles FROM categories WHERE slug = 'projectiles';
  SELECT id INTO cat_enemies FROM categories WHERE slug = 'enemies';
  SELECT id INTO cat_platformer FROM categories WHERE slug = 'platformer';
  SELECT id INTO cat_characters FROM categories WHERE slug = 'characters';
  SELECT id INTO cat_tilesets FROM categories WHERE slug = 'tilesets';
  SELECT id INTO cat_terrain FROM categories WHERE slug = 'terrain';
  SELECT id INTO cat_nature FROM categories WHERE slug = 'nature';
  SELECT id INTO cat_backgrounds FROM categories WHERE slug = 'backgrounds';
  SELECT id INTO cat_buildings FROM categories WHERE slug = 'buildings';
  SELECT id INTO cat_ruins FROM categories WHERE slug = 'ruins';
  SELECT id INTO cat_ui FROM categories WHERE slug = 'ui-elements';
  SELECT id INTO cat_icons FROM categories WHERE slug = 'icons';
  SELECT id INTO cat_spells FROM categories WHERE slug = 'spells';
  SELECT id INTO cat_effects FROM categories WHERE slug = 'effects';
  SELECT id INTO cat_fonts FROM categories WHERE slug = 'fonts';
  SELECT id INTO cat_music FROM categories WHERE slug = 'music';
  SELECT id INTO cat_sfx FROM categories WHERE slug = 'sfx';
  SELECT id INTO cat_ambient FROM categories WHERE slug = 'ambient';

  -- ── ZOLT SPRITES (Combat / Action) ──────────────
  z1 := gen_random_uuid(); z2 := gen_random_uuid(); z3 := gen_random_uuid();
  z4 := gen_random_uuid(); z5 := gen_random_uuid();

  INSERT INTO sprites (id, name, slug, image_url, cloudinary_id, created_by, is_public, status, created_at, updated_at) VALUES
  (z1, 'Berserker Warrior Sheet',    'berserker-warrior',    ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (z2, 'Axe Combo Animation',        'axe-combo',            ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (z3, 'Arrow Projectile Pack',      'arrow-projectile',     ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (z4, 'Orc Horde Enemy Set',        'orc-horde',            ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (z5, 'Platformer Hero Jump Sheet', 'platformer-hero-jump', ph, ph_id, user_id, true, 'ACTIVE', now(), now());

  INSERT INTO sprite_categories (sprite_id, category_id) VALUES
  (z1, cat_combat), (z1, cat_characters),
  (z2, cat_combat), (z2, cat_weapons),
  (z3, cat_projectiles), (z3, cat_combat),
  (z4, cat_enemies), (z4, cat_combat),
  (z5, cat_platformer), (z5, cat_characters);

  -- ── LYRA SPRITES (Environment / Nature) ─────────
  l1 := gen_random_uuid(); l2 := gen_random_uuid(); l3 := gen_random_uuid();
  l4 := gen_random_uuid(); l5 := gen_random_uuid();

  INSERT INTO sprites (id, name, slug, image_url, cloudinary_id, created_by, is_public, status, created_at, updated_at) VALUES
  (l1, 'Enchanted Forest Tileset',  'enchanted-forest-tileset', ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (l2, 'Cobblestone Terrain Pack',  'cobblestone-terrain',      ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (l3, 'Sunset Horizon Background', 'sunset-horizon-bg',        ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (l4, 'Ancient Stone Ruins',       'ancient-stone-ruins',      ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (l5, 'Medieval Castle Building',  'medieval-castle',          ph, ph_id, user_id, true, 'ACTIVE', now(), now());

  INSERT INTO sprite_categories (sprite_id, category_id) VALUES
  (l1, cat_tilesets), (l1, cat_nature),
  (l2, cat_terrain), (l2, cat_tilesets),
  (l3, cat_backgrounds),
  (l4, cat_ruins), (l4, cat_buildings),
  (l5, cat_buildings);

  -- ── VEXIS SPRITES (UI / Magic) ───────────────────
  v1 := gen_random_uuid(); v2 := gen_random_uuid(); v3 := gen_random_uuid();
  v4 := gen_random_uuid(); v5 := gen_random_uuid();

  INSERT INTO sprites (id, name, slug, image_url, cloudinary_id, created_by, is_public, status, created_at, updated_at) VALUES
  (v1, 'Arcane HUD Frame Kit',     'arcane-hud-frame',   ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (v2, 'Elemental Spell Icons',    'elemental-icons',    ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (v3, 'Fireball Spell Effect',    'fireball-effect',    ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (v4, 'Pixel RPG Font Set',       'pixel-rpg-font',     ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (v5, 'Portal Magic Effect',      'portal-magic',       ph, ph_id, user_id, true, 'ACTIVE', now(), now());

  INSERT INTO sprite_categories (sprite_id, category_id) VALUES
  (v1, cat_ui),
  (v2, cat_icons), (v2, cat_spells),
  (v3, cat_spells), (v3, cat_effects),
  (v4, cat_fonts),
  (v5, cat_effects), (v5, cat_spells);

  -- ── ECHO SPRITES (Audio) ─────────────────────────
  e1 := gen_random_uuid(); e2 := gen_random_uuid(); e3 := gen_random_uuid();
  e4 := gen_random_uuid(); e5 := gen_random_uuid();

  INSERT INTO sprites (id, name, slug, image_url, cloudinary_id, created_by, is_public, status, created_at, updated_at) VALUES
  (e1, 'Epic Battle Orchestra',    'epic-battle-ost',    ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (e2, 'Dungeon Ambient Loop',     'dungeon-ambient',    ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (e3, 'Sword Combat SFX Pack',    'sword-combat-sfx',   ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (e4, 'Magic Spell SFX Bundle',   'magic-spell-sfx',    ph, ph_id, user_id, true, 'ACTIVE', now(), now()),
  (e5, 'Forest Nature Ambience',   'forest-ambience',    ph, ph_id, user_id, true, 'ACTIVE', now(), now());

  INSERT INTO sprite_categories (sprite_id, category_id) VALUES
  (e1, cat_music),
  (e2, cat_ambient),
  (e3, cat_sfx),
  (e4, cat_sfx), (e4, cat_spells),
  (e5, cat_ambient), (e5, cat_nature);

  -- ── ASSET PACKS ──────────────────────────────────
  pz := gen_random_uuid(); pl := gen_random_uuid();
  pv := gen_random_uuid(); pe := gen_random_uuid();

  INSERT INTO asset_pack (id, name, description, price, image_url, cloudinary_id, created_by, created_at, updated_at) VALUES
  (pz, 'Zolt''s Combat Arsenal',      'The ultimate combat pack — warriors, axes, projectiles, orc enemies and platformer heroes. Built for action games that hit hard.', 12.99, ph, ph_id, user_id, now(), now()),
  (pl, 'Lyra''s World Builder',        'A complete environment bundle featuring enchanted forests, cobblestone terrain, sunset backgrounds, ancient ruins and medieval castles.', 16.99, ph, ph_id, user_id, now(), now()),
  (pv, 'Vexis Arcane UI Tome',         'Everything your game UI needs — HUD frames, elemental icons, spell effects, pixel fonts, and portal magic animations.', 9.99, ph, ph_id, user_id, now(), now()),
  (pe, 'Echo''s Audio Sanctum',        'Immersive audio collection with battle orchestras, dungeon ambience, combat SFX, magic spell sounds, and forest atmospheres.', 11.99, ph, ph_id, user_id, now(), now());

  -- ── ASSET PACK SPRITES ───────────────────────────
  INSERT INTO asset_pack_sprites (asset_pack_id, sprite_id) VALUES
  (pz, z1), (pz, z2), (pz, z3), (pz, z4), (pz, z5),
  (pl, l1), (pl, l2), (pl, l3), (pl, l4), (pl, l5),
  (pv, v1), (pv, v2), (pv, v3), (pv, v4), (pv, v5),
  (pe, e1), (pe, e2), (pe, e3), (pe, e4), (pe, e5);

  RAISE NOTICE 'Seed complete! 20 sprites, 4 NPC-themed asset packs created.';
END $$;