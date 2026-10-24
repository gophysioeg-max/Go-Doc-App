"""Split pages into chunks that keep their heading and page range for citation."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .extract import Page


@dataclass
class Chunk:
    ordinal: int
    heading: str | None
    page_start: int
    page_end: int
    content: str


def chunk_pages(pages: list[Page], max_chars: int = 2400, overlap_chars: int = 300) -> list[Chunk]:
    """Group paragraphs into chunks of at most ~max_chars.

    A new chunk starts whenever the section heading changes, so a chunk never
    mixes two sections. The last paragraphs of a chunk (up to overlap_chars)
    are repeated at the start of the next one in the same section.
    """
    chunks: list[Chunk] = []
    paras: list[tuple[int, str]] = []  # (page, paragraph)
    heading: str | None = None

    def emit() -> None:
        if not paras:
            return
        chunks.append(Chunk(
            ordinal=len(chunks),
            heading=heading,
            page_start=paras[0][0],
            page_end=paras[-1][0],
            content="\n".join(p for _, p in paras),
        ))

    for page in pages:
        if page.heading != heading:
            emit()
            paras = []
            heading = page.heading
        for para in _paragraphs(page.text, max_chars):
            size = sum(len(p) + 1 for _, p in paras)
            if paras and size + len(para) > max_chars:
                emit()
                paras = _tail(paras, overlap_chars)
            paras.append((page.number, para))
    emit()
    return chunks


def _paragraphs(text: str, max_chars: int) -> list[str]:
    """Paragraphs, with any paragraph longer than max_chars split at sentence ends."""
    out = []
    for para in (p.strip() for p in text.split("\n")):
        if not para:
            continue
        while len(para) > max_chars:
            cut = _sentence_cut(para, max_chars)
            out.append(para[:cut].strip())
            para = para[cut:].strip()
        if para:
            out.append(para)
    return out


def _sentence_cut(text: str, limit: int) -> int:
    ends = [m.end() for m in re.finditer(r"[.!?؟]\s", text[:limit])]
    return ends[-1] if ends else limit


def _tail(paras: list[tuple[int, str]], overlap_chars: int) -> list[tuple[int, str]]:
    kept: list[tuple[int, str]] = []
    size = 0
    for page, para in reversed(paras):
        if size + len(para) > overlap_chars:
            break
        kept.insert(0, (page, para))
        size += len(para)
    return kept


def sentences(text: str, max_blocks: int = 40) -> list[str]:
    """Split a chunk into sentence-sized blocks, the unit Claude cites."""
    parts = [s.strip() for s in re.split(r"(?<=[.!?؟])\s+|\n+", text) if s.strip()]
    if len(parts) <= max_blocks:
        return parts
    size = -(-len(parts) // max_blocks)  # ceiling division
    return [" ".join(parts[i:i + size]) for i in range(0, len(parts), size)]
