-- Go Doc knowledge base: sources, chunks and hybrid search.
-- Runs on plain Postgres 16 + pgvector and on Supabase (same SQL).
-- Embedding size is fixed at 1024 (bge-m3 and Voyage 1024-dim models).

create extension if not exists vector;

create table if not exists knowledge_sources (
  id            text primary key,              -- slug from library/manifest.csv
  title         text not null,
  authors       text,
  edition       text,
  year          int,
  publisher     text,
  specialty     text,
  kind          text not null check (kind in ('guideline', 'textbook', 'program', 'article')),
  tier          text not null check (tier in ('clinical', 'patient')),
  priority      text check (priority in ('P0', 'P1', 'P2')),
  language      text not null default 'en',
  file_path     text not null,
  file_sha256   text not null,
  review_date   date,
  status        text not null default 'active' check (status in ('active', 'expired', 'removed')),
  ingested_at   timestamptz not null default now()
);

create table if not exists knowledge_chunks (
  id            bigserial primary key,
  source_id     text not null references knowledge_sources (id) on delete cascade,
  tier          text not null check (tier in ('clinical', 'patient')),
  ordinal       int  not null,                 -- position inside the source
  heading       text,                          -- "Chapter 12 > Shoulder > Special tests"
  page_start    int,
  page_end      int,
  content       text not null,                 -- original text, shown and cited
  search_text   text not null,                 -- normalised text for full-text search
  embedding     vector(1024) not null,
  fts           tsvector generated always as (to_tsvector('simple', search_text)) stored,
  unique (source_id, ordinal)
);

create index if not exists knowledge_chunks_embedding_idx
  on knowledge_chunks using hnsw (embedding vector_cosine_ops);
create index if not exists knowledge_chunks_fts_idx
  on knowledge_chunks using gin (fts);
create index if not exists knowledge_chunks_tier_idx
  on knowledge_chunks (tier);

-- Hybrid search: vector similarity and full-text rank fused with
-- Reciprocal Rank Fusion. Only active sources of the requested tier.
-- Returns the best vector similarity per row so callers can apply
-- "no source, no answer".
create or replace function match_chunks(
  query_embedding vector(1024),
  query_text      text,
  match_tier      text,
  match_count     int default 8,
  candidates      int default 50,
  rrf_k           int default 60
)
returns table (
  id          bigint,
  source_id   text,
  title       text,
  edition     text,
  heading     text,
  page_start  int,
  page_end    int,
  content     text,
  similarity  float,
  score       float
)
language sql stable
as $$
  with vec as (
    select c.id,
           1 - (c.embedding <=> query_embedding) as similarity,
           row_number() over (order by c.embedding <=> query_embedding) as rnk
    from knowledge_chunks c
    join knowledge_sources s on s.id = c.source_id
    where c.tier = match_tier and s.status = 'active'
    order by c.embedding <=> query_embedding
    limit candidates
  ),
  txt as (
    select c.id,
           row_number() over (
             order by ts_rank_cd(c.fts, websearch_to_tsquery('simple', query_text)) desc
           ) as rnk
    from knowledge_chunks c
    join knowledge_sources s on s.id = c.source_id
    where c.tier = match_tier and s.status = 'active'
      and c.fts @@ websearch_to_tsquery('simple', query_text)
    limit candidates
  ),
  fused as (
    select coalesce(vec.id, txt.id) as id,
           coalesce(1.0 / (rrf_k + vec.rnk), 0) + coalesce(1.0 / (rrf_k + txt.rnk), 0) as score
    from vec full outer join txt on vec.id = txt.id
  )
  select c.id, c.source_id, s.title, s.edition, c.heading, c.page_start, c.page_end, c.content,
         1 - (c.embedding <=> query_embedding) as similarity,
         f.score
  from fused f
  join knowledge_chunks c on c.id = f.id
  join knowledge_sources s on s.id = c.source_id
  order by f.score desc
  limit match_count;
$$;

-- On Supabase: no client may read these tables directly. Edge Functions use
-- the service role and enforce the tier in code (patients never get 'clinical').
alter table knowledge_sources enable row level security;
alter table knowledge_chunks  enable row level security;
