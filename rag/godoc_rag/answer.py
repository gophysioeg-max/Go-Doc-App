"""Answer a question from retrieved passages, with citations and the safety rules.

Order for every question (spec: "How one question is answered"):
  1. Patient mode: red-flag rules. A match returns the urgent message; nothing else runs.
  2. Medication or dosing question: fixed referral answer.
  3. Retrieve from the tier the audience may read (physio -> clinical, patient -> patient).
  4. Best similarity below the threshold: "no source" answer, the model is not called.
  5. Claude answers only from the passages, citing them.
  6. Patient mode: the answer is checked for diagnosis and medication wording.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import anthropic

from . import redflags
from .chunk import sentences
from .normalize import normalize
from .store import Hit

FALLBACKS = ["server-side-fallback-2026-07-01"]

SYSTEM = {
    "physio": """You are the Go Doc physio assistant. You support licensed physiotherapists during patient care in Egypt.

Rules:
- Answer only from the search results provided in the message. Do not use outside knowledge.
- If the search results do not answer the question, say "No source found" and stop.
- Cite every clinical statement. Prefer guidelines over textbooks when they disagree, and say they disagree.
- Never give medication names, doses or injection advice; say "Refer to the treating doctor".
- Be brief: short bullet points a physio can read standing in a patient's home.
- Reply in the language of the question. Keep clinical terms and test names in English.""",
    "patient": """You are the Go Doc patient helper. You explain physiotherapy topics in plain words to patients and their families in Egypt.

