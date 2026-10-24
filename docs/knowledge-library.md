# Go Doc Knowledge Library and Build Resources

Everything Go Doc needs to build the knowledge layer described in the
[Self-Assessment & Knowledge Assistant spec](https://claude.ai/artifact/S86EMtwTbRC2v4wdXaDJfV):
the sources that go into the knowledge base, and the material to learn how to build it.

As of 24 Oct 2026. Owner of the source list: Michael (decision K5). Licences: decision K4.

## How to read this list

| Mark | Meaning |
| --- | --- |
| **P0** | Needed before the physio assistant launches (Phase 2) |
| **P1** | Add in the first 3 months after launch |
| **P2** | Add when the specialty is offered or asked for |
| **Ingest** | Goes into the clinical tier (chunked, embedded, cited) |
| **Reference** | Read by Michael to write patient articles and triage rules; not ingested |
| **Licence** | Ingest only after written permission from the publisher (decision K4) |

Order of authority when sources disagree: clinical practice guideline → systematic review → textbook.
Guidelines are ingested first because they are free or cheap to licence and are revised more often than textbooks.

<!-- SOURCES -->

## Learning to build it

### 1. Foundations: how RAG systems work

| Resource | Type | Why |
| --- | --- | --- |
| Chip Huyen, *AI Engineering* (O'Reilly) | Book | The best single overview: RAG, evaluation, guardrails, cost |
| Jay Alammar and Maarten Grootendorst, *Hands-On Large Language Models* (O'Reilly) | Book | Embeddings, semantic search and RAG with diagrams and code |
| John Berryman and Albert Ziegler, *Prompt Engineering for LLMs* (O'Reilly) | Book | How to structure prompts and context for reliable answers |
| [Anthropic: Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) | Article | Chunking + contextual embeddings + BM25 + reranking; the retrieval design this project should copy |
| [Anthropic courses on GitHub](https://github.com/anthropics/courses) | Course | API fundamentals, prompt engineering, real-world prompting, tool use |
| [Anthropic Academy](https://anthropic.skilljar.com) | Course | Free courses on building with the Claude API |
| [Claude cookbooks](https://github.com/anthropics/anthropic-cookbook) | Code | RAG, contextual retrieval, citations and evaluation notebooks |
| [DeepLearning.AI short courses](https://www.deeplearning.ai/short-courses/) | Course | Search for "RAG", "evaluating RAG", "embeddings", "vector databases" |

### 2. Claude API features this project uses

| Feature | Docs | Used for |
| --- | --- | --- |
| Citations | [docs](https://platform.claude.com/docs/en/build-with-claude/citations) | Every answer quotes its source passage (safety rule "No source, no answer") |
| Prompt caching | [docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | Cache the fixed system prompt and safety rules; cuts cost and latency per message |
| Structured outputs | [docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) | The pre-visit brief and the diagnosis/medication output check as validated JSON |
| PDF support | [docs](https://platform.claude.com/docs/en/build-with-claude/pdf-support) | Reading guideline PDFs during ingestion |
| Streaming | [docs](https://platform.claude.com/docs/en/build-with-claude/streaming) | Chat answers appear as they are written |
| Batch processing | [docs](https://platform.claude.com/docs/en/build-with-claude/batch-processing) | Generating chunk context for contextual retrieval at half price |
| Embeddings | [docs](https://platform.claude.com/docs/en/build-with-claude/embeddings) | Anthropic has no embedding model of its own; this page lists recommended providers |
| TypeScript SDK | [repo](https://github.com/anthropics/anthropic-sdk-typescript) | Supabase Edge Functions run TypeScript (Deno) |
| Python SDK | [repo](https://github.com/anthropics/anthropic-sdk-python) | The ingestion script |

### 3. Stack: GitHub, Vercel, Supabase, Expo

| Resource | Used for |
| --- | --- |
| [Supabase AI & Vectors](https://supabase.com/docs/guides/ai) | pgvector setup, semantic and hybrid search, RAG with permissions |
| [pgvector](https://github.com/pgvector/pgvector) | Vector column types and indexes (HNSW) |
| [Supabase Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security) | "Physio sees assigned patients only"; patients cannot read the clinical tier |
| [Supabase Edge Functions](https://supabase.com/docs/guides/functions) | The chat, assistant and triage APIs |
| [Supabase phone login](https://supabase.com/docs/guides/auth/phone-login) | Phone and one-time code sign-in |
| [Supabase Storage](https://supabase.com/docs/guides/storage) | Source files, exercise videos, before/after photos |
| [Next.js docs](https://nextjs.org/docs) | Web apps for patient, physio and admin |
| [Vercel docs](https://vercel.com/docs) | Deploys from GitHub `main`, preview per pull request, environment variables |
| [Expo docs](https://docs.expo.dev) | Patient and physio mobile apps, push notifications |
| [GitHub Actions](https://docs.github.com/actions) | Tests and the safety test set on every pull request |

### 4. Arabic language

| Resource | Used for |
| --- | --- |
| [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard) | Compare embedding models on Arabic retrieval before choosing (decision K3) |
| [CAMeL Tools](https://github.com/CAMeL-Lab/camel_tools) | Arabic normalisation and dialect handling (alef/yaa forms, diacritics, Arabic-Indic digits) |
| [Arabic-English medical glossary: WHO EMRO Unified Medical Dictionary](https://www.emro.who.int/umd/) | Consistent Arabic terms in patient articles |

### 5. Getting text out of books and PDFs

| Resource | Used for |
| --- | --- |
| [Docling](https://github.com/docling-project/docling) | PDF to structured text with headings, tables and page numbers |
| [PyMuPDF](https://pymupdf.readthedocs.io) | Fast page-level text extraction with page numbers for citations |

### 6. Testing that it is safe and correct

| Resource | Used for |
| --- | --- |
| [Ragas](https://docs.ragas.io) | Retrieval and answer-faithfulness metrics |
| [promptfoo](https://www.promptfoo.dev) | Regression tests in CI: red-flag phrases, diagnosis wording, medication refusals |
| [Anthropic: define success criteria and build evals](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) | How to write an eval set |

The safety test set (decision K12) is written by Michael: at least one message per red flag in each of the 10 patterns,
in Arabic, English and Franco-Arabic, plus diagnosis-seeking and medication questions. It runs on every pull request.

### 7. Medical AI, regulation and privacy

| Resource | Used for |
| --- | --- |
| [WHO: Ethics and governance of AI for health (2021)](https://www.who.int/publications/i/item/9789240029200) | Principles to cite in the legal review |
| [WHO: Guidance on large multi-modal models (2024)](https://www.who.int/publications/i/item/9789240084759) | Risks specific to chat models in health |
| [FDA: Clinical Decision Support Software guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software) | Why the physio assistant (professional reviews the basis) is lower risk than patient-facing advice |
| [IMDRF: Software as a Medical Device](https://www.imdrf.org/documents) | Risk categories regulators use for health software |
| Egypt Personal Data Protection Law (Law 151 of 2020) and its executive regulations | Health data consent and retention; confirm in the legal review (K6) |
| Egyptian Drug Authority rules on medical devices and software | Whether the patient chat counts as a device; confirm in the legal review (K6) |

## Next steps

1. Michael confirms the P0 list and marks anything Go Doc already owns.
2. Omar emails the publishers of P0 textbooks asking for commercial AI-use licences (template to draft).
3. While waiting: ingest the free P0 guidelines and Mona's program, and build the physio assistant on them.
4. Run the embedding comparison on 50 real Arabic and English questions (K3).
5. Write the safety test set before any patient-facing code.
