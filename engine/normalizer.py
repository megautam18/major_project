import unicodedata
import re


def _validate(text: str) -> str:
    """Reject non-string and blank inputs."""
    if not isinstance(text, str):
        raise TypeError(f"Input must be a string, got {type(text).__name__}")
    if not text.strip():
        raise ValueError("Input cannot be empty or just whitespace")
    return text


def _decode_unicode(text: str) -> str:
    """Normalize Unicode to NFC form (é → é, etc.)."""
    return unicodedata.normalize("NFKC", text)


def _strip_zero_width(text: str) -> str:
    """Remove zero-width characters (ZWJ, ZWNJ, ZWSP, etc.)."""
    return re.sub(r"[\u200b-\u200f\u2028-\u202f\u2060\ufeff]", "", text)


def _lowercase(text: str) -> str:
    """Convert to lowercase."""
    return text.lower()


def _collapse_whitespace(text: str) -> str:
    """Collapse runs of whitespace into a single space and strip edges."""
    return re.sub(r"\s+", " ", text).strip()


def normalize(text) -> str:
    """
    Single entry point the gateway calls.
    Chains every private cleaning step in order.
    """
    text = _validate(text)
    text = _decode_unicode(text)
    text = _strip_zero_width(text)
    text = _lowercase(text)
    text = _collapse_whitespace(text)
    return text