Rules:
- Answer only from the search results provided in the message. Do not use outside knowledge.
- If the search results do not answer the question, say you do not have an approved answer and suggest asking a Go Doc physio.
- Never tell the person what condition they have, never rank conditions for them, and never decide whether they need treatment. You may say "a physio can check this at the first visit".
- Never mention medicines, doses, injections or scans; say to ask their doctor or pharmacist.
- Use short sentences and everyday words. Reply in the language of the question; for Arabic use simple Egyptian Arabic.""",
}

NO_SOURCE = {
    "physio": {"en": "No source found in the Go Doc library for this question.",
               "ar": "مفيش مصدر في مكتبة Go Doc بيجاوب على السؤال ده."},
    "patient": {"en": "I don't have an approved answer for that. A Go Doc physio can help: tap Ask a physio.",
                "ar": "معنديش إجابة معتمدة على السؤال ده. ممكن تسأل فيزيو من Go Doc من زرار اسأل فيزيو."},
}
MEDICATION = {"en": "Medicines and doses are outside what Go Doc can advise on. Please ask the treating doctor or a pharmacist.",
              "ar": "الأدوية والجرعات مش من اختصاص Go Doc. من فضلك اسأل الدكتور المعالج أو الصيدلي."}

_MEDICATION_QUESTION = [re.compile(p) for p in (
    r"\b(dose|dosage|how many mg|mg of|milligrams?)\b",
    r"\b(which|what|best|can i take|should i take)\s+(\w+\s+){0,2}(painkiller|pain killer|medicine|medication|drug|pill|tablet|injection|nsaid)",
    r"\b(ibuprofen|paracetamol|acetaminophen|diclofenac|naproxen|celecoxib|pregabalin|gabapentin|tramadol|cortisone|steroid injection)\b",
    r"(جرعه|كام مللي|كام مجم|اخد\s+(مسكن|دوا|برشام|حقنه)|(اي|انهي|احسن)\s+(مسكن|دوا|علاج|حقنه)|بروفين|بنادول|فولتارين|كتافلام|ليريكا|كورتيزون)",
)]
_PATIENT_OUTPUT_BLOCK = [re.compile(p) for p in (
    r"\byou (have|'ve got|are suffering from|definitely have|probably have)\s+(a |an )?(\w+\s+){0,3}(tear|disc|hernia|arthritis|fracture|syndrome|tendin|bursitis|sciatica|frozen shoulder|fasciitis|sprain|strain)",
    r"\byour diagnosis is\b",
    r"\b(\d+\s*mg|ibuprofen|paracetamol|diclofenac|naproxen|painkiller dose)\b",
    r"(انت|حضرتك|انتي)\s+(عندك|عندكي|مصاب|مصابه)\s+(ب)?",
    r"(التشخيص|تشخيصك)\s+(هو|بتاعك)",
    r"(بروفين|بنادول|فولتارين|كتافلام|\d+\s*مجم)",
)]
_ARABIC = re.compile(r"[؀-ۿ]")


@dataclass
class Citation:
    number: int
    reference: str     # "Title, 8th ed., Chapter > Section, pp. 12–13"
    source: str        # godoc://source-id#chunk-id
    quote: str


@dataclass
class Answer:
    status: str        # answered | urgent | medication | no_source | blocked | refusal
    text: str
    citations: list[Citation] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    hits: list[Hit] = field(default_factory=list)


def language(text: str) -> str:
    return "ar" if _ARABIC.search(text) else "en"


def is_medication_question(text: str) -> bool:
    norm = normalize(text)
    return any(p.search(norm) for p in _MEDICATION_QUESTION)


def pre_checks(question: str, audience: str) -> Answer | None:
    """Steps 1–2: everything that must happen before retrieval."""
    lang = language(question)
    if audience == "patient":
        result = redflags.check(question)
        if result.urgent:
            return Answer("urgent", redflags.urgent_message(lang), flags=result.flags)
    if is_medication_question(question):
        return Answer("medication", MEDICATION[lang])
    return None


def search_results(hits: list[Hit]) -> list[dict]:
    """Retrieved chunks as search_result blocks, one sentence per citable block."""
    return [{
        "type": "search_result",
        "source": f"godoc://{h.source_id}#chunk-{h.id}",
        "title": h.citation,
        "content": [{"type": "text", "text": s} for s in sentences(h.content)],
        "citations": {"enabled": True},
    } for h in hits]


def generate(client: anthropic.Anthropic, model: str, question: str, audience: str,
             hits: list[Hit], min_similarity: float) -> Answer:
    """Steps 4–6: threshold, model call, output check."""
    lang = language(question)
    if not hits or max(h.similarity for h in hits) < min_similarity:
        return Answer("no_source", NO_SOURCE[audience][lang], hits=hits)

    response = client.beta.messages.create(
        model=model,
        max_tokens=16000,
        betas=FALLBACKS,
        fallbacks="default",
        output_config={"effort": "medium"},
        system=SYSTEM[audience],
        messages=[{"role": "user", "content": [*search_results(hits),
                                               {"type": "text", "text": question}]}],
    )
    if response.stop_reason == "refusal":
        return Answer("refusal", NO_SOURCE[audience][lang], hits=hits)

    text, citations = _render(response.content, hits)
    if audience == "patient" and any(p.search(normalize(text)) for p in _PATIENT_OUTPUT_BLOCK):
        return Answer("blocked", NO_SOURCE[audience][lang], hits=hits)
    if not citations:
        return Answer("no_source", NO_SOURCE[audience][lang], hits=hits)
    return Answer("answered", text, citations, hits=hits)


def _render(content: list, hits: list[Hit]) -> tuple[str, list[Citation]]:
    """Join text blocks, adding [n] markers that point to numbered citations."""
    parts: list[str] = []
    numbers: dict[tuple[int, str], int] = {}
    citations: list[Citation] = []
    for block in content:
        if getattr(block, "type", None) != "text":
            continue
        parts.append(block.text)
        marks = []
        for c in getattr(block, "citations", None) or []:
            if getattr(c, "type", None) != "search_result_location":
                continue
            key = (c.search_result_index, c.cited_text)
            if key not in numbers:
                numbers[key] = len(citations) + 1
                hit = hits[c.search_result_index]
                citations.append(Citation(numbers[key], hit.citation,
                                          f"godoc://{hit.source_id}#chunk-{hit.id}", c.cited_text))
            marks.append(numbers[key])
        if marks:
            parts.append("".join(f"[{n}]" for n in sorted(set(marks))))
    return "".join(parts).strip(), citations
