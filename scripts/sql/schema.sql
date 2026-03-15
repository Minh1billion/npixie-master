-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.asset_pack (
  id uuid NOT NULL,
  cloudinary_id character varying NOT NULL,
  created_at timestamp without time zone,
  description text,
  image_url character varying NOT NULL,
  name character varying NOT NULL,
  price numeric NOT NULL,
  updated_at timestamp without time zone,
  created_by uuid NOT NULL,
  deleted_at timestamp without time zone,
  CONSTRAINT asset_pack_pkey PRIMARY KEY (id),
  CONSTRAINT fk1r4h2j6tvb87g5bfodj457rcd FOREIGN KEY (created_by) REFERENCES public.users(id)
);
CREATE TABLE public.asset_pack_sprites (
  asset_pack_id uuid NOT NULL,
  sprite_id uuid NOT NULL,
  CONSTRAINT fkqddvng16y3sefhcrdixmx86vx FOREIGN KEY (sprite_id) REFERENCES public.sprites(id),
  CONSTRAINT fkbb67v59b3sam3605g6ihmi6pw FOREIGN KEY (asset_pack_id) REFERENCES public.asset_pack(id)
);
CREATE TABLE public.categories (
  id uuid NOT NULL,
  created_at timestamp without time zone,
  description text,
  name character varying NOT NULL UNIQUE,
  slug character varying NOT NULL UNIQUE,
  updated_at timestamp without time zone,
  CONSTRAINT categories_pkey PRIMARY KEY (id)
);
CREATE TABLE public.refresh_tokens (
  id uuid NOT NULL,
  created_at timestamp without time zone,
  expires_at timestamp without time zone NOT NULL,
  is_revoked boolean NOT NULL,
  token character varying NOT NULL UNIQUE,
  user_id uuid NOT NULL,
  CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id),
  CONSTRAINT fk1lih5y2npsf8u5o3vhdb9y0os FOREIGN KEY (user_id) REFERENCES public.users(id)
);
CREATE TABLE public.sprite_categories (
  sprite_id uuid NOT NULL,
  category_id uuid NOT NULL,
  CONSTRAINT fke3mk28q0sv4sbn93tpbt6aelp FOREIGN KEY (category_id) REFERENCES public.categories(id),
  CONSTRAINT fkme1aaj7mfis2swiq7b6ig8rko FOREIGN KEY (sprite_id) REFERENCES public.sprites(id)
);
CREATE TABLE public.sprites (
  id uuid NOT NULL,
  cloudinary_id character varying NOT NULL,
  created_at timestamp without time zone,
  image_url character varying NOT NULL,
  name character varying NOT NULL,
  slug character varying NOT NULL UNIQUE,
  updated_at timestamp without time zone,
  created_by uuid NOT NULL,
  deleted_at timestamp without time zone,
  is_public boolean,
  status character varying NOT NULL DEFAULT 'ACTIVE'::character varying,
  CONSTRAINT sprites_pkey PRIMARY KEY (id),
  CONSTRAINT fkd2yxg5ry8479832dpm5uxmy0d FOREIGN KEY (created_by) REFERENCES public.users(id)
);
CREATE TABLE public.user_auth_providers (
  id uuid NOT NULL,
  provider character varying NOT NULL CHECK (provider::text = ANY (ARRAY['LOCAL'::character varying, 'GOOGLE'::character varying, 'GITHUB'::character varying]::text[])),
  provider_id character varying NOT NULL,
  user_id uuid NOT NULL,
  CONSTRAINT user_auth_providers_pkey PRIMARY KEY (id),
  CONSTRAINT fk36nn9pmlugyb6c34h3vakuai FOREIGN KEY (user_id) REFERENCES public.users(id)
);
CREATE TABLE public.users (
  id uuid NOT NULL,
  avatar_url character varying,
  created_at timestamp without time zone,
  email character varying UNIQUE,
  full_name character varying NOT NULL,
  is_active boolean NOT NULL,
  is_verified boolean NOT NULL,
  password character varying,
  role character varying NOT NULL CHECK (role::text = ANY (ARRAY['USER'::character varying, 'ADMIN'::character varying]::text[])),
  updated_at timestamp without time zone,
  username character varying NOT NULL,
  CONSTRAINT users_pkey PRIMARY KEY (id)
);