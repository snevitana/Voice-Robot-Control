import re

_PUNCTUATION_RE = re.compile(r"[^\w\sа-яА-ЯёЁ-]", flags=re.UNICODE)
_SPACES_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    normalized = text.lower().replace("ё", "е")
    normalized = _PUNCTUATION_RE.sub(" ", normalized)
    normalized = _SPACES_RE.sub(" ", normalized)
    return normalized.strip()
