INSERT INTO categories (id, name, slug, description, created_at, updated_at) VALUES
-- Environment
(gen_random_uuid(), 'Tilesets', 'tilesets', 'Tile-based environment assets', now(), now()),
(gen_random_uuid(), 'Terrain', 'terrain', 'Ground, floor, and terrain tiles', now(), now()),
(gen_random_uuid(), 'Backgrounds', 'backgrounds', 'Background and scenery assets', now(), now()),
(gen_random_uuid(), 'Dungeon', 'dungeon', 'Dungeon tiles, traps, and underground assets', now(), now()),
(gen_random_uuid(), 'Buildings', 'buildings', 'Building and structure assets', now(), now()),
(gen_random_uuid(), 'Ruins', 'ruins', 'Ancient ruins and mystical structures', now(), now()),
(gen_random_uuid(), 'Nature', 'nature', 'Nature and vegetation assets', now(), now()),

-- Characters
(gen_random_uuid(), 'Characters', 'characters', 'Character sprites and animations', now(), now()),
(gen_random_uuid(), 'Enemies', 'enemies', 'Enemy sprites and boss characters', now(), now()),
(gen_random_uuid(), 'Animals', 'animals', 'Animal sprites and creatures', now(), now()),
(gen_random_uuid(), 'Dragons', 'dragons', 'Dragon sprites and mythical creatures', now(), now()),
(gen_random_uuid(), 'Undead', 'undead', 'Undead, skeletons, and dark creatures', now(), now()),
(gen_random_uuid(), 'Vehicles', 'vehicles', 'Vehicle sprites and animations', now(), now()),

-- Combat & Action
(gen_random_uuid(), 'Combat', 'combat', 'Combat animations and weapon effects', now(), now()),
(gen_random_uuid(), 'Weapons', 'weapons', 'Weapon sprites and animations', now(), now()),
(gen_random_uuid(), 'Projectiles', 'projectiles', 'Bullets, arrows, and projectile assets', now(), now()),

-- Fantasy & Magic
(gen_random_uuid(), 'Fantasy', 'fantasy', 'Fantasy-themed assets and magical elements', now(), now()),
(gen_random_uuid(), 'Spells', 'spells', 'Spell effects and magic animations', now(), now()),
(gen_random_uuid(), 'Potions', 'potions', 'Potion and consumable item assets', now(), now()),
(gen_random_uuid(), 'Effects', 'effects', 'Visual effects and particle systems', now(), now()),

-- Props & Items
(gen_random_uuid(), 'Props', 'props', 'Interactive and decorative prop assets', now(), now()),
(gen_random_uuid(), 'Icons', 'icons', 'Icon packs and UI symbols', now(), now()),

-- UI & Game Feel
(gen_random_uuid(), 'UI Elements', 'ui-elements', 'User interface components and HUD elements', now(), now()),
(gen_random_uuid(), 'Fonts', 'fonts', 'Pixel fonts and typography', now(), now()),
(gen_random_uuid(), 'Animations', 'animations', 'Standalone animation sheets and sprite sequences', now(), now()),
(gen_random_uuid(), 'Cutscenes', 'cutscenes', 'Cutscene backgrounds and story assets', now(), now()),

-- Audio
(gen_random_uuid(), 'Music', 'music', 'Music packs and soundtracks', now(), now()),
(gen_random_uuid(), 'SFX', 'sfx', 'Sound effects and audio assets', now(), now()),
(gen_random_uuid(), 'Ambient', 'ambient', 'Ambient sounds and atmospheric audio', now(), now()),

-- Genres & Packs
(gen_random_uuid(), 'RPG', 'rpg', 'RPG-specific assets including maps, characters, and UI', now(), now()),
(gen_random_uuid(), 'Platformer', 'platformer', 'Platformer-specific assets and mechanics', now(), now()),
(gen_random_uuid(), 'Top-down', 'top-down', 'Top-down perspective game assets', now(), now()),
(gen_random_uuid(), 'Side-scroller', 'side-scroller', 'Side-scrolling game assets and environments', now(), now()),
(gen_random_uuid(), 'Asset Packs', 'asset-packs', 'Complete multi-asset collection packs', now(), now());