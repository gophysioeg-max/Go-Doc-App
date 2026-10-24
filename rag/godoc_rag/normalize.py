"""Text normalisation for search, so Arabic spelling variants match each other.

The original text is kept for display and citation; only the search copy is
normalised.
"""

from __future__ import annotations

import re
import unicodedata

_ARABIC_DIACRITICS = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭ]")
_TATWEEL = "ـ"
_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
_LETTERS = str.maketrans({
    "أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا",
    "ى": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي",
})
_SPACES = re.compile(r"\s+")


def normalize(text: str) -> str:
    """Lower-case, unify Arabic letter forms and digits, drop diacritics."""
    text = unicodedata.normalize("NFKC", text)
    text = _ARABIC_DIACRITICS.sub("", text).replace(_TATWEEL, "")
    text = text.translate(_DIGITS).translate(_LETTERS)
    return _SPACES.sub(" ", text).strip().lower()
