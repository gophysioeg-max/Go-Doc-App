"""Postgres + pgvector storage: schema, ingestion writes and hybrid search."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import psycopg
from pgvector.psycopg import register_vector

from .chunk import Chunk
from .manifest import Source
from .normalize import normalize

SCHEMA = Path(__file__).resolve().parents[1] / "sql" / "001_knowledge.sql"


@dataclass
class Hit:
    id: int
    source_id: str
    title: str
    edition: str | None
    heading: str | None
    page_start: int | None
    page_end: int | None
    content: str
    similarity: float
    score: float

    @property
    def citation(self) -> str:
        parts = [self.title]
        if self.edition:
            parts.append(f"{self.edition} ed.")
        if self.heading:
            parts.append(self.heading)
        if self.page_start:
            pages = (f"p. {self.page_start}" if self.page_start == self.page_end
                     else f"pp. {self.page_start}–{self.page_end}")
            parts.append(pages)
        return ", ".join(parts)


def connect(database_url: str) -> psycopg.Connection:
    conn = psycopg.connect(database_url, autocommit=False)
    conn.execute("create extension if not exists vector")
    register_vector(conn)
    return conn


def init_schema(conn: psycopg.Connection) -> None:
    conn.execute(SCHEMA.read_text(encoding="utf-8"))
    conn.commit()


def stored_hash(conn: psycopg.Connection, source_id: str) -> str | None:
    row = conn.execute("select file_sha256 from knowledge_sources where id = %s",
                       (source_id,)).fetchone()
    return row[0] if row else None


def replace_source(conn: psycopg.Connection, source: Source, file_sha256: str,
                   chunks: list[Chunk], embeddings: list[list[float]]) -> None:
    """Write a source and its chunks in one transaction, replacing any older version."""
    import numpy as np

    year = int(source.year) if source.year.isdigit() else None
    with conn.transaction():
        conn.execute("delete from knowledge_sources where id = %s", (source.id,))
        conn.execute(
            """insert into knowledge_sources
               (id, title, authors, edition, year, publisher, specialty, kind, tier,
                priority, language, file_path, file_sha256, review_date, status)
               values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (source.id, source.title, source.authors or None, source.edition or None, year,
             source.publisher or None, source.specialty or None, source.kind, source.tier,
             source.priority or None, source.language, source.file, file_sha256,
             source.review_date or None, source.status),
        )
        with conn.cursor() as cur:
            cur.executemany(
                """insert into knowledge_chunks
                   (source_id, tier, ordinal, heading, page_start, page_end, content,
                    search_text, embedding)
                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                [(source.id, source.tier, c.ordinal, c.heading, c.page_start, c.page_end,
                  c.content, normalize(f"{c.heading or ''} {c.content}"),
                  np.asarray(e, dtype=np.float32))
                 for c, e in zip(chunks, embeddings, strict=True)],
            )


def set_status(conn: psycopg.Connection, source_id: str, status: str) -> bool:
    with conn.transaction():
        cur = conn.execute("update knowledge_sources set status = %s where id = %s",
                           (status, source_id))
    return cur.rowcount == 1


def search(conn: psycopg.Connection, query_embedding: list[float], query_text: str,
           tier: str, limit: int = 8) -> list[Hit]:
    import numpy as np

    rows = conn.execute(
        "select * from match_chunks(%s, %s, %s, %s)",
        (np.asarray(query_embedding, dtype=np.float32), normalize(query_text), tier, limit),
    ).fetchall()
    conn.commit()
    return [Hit(*row) for row in rows]


def stats(conn: psycopg.Connection) -> list[tuple]:
    return conn.execute(
        """select s.id, s.tier, s.status, count(c.id), s.title
           from knowledge_sources s left join knowledge_chunks c on c.source_id = s.id
           group by s.id order by s.tier, s.id"""
    ).fetchall()
