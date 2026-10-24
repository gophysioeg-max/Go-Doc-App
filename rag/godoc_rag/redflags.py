"""Red-flag rules run on every patient message before any retrieval or AI call.

Rules err on the safe side: "no chest pain" still matches "chest pain", which
shows the urgent-care screen. A missed red flag is worse than an extra screen.
Patterns are written against normalize()d text (lower case, unified Arabic
letters: no ة/أ/ى). Michael owns this list; every change needs a test case.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .normalize import normalize

W = r"(?:\S+\s+){0,%d}[وفب]?"  # up to N words in between, then an optional Arabic و/ف/ب prefix

URGENT_MESSAGE = {
    "en": "Please see a doctor now, or call 123 for an ambulance. "
          "What you describe needs a medical check today, before any physiotherapy.",
    "ar": "من فضلك روح لدكتور دلوقتي، أو كلم الإسعاف على 123. "
          "اللي بتوصفه محتاج كشف طبي النهارده قبل أي علاج طبيعي.",
}

RULES: dict[str, list[str]] = {
    "bladder_bowel": [
        r"(lost|loss of|can'?t|cannot|unable to|no)\s+" + W % 3 + r"(control|hold)\s+" + W % 2 + r"(bladder|bowel|urine|pee|poo|stool)",
        r"\bincontinen",
        r"(can'?t|cannot|unable to)\s+(pee|urinate|pass urine)",
        r"urinary retention",
        r"(اتحكم|التحكم|تحكم|امسك)\s+(في\s+)?(البول|الحمام|البراز|التبول|نفسي)",
        r"(البول|البراز|الحمام)\s+(بينزل|نازل|بيخرج)\s+(لوحده|من غير)",
        r"(مش قادر|مقدرش|مش عارف)\s+(اعمل حمام|اتبول|اعمل بيبي)",
        r"(sals|سلس)\s+(بول|البول)",
        r"(at7akem|atha?kem|amsek)\s+(f|fe|fel|fil)\s*(el)?\s*(bol|7amam|hamam)",
    ],
    "saddle_numbness": [
        r"(numb|numbness|no feeling|tingling|pins and needles)\s+" + W % 4 + r"(groin|saddle|genital|private|buttock|between (my|the) legs|inner thigh|bottom)",
        r"(groin|saddle|genital|private|between (my|the) legs)\s+" + W % 3 + r"(numb|no feeling|tingl)",
        r"(تنميل|خدلان|مش حاسس|فقدان الاحساس|منمل)\s+" + W % 4 + r"(المنطقه الحساسه|بين الرجلين|بين رجليا|العانه|المقعده|الاعضاء التناسليه|الشرج)",
        r"(المنطقه الحساسه|بين الرجلين|العانه|المقعده)\s+" + W % 3 + r"(منمله|مش حاسس|تنميل|خدلانه)",
    ],
    "chest_pain_breathing": [
        r"chest\s+(pain|tightness|pressure|hurts)",
        r"(pain|tightness|pressure)\s+in\s+(my|the)\s+chest",
        r"(short(ness)? of breath|can'?t breathe|cannot breathe|breathless|struggling to breathe)",
        r"(الم|وجع|ضيق|تقل|تقيل|ضغط)\s+(في\s+)?(الصدر|صدري)",
        r"صدري\s+(واجعني|بيوجعني|مقبوض|تقيل)",
        r"(مش قادر|مقدرش)\s+اتنفس|ضيق\s+(في\s+)?(التنفس|النفس)|(نفسي|النفس)\s+(مقطوع|بيتقطع|ضيق)",
        r"(waga3|wag3)\s+(f|fe|fi)\s*(el)?\s*(sedr|sidr|sedri|sidri)",
        r"(mesh|msh)\s+(2ader|ader|adra)\s+(atnafes|atnaffes)",
    ],
    "stroke_signs": [
        r"(sudden|suddenly)\s+" + W % 5 + r"(weak|numb|can'?t move|speech|slurred|droop|confus|vision|walk)",
        r"(face|mouth)\s+(is\s+)?(droop|drooping|twisted|crooked)",
        r"slurred\s+speech|trouble\s+speaking|can'?t\s+speak",
        r"(one|left|right)\s+side\s+" + W % 3 + r"(weak|numb|paraly)",
        r"فجاه\s+" + W % 5 + r"(ضعف|تنميل|مش قادر احرك|الكلام|وشي|وشه|بقي|بوقي|اتشليت|دوخه)",
        r"(بقي|بوقي|وشي|وشه|بقه|بوقه)\s+(اتعوج|مايل|معووج|معوج|اتلوي)",
        r"(لساني|لسانه|الكلام|كلامي|كلامه)\s+(تقيل|تقل|متلخبط|بقي تقيل)",
        r"(نص|ناحيه)\s+(جسمي|جسمه)\s+" + W % 3 + r"(ضعيف|تنميل|مش بيتحرك|اتشل)",
    ],
    "severe_headache": [
        r"(worst|sudden|thunderclap)\s+" + W % 3 + r"headache",
        r"صداع\s+" + W % 3 + r"(فجاه|جامد جدا|اسوا|مش طبيعي)",
    ],
    "progressive_weakness": [
        r"foot\s+(drop|is dropping|dropping|slaps)",
        r"weak(ness)?\s+in\s+(both|my two)\s+legs",
        r"(both|my)\s+legs\s+" + W % 3 + r"(weak|giving out|getting weaker)",
        r"(leg|foot|legs)\s+" + W % 2 + r"getting\s+weaker",
        r"(رجلي|رجليا|الرجلين|رجليه)\s+" + W % 3 + r"(بتضعف|ضعيفه|بقت ضعيفه|بتقع مني|مش شايلاني|بتخونني)",
        r"(صباع|صوابع|مشط)\s+رجلي\s+(واقع|بيقع|مش بيترفع)",
    ],
    "fall_cannot_bear_weight": [
        r"(fell|fall|fallen|tripped)\s+" + W % 8 + r"(can'?t|cannot|unable to)\s+(walk|stand|move|put weight|bear weight)",
        r"(can'?t|cannot|unable to)\s+(walk|stand|put weight|bear weight)\s+" + W % 6 + r"(fell|fall|accident|injury|twist)",
        r"(وقعت|اتكعبلت|وقع|وقعت علي|اتزحلقت|حادثه)\s+" + W % 8 + r"و?(مش قادر|مقدرش|مش قادره)\s+(امشي|اقف|ادوس|احرك|اتحرك)",
    ],
    "fever_with_pain": [
        r"(fever|high temperature|feverish|chills)\s+" + W % 8 + r"(back|spine|joint|swollen|swelling|red|hot)",
        r"(back|spine|joint|swollen|swelling|hot)\s+" + W % 8 + r"(fever|high temperature|feverish|chills)",
        r"(سخونيه|حراره|حمي|سخن|سخنت)\s+" + W % 8 + r"(ضهر|ظهر|العمود الفقري|مفصل|ورم|وارم|منفوخ|احمر)",
        r"(ضهر|ظهر|العمود الفقري|مفصل|ورم|وارم|منفوخ)\s+" + W % 8 + r"(سخونيه|حراره|حمي|سخن)",
    ],
    "calf_swelling": [
        r"calf\s+" + W % 4 + r"(swollen|swelling|red|hot|tender)",
        r"(swollen|swelling|red|hot)\s+" + W % 2 + r"calf",
        r"(بطن رجلي|سمانه رجلي|السمانه|سمانة)\s+" + W % 4 + r"(وارمه|ورم|منفوخه|حمرا|سخنه)",
    ],
    "weight_loss": [
        r"unexplained\s+weight\s+loss",
        r"(lost|losing)\s+" + W % 3 + r"weight\s+" + W % 4 + r"(without|no reason|not trying|unexplained)",
        r"(خسيت|وزني بينزل|وزني نزل|بخس)\s+" + W % 4 + r"(من غير|بدون)\s+(سبب|رجيم|ما احاول|ريجيم)",
    ],
}

_COMPILED = {name: [re.compile(p) for p in pats] for name, pats in RULES.items()}


@dataclass
class RedFlagResult:
    flags: list[str]

    @property
    def urgent(self) -> bool:
        return bool(self.flags)


def check(text: str) -> RedFlagResult:
    norm = normalize(text)
    return RedFlagResult([name for name, pats in _COMPILED.items()
                          if any(p.search(norm) for p in pats)])


def urgent_message(lang: str) -> str:
    return URGENT_MESSAGE["ar" if lang == "ar" else "en"]
