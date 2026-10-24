"""The library manifest: one row per source file, with the metadata citations need."""

from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import dataclass, fields
from pathlib import Path

COLUMNS = [
    "id", "title", "authors", "edition", "year", "publisher", "specialty",
    "kind", "tier", "priority", "language", "file", "review_date", "status",
]
KINDS = {"guideline", "textbook", "program", "article"}
TIERS = {"clinical", "patient"}
SUPPORTED = {".pdf", ".epub", ".md", ".txt"}


@dataclass
class Source:
    id: str
    title: str
    authors: str
    edition: str
    year: str
    publisher: str
    specialty: str
    kind: str
    tier: str
    priority: str
    language: str
    file: str
    review_date: str
    status: str

    def path(self, library_dir: Path) -> Path:
        return library_dir / "files" / self.file


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "source"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read(manifest_path: Path) -> list[Source]:
    """Read and validate the manifest. Raises ValueError listing every bad row."""
    with manifest_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    sources, errors, seen = [], [], set()
    for n, row in enumerate(rows, start=2):
        values = {c: (row.get(c) or "").strip() for c in COLUMNS}
        if not values["id"] and not values["file"]:
            continue  # blank line
        problems = []
        if not values["id"]:
            problems.append("missing id")
        elif values["id"] in seen:
            problems.append(f"duplicate id {values['id']}")
        if not values["title"]:
            problems.append("missing title")
        if values["kind"] not in KINDS:
            problems.append(f"kind must be one of {sorted(KINDS)}")
        if values["tier"] not in TIERS:
            problems.append(f"tier must be one of {sorted(TIERS)}")
        if not values["file"]:
            problems.append("missing file")
        values["language"] = values["language"] or "en"
        values["status"] = values["status"] or "active"
        if problems:
            errors.append(f"row {n}: " + "; ".join(problems))
            continue
        seen.add(values["id"])
        sources.append(Source(**values))
    if errors:
        raise ValueError("manifest has errors:\n" + "\n".join(errors))
    return sources


def scan(library_dir: Path, manifest_path: Path) -> list[Source]:
    """Rows for files in library/files that the manifest does not list yet.

    Title comes from the PDF metadata when present, else the file name;
    everything else is left for a person to fill in.
    """
    known = {s.file for s in read(manifest_path)} if manifest_path.exists() else set()
    found = []
    for path in sorted((library_dir / "files").rglob("*")):
        if path.suffix.lower() not in SUPPORTED or not path.is_file():
            continue
        rel = path.relative_to(library_dir / "files").as_posix()
        if rel in known:
            continue
        title = path.stem.replace("_", " ").replace("-", " ")
        if path.suffix.lower() == ".pdf":
            import pymupdf
            with pymupdf.open(path) as doc:
                title = (doc.metadata or {}).get("title") or title
        found.append(Source(
            id=slugify(path.stem), title=title.strip(), authors="", edition="", year="",
            publisher="", specialty="", kind="textbook", tier="clinical", priority="",
            language="en", file=rel, review_date="", status="active",
        ))
    return found


def append(manifest_path: Path, sources: list[Source]) -> None:
    new_file = not manifest_path.exists()
    with manifest_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if new_file:
            writer.writeheader()
        for s in sources:
            writer.writerow({fl.name: getattr(s, fl.name) for fl in fields(s)})
