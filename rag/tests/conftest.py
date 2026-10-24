import os
from pathlib import Path

import pymupdf
import pytest

TEST_DB = os.getenv("TEST_DATABASE_URL", "postgresql://godoc:godoc@localhost:5432/godoc_rag")


def make_pdf(path: Path, pages: list[tuple[str, str]], toc: list[list]) -> Path:
    """pages: (running header, body) per page. toc: [[level, title, page], ...]."""
    doc = pymupdf.open()
    for header, body in pages:
        page = doc.new_page()
        page.insert_text((72, 40), header, fontsize=8)
        page.insert_textbox(pymupdf.Rect(72, 72, 520, 780), body, fontsize=10)
    doc.set_toc(toc)
    doc.save(path)
    doc.close()
    return path


HEEL_PAGES = [
    ("Go Doc Home PT Program", "Plantar heel pain is pain under the heel that is worst with the first steps in the morning. "
     "It often eases after a few minutes of walking and returns after rest."),
    ("Go Doc Home PT Program", "Assessment. Palpate the medial calcaneal tubercle. Measure ankle dorsiflexion with the knee straight. "
     "Ask about first-step pain on a scale from 0 to 10."),
    ("Go Doc Home PT Program", "Phase 1 exercises. Towel calf stretch, three holds of 30 seconds, twice a day. "
     "Plantar fascia stretch before the first steps in the morning."),
    ("Go Doc Home PT Program", "Phase 2 exercises. Calf raises on a step, three sets of 12, every other day. "
     "Progress when first-step pain is 3 out of 10 or less."),
] * 3  # 12 pages, so the running header is detected as repeated

HEEL_TOC = [
    [1, "Plantar heel pain", 1],
    [2, "Assessment", 2],
    [2, "Exercises", 3],
    [3, "Phase 2", 4],
]


@pytest.fixture
def heel_pdf(tmp_path: Path) -> Path:
    return make_pdf(tmp_path / "heel.pdf", HEEL_PAGES, HEEL_TOC)


@pytest.fixture
def db_url() -> str:
    try:
        import psycopg

        with psycopg.connect(TEST_DB, connect_timeout=3):
            pass
    except Exception:
        pytest.skip("test database not reachable")
    return TEST_DB
