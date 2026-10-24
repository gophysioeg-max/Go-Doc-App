# Go Doc RAG

The knowledge base behind the physio assistant and the patient chat
([spec](https://claude.ai/artifact/S86EMtwTbRC2v4wdXaDJfV), [source list](../docs/knowledge-library.md)).
It reads the books and guidelines in `library/files/`, splits them into cited chunks, stores them in
Postgres with pgvector, and answers questions with Claude, citing book, edition, section and page.

Everything runs on your own machine. Books stay in `library/files/`, which git ignores.

## How it works

1. **Extract.** Text is read page by page with PyMuPDF. Section headings come from the book's outline,
   and running headers and footers are removed. Markdown and text files are split by `#` headings.
2. **Chunk.** Chunks are about 2,400 characters and never cross a section boundary. Each keeps its
   heading and page range, and the last paragraph of each chunk is repeated at the start of the next.
3. **Embed.** Each chunk is embedded as `title + heading + text` with bge-m3, which runs locally, is free
   and handles Arabic well. Voyage is an alternative.
4. **Store.** Two tables, `knowledge_sources` and `knowledge_chunks`, hold two tiers: `clinical` for
   physios and `patient` for patients. A patient query can never read the clinical tier.
5. **Search.** Hybrid search runs vector similarity and full-text search over normalised Arabic and
   English, then fuses the two rankings with Reciprocal Rank Fusion.
6. **Answer.** Each question goes through these checks in order:
   1. In patient mode, the red-flag rules run first and can return the urgent-care message.
   2. A medication question gets a fixed answer.
   3. If the best similarity is below the threshold, the answer is "no source".
   4. Claude answers from `search_result` blocks with citations turned on.
   5. In patient mode, the answer is checked for diagnosis and medication wording.

## Set up (once)

```bash
cd rag
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[local,dev]"          # bge-m3 needs ~2 GB of disk on first run
cp .env.example .env                    # add ANTHROPIC_API_KEY
docker compose up -d                    # local Postgres + pgvector
godoc-rag init-db
```

To use your Supabase project instead of Docker, set `DATABASE_URL` to its direct connection string,
then run `godoc-rag init-db`. The SQL is in `sql/001_knowledge.sql`.

## Add sources

1. Put the files in `library/files/`. The names in `library/manifest.csv` are the ones it expects for
   the P0 list.
2. Run `godoc-rag scan` to add rows for any files the manifest does not list yet.
3. Open `library/manifest.csv` and fill in title, edition, specialty, kind
   (`guideline | textbook | program | article`), tier (`clinical | patient`) and priority.
4. Run `godoc-rag ingest`. Sources that haven't changed are skipped. Missing files are listed and
   don't stop the run.

Scanned PDFs with no text layer need OCR first, for example `ocrmypdf in.pdf out.pdf`.

## Use

```bash
godoc-rag status                                         # sources and chunk counts
godoc-rag search "special tests lateral hip pain"        # see what retrieval returns
godoc-rag ask "progression criteria after ACL reconstruction"            # physio
godoc-rag ask "ليه ركبتي بتوجعني على السلم؟" --audience patient            # patient
godoc-rag retire magee-orthopedic-assessment             # stop citing a source
godoc-rag ingest --only magee-orthopedic-assessment --force
```

## Test

```bash
pytest          # 58 tests; the pipeline tests need the database from docker compose
```

The red-flag cases are in `tests/test_redflags.py`. Every new rule needs a positive case and must
keep the routine messages passing.

## Tuning

| Setting | Default | Change when |
| --- | --- | --- |
| `GODOC_MIN_SIMILARITY` | 0.35 | Too many "no source" answers: lower it. Answers drift off topic: raise it. Tune on about 50 real questions |
| `GODOC_CHUNK_CHARS` | 2400 | Citations feel too broad: lower it |
| `GODOC_EMBEDDER` | bge-m3 | Switch to `voyage` if bge-m3 is too slow on your machine. Changing the embedder means a full `ingest --force` |
