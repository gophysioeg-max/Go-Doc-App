"""End to end on a real Postgres + pgvector: manifest -> ingest -> hybrid search -> retire."""

import csv

import psycopg
import pytest

from godoc_rag import cli, embed, store

from .conftest import HEEL_PAGES, HEEL_TOC, make_pdf

ROWS = [
    {"id": "heel-program", "title": "Go Doc Plantar Heel Pain Program", "edition": "1",
     "kind": "program", "tier": "clinical", "priority": "P0", "file": "heel.pdf"},
    {"id": "knee-article", "title": "Knee pain on stairs", "kind": "article",
     "tier": "patient", "priority": "P0", "file": "knee.md", "language": "ar"},
]


@pytest.fixture
def library(tmp_path, monkeypatch, db_url):
    files = tmp_path / "files"
    files.mkdir()
    make_pdf(files / "heel.pdf", HEEL_PAGES, HEEL_TOC)
    (files / "knee.md").write_text(
        "# ألم الركبة على السلم\nاطلع السلم برجلك السليمة الأول، وانزل برجلك اللي بتوجعك الأول.\n"
        "## تمارين\nتمرين فرد الركبة وانت قاعد على كرسي، عشر مرات، مرتين في اليوم.\n",
        encoding="utf-8")
    with (tmp_path / "manifest.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "title", "authors", "edition", "year", "publisher",
                                          "specialty", "kind", "tier", "priority", "language",
                                          "file", "review_date", "status"])
        w.writeheader()
        w.writerows(ROWS)
    monkeypatch.setenv("GODOC_LIBRARY_DIR", str(tmp_path))
    monkeypatch.setenv("GODOC_MANIFEST", str(tmp_path / "manifest.csv"))
    monkeypatch.setenv("GODOC_EMBEDDER", "hash")
    monkeypatch.setenv("DATABASE_URL", db_url)
    with psycopg.connect(db_url, autocommit=True) as conn:
        conn.execute("drop table if exists knowledge_chunks, knowledge_sources cascade")
    assert cli.main(["init-db"]) == 0
    return tmp_path


def _search(db_url, query, tier):
    with store.connect(db_url) as conn:
        return store.search(conn, embed.HashEmbedder().embed_query(query), query, tier, 5)


def test_ingest_then_search_finds_cited_passage(library, db_url, capsys):
    assert cli.main(["ingest"]) == 0
    out = capsys.readouterr().out
    assert "ok     heel-program" in out and "ok     knee-article" in out

    hits = _search(db_url, "calf raises progression first-step pain", "clinical")
    assert hits[0].source_id == "heel-program"
    assert "Calf raises" in hits[0].content
    assert hits[0].heading.endswith("Phase 2")
    assert "Go Doc Plantar Heel Pain Program, 1 ed." in hits[0].citation
    assert "p. " in hits[0].citation or "pp. " in hits[0].citation


def test_unchanged_files_are_skipped(library, capsys):
    cli.main(["ingest"])
    capsys.readouterr()
    assert cli.main(["ingest"]) == 0
    assert "same   heel-program" in capsys.readouterr().out


def test_tiers_are_isolated(library, db_url):
    cli.main(["ingest"])
    assert all(h.source_id == "knee-article" for h in _search(db_url, "السلم الركبة", "patient"))
    assert all(h.source_id == "heel-program" for h in _search(db_url, "السلم الركبة", "clinical"))


def test_arabic_spelling_variants_match_in_full_text(library, db_url):
    cli.main(["ingest"])
    # "الركبه" (ه) and "اطلع" without hamza must still match the stored text.
    hits = _search(db_url, "الركبه اطلع السلم", "patient")
    assert hits and hits[0].source_id == "knee-article"


def test_retired_source_is_not_cited(library, db_url):
    cli.main(["ingest"])
    assert cli.main(["retire", "heel-program"]) == 0
    assert _search(db_url, "calf raises", "clinical") == []


def test_missing_file_is_reported_and_others_still_ingest(library, capsys):
    (library / "files" / "heel.pdf").unlink()
    assert cli.main(["ingest"]) == 0
    out = capsys.readouterr().out
    assert "missing heel-program" in out
    assert "ok     knee-article" in out


def test_unreadable_file_fails(library, capsys):
    (library / "files" / "heel.pdf").write_bytes(b"not a pdf")
    assert cli.main(["ingest"]) == 1
    assert "FAILED heel-program" in capsys.readouterr().err


def test_scan_adds_new_files(library, capsys):
    make_pdf(library / "files" / "new-book.pdf", [("h", "Some text.")], [[1, "Ch 1", 1]])
    assert cli.main(["scan"]) == 0
    assert "added new-book: new-book.pdf" in capsys.readouterr().out
    assert "new-book.pdf" in (library / "manifest.csv").read_text(encoding="utf-8")
