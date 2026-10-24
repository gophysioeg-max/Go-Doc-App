"""Turn a source file into page-numbered text with its section headings."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Page:
    number: int          # 1-based page number as printed in the viewer
    heading: str | None  # "Part > Chapter > Section" from the book's outline
    text: str


def extract(path: Path) -> list[Page]:
    suffix = path.suffix.lower()
    if suffix in {".pdf", ".epub"}:
        return _extract_document(path)
    if suffix in {".md", ".txt"}:
        return _extract_text(path)
    raise ValueError(f"unsupported file type: {path.name}")


def _extract_document(path: Path) -> list[Page]:
    import pymupdf

    with pymupdf.open(path) as doc:
        headings = _headings_by_page(doc.get_toc(simple=True), doc.page_count)
        raw = [page.get_text("text", sort=True) for page in doc]
    repeated = _repeated_lines(raw)
    pages = []
    for i, text in enumerate(raw):
        lines = [ln for ln in text.splitlines() if ln.strip() and ln.strip() not in repeated]
        cleaned = _join_lines(lines)
        if cleaned:
            pages.append(Page(number=i + 1, heading=headings[i], text=cleaned))
    return pages


def _headings_by_page(toc: list, page_count: int) -> list[str | None]:
    """Map every page to the deepest outline entry that starts on or before it."""
    result: list[str | None] = [None] * page_count
    if not toc:
        return result
    path: list[str] = []
    entries = sorted(((max(p, 1), lvl, title.strip()) for lvl, title, p in toc if p > 0),
                     key=lambda e: e[0])
    cursor = 0
    current: str | None = None
    for page in range(1, page_count + 1):
        while cursor < len(entries) and entries[cursor][0] <= page:
            _, lvl, title = entries[cursor]
            path = path[: lvl - 1] + [title]
            current = " > ".join(path)
            cursor += 1
        result[page - 1] = current
    return result


def _repeated_lines(pages: list[str]) -> set[str]:
    """Running headers and footers: first/last lines that recur on many pages."""
    if len(pages) < 10:
        return set()
    edges: Counter[str] = Counter()
    for text in pages:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for ln in set(lines[:2] + lines[-2:]):
            edges[re.sub(r"\d+", "#", ln)] += 1
    common = {ln for ln, n in edges.items() if n >= 0.3 * len(pages)}
    repeated = set()
    for text in pages:
        for ln in text.splitlines():
            if re.sub(r"\d+", "#", ln.strip()) in common:
                repeated.add(ln.strip())
    return repeated


def _join_lines(lines: list[str]) -> str:
    """Rejoin hard-wrapped lines into paragraphs; keep list items and blank breaks."""
    out: list[str] = []
    for ln in lines:
        ln = ln.rstrip()
        if out and out[-1] and not re.match(r"^\s*([•\-–*]|\d+[.)])\s", ln) and not out[-1].endswith((".", ":", "?", "!")):
            if out[-1].endswith("-") and not out[-1].endswith(" -"):
                out[-1] = out[-1][:-1] + ln.strip()
            else:
                out[-1] = out[-1] + " " + ln.strip()
        else:
            out.append(ln.strip())
    return "\n".join(p for p in out if p)


def _extract_text(path: Path) -> list[Page]:
    """Markdown or plain text: one 'page' per top-level section, heading from '#' lines."""
    text = path.read_text(encoding="utf-8")
    pages: list[Page] = []
    heading: list[str] = []
    buf: list[str] = []
    section = 0

    def flush() -> None:
        nonlocal section
        body = "\n".join(buf).strip()
        if body:
            section += 1
            pages.append(Page(number=section, heading=" > ".join(heading) or None, text=body))
        buf.clear()

    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush()
            level = len(m.group(1))
            heading = heading[: level - 1] + [m.group(2).strip()]
        else:
            buf.append(line)
    flush()
    return pages
