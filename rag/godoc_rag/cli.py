"""Command line: godoc-rag init-db | scan | ingest | status | search | ask | retire."""

from __future__ import annotations

import argparse
import sys
import time

from . import answer, config, embed, manifest, store
from .chunk import chunk_pages
from .extract import extract


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="godoc-rag", description="Go Doc knowledge base tools")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init-db", help="create tables, indexes and the search function")
    sub.add_parser("scan", help="add rows to the manifest for new files in library/files")
    p = sub.add_parser("ingest", help="extract, chunk, embed and store every source in the manifest")
    p.add_argument("--only", nargs="*", help="source ids to ingest (default: all)")
    p.add_argument("--force", action="store_true", help="re-ingest even if the file is unchanged")
    sub.add_parser("status", help="list stored sources and chunk counts")
    p = sub.add_parser("search", help="show the passages retrieved for a query")
    p.add_argument("query")
    p.add_argument("--tier", choices=["clinical", "patient"], default="clinical")
    p.add_argument("-k", type=int, default=8)
    p = sub.add_parser("ask", help="answer a question with citations")
    p.add_argument("question")
    p.add_argument("--audience", choices=["physio", "patient"], default="physio")
    p.add_argument("-k", type=int, default=8)
    p = sub.add_parser("retire", help="stop citing a source (status expired or removed)")
    p.add_argument("source_id")
    p.add_argument("--status", choices=["expired", "removed", "active"], default="expired")
    args = parser.parse_args(argv)

    settings = config.load()
    if args.command == "scan":
        return _scan(settings)
    with store.connect(settings.database_url) as conn:
        if args.command == "init-db":
            store.init_schema(conn)
            print("Schema ready.")
        elif args.command == "ingest":
            return _ingest(settings, conn, args.only, args.force)
        elif args.command == "status":
            for sid, tier, status, n, title in store.stats(conn):
                print(f"{tier:8} {status:8} {n:6} chunks  {sid}  ({title})")
        elif args.command == "search":
            emb = embed.get(settings.embedder, settings.voyage_model)
            for h in store.search(conn, emb.embed_query(args.query), args.query, args.tier, args.k):
                print(f"\n[{h.similarity:.3f} | {h.score:.4f}] {h.citation}\n{h.content[:400]}…")
        elif args.command == "ask":
            return _ask(settings, conn, args.question, args.audience, args.k)
        elif args.command == "retire":
            ok = store.set_status(conn, args.source_id, args.status)
            print(f"{args.source_id}: {args.status}" if ok else f"{args.source_id}: not found")
            return 0 if ok else 1
    return 0


def _scan(settings: config.Settings) -> int:
    new = manifest.scan(settings.library_dir, settings.manifest_path)
    if not new:
        print("No new files.")
        return 0
    manifest.append(settings.manifest_path, new)
    for s in new:
        print(f"added {s.id}: {s.file}")
    print(f"\n{len(new)} rows added to {settings.manifest_path}. "
          "Fill in edition, specialty, kind, tier and priority before ingesting.")
    return 0


def _ingest(settings: config.Settings, conn, only: list[str] | None, force: bool) -> int:
    sources = manifest.read(settings.manifest_path)
    if only:
        unknown = set(only) - {s.id for s in sources}
        if unknown:
            print(f"not in manifest: {', '.join(sorted(unknown))}", file=sys.stderr)
            return 1
        sources = [s for s in sources if s.id in only]
    emb = None
    failures = missing = 0
    for s in sources:
        path = s.path(settings.library_dir)
        if s.status != "active":
            store.set_status(conn, s.id, s.status)
            print(f"skip   {s.id}: status {s.status}")
            continue
        if not path.exists():
            missing += 1
            print(f"missing {s.id}: put the file at {path}")
            continue
        digest = manifest.sha256(path)
        if not force and store.stored_hash(conn, s.id) == digest:
            print(f"same   {s.id}")
            continue
        started = time.time()
        try:
            pages = extract(path)
            chunks = chunk_pages(pages, settings.chunk_chars, settings.overlap_chars)
            if not chunks:
                raise ValueError("no text extracted (scanned PDF? run OCR first)")
            emb = emb or embed.get(settings.embedder, settings.voyage_model)
            texts = [f"{s.title}\n{c.heading or ''}\n{c.content}" for c in chunks]
            store.replace_source(conn, s, digest, chunks, emb.embed_documents(texts))
        except Exception as e:  # report and carry on with the next source
            conn.rollback()
            print(f"FAILED {s.id}: {e}", file=sys.stderr)
            failures += 1
            continue
        print(f"ok     {s.id}: {len(pages)} pages, {len(chunks)} chunks, "
              f"{time.time() - started:.0f}s")
    if missing:
        print(f"\n{missing} source(s) in the manifest have no file yet.")
    return 1 if failures else 0


def _ask(settings: config.Settings, conn, question: str, audience: str, k: int) -> int:
    result = answer.pre_checks(question, audience)
    if result is None:
        import anthropic

        emb = embed.get(settings.embedder, settings.voyage_model)
        tier = "clinical" if audience == "physio" else "patient"
        hits = store.search(conn, emb.embed_query(question), question, tier, k)
        result = answer.generate(anthropic.Anthropic(), settings.answer_model, question,
                                 audience, hits, settings.min_similarity)
    print(f"[{result.status}]" + (f" flags: {', '.join(result.flags)}" if result.flags else ""))
    print(result.text)
    for c in result.citations:
        print(f"\n[{c.number}] {c.reference}\n    \"{c.quote[:300]}\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
