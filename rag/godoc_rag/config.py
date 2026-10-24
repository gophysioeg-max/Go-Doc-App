"""Settings, read from the environment (or a .env file next to the repo)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / "rag" / ".env")


@dataclass(frozen=True)
class Settings:
    database_url: str
    library_dir: Path
    manifest_path: Path
    embedder: str  # "bge-m3" | "voyage" | "hash"
    voyage_model: str
    answer_model: str
    min_similarity: float
    chunk_chars: int
    overlap_chars: int


def load() -> Settings:
    library_dir = Path(os.getenv("GODOC_LIBRARY_DIR", REPO_ROOT / "library"))
    return Settings(
        database_url=os.getenv("DATABASE_URL", "postgresql://godoc:godoc@localhost:5432/godoc_rag"),
        library_dir=library_dir,
        manifest_path=Path(os.getenv("GODOC_MANIFEST", library_dir / "manifest.csv")),
        embedder=os.getenv("GODOC_EMBEDDER", "bge-m3"),
        voyage_model=os.getenv("GODOC_VOYAGE_MODEL", "voyage-3.5"),
        answer_model=os.getenv("GODOC_ANSWER_MODEL", "claude-opus-5-5"),
        # Below this cosine similarity the best hit is treated as "no source".
        # Tune it on real questions once the library is ingested.
        min_similarity=float(os.getenv("GODOC_MIN_SIMILARITY", "0.35")),
        chunk_chars=int(os.getenv("GODOC_CHUNK_CHARS", "2400")),
        overlap_chars=int(os.getenv("GODOC_OVERLAP_CHARS", "300")),
    )
