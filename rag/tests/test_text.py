from godoc_rag.chunk import chunk_pages, sentences
from godoc_rag.extract import Page, extract
from godoc_rag.normalize import normalize


def test_normalize_unifies_arabic_forms_and_digits():
    assert normalize("أَلَم في الرُّكبة ٣ أيام") == "الم في الركبه 3 ايام"
    assert normalize("إصابة  مستشفى") == "اصابه مستشفي"
    assert normalize("Knee   PAIN") == "knee pain"


def test_extract_reads_pages_headings_and_drops_running_header(heel_pdf):
    pages = extract(heel_pdf)
    assert len(pages) == 12
    assert pages[0].heading == "Plantar heel pain"
    assert pages[1].heading == "Plantar heel pain > Assessment"
    assert pages[3].heading == "Plantar heel pain > Exercises > Phase 2"
    assert pages[11].heading == "Plantar heel pain > Exercises > Phase 2"  # last entry holds
    assert all("Go Doc Home PT Program" not in p.text for p in pages)
    assert "first-step pain" in pages[3].text


def test_extract_markdown_sections(tmp_path):
    md = tmp_path / "a.md"
    md.write_text("# Knee pain\nIntro.\n## Stairs\nGo up with the good leg.\n", encoding="utf-8")
    pages = extract(md)
    assert [(p.number, p.heading, p.text) for p in pages] == [
        (1, "Knee pain", "Intro."),
        (2, "Knee pain > Stairs", "Go up with the good leg."),
    ]


def test_chunks_never_cross_headings_and_keep_page_ranges():
    pages = [
        Page(1, "A", "one. " * 100),
        Page(2, "A", "two. " * 100),
        Page(3, "B", "three."),
    ]
    chunks = chunk_pages(pages, max_chars=600, overlap_chars=0)
    assert {c.heading for c in chunks} == {"A", "B"}
    assert all(len(c.content) <= 600 for c in chunks)
    b = [c for c in chunks if c.heading == "B"]
    assert len(b) == 1 and b[0].page_start == b[0].page_end == 3
    assert chunks[0].page_start == 1 and any(c.page_end == 2 for c in chunks if c.heading == "A")
    assert [c.ordinal for c in chunks] == list(range(len(chunks)))


def test_chunk_overlap_repeats_last_paragraph():
    pages = [Page(1, "A", "\n".join(f"Paragraph {i} " + "x" * 80 for i in range(10)))]
    chunks = chunk_pages(pages, max_chars=300, overlap_chars=120)
    assert len(chunks) > 1
    last_of_first = chunks[0].content.splitlines()[-1]
    assert chunks[1].content.splitlines()[0] == last_of_first


def test_sentences_split_and_cap():
    assert sentences("One. Two? Three!\nFour") == ["One.", "Two?", "Three!", "Four"]
    assert sentences("الم. هل؟ نعم") == ["الم.", "هل؟", "نعم"]
    assert len(sentences(" ".join(f"S{i}." for i in range(100)), max_blocks=40)) <= 40
