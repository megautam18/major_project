"""
matcher.py — pattern-matching engine.

Gateway calls  match(cleaned_text)  →  returns a list of match dicts.
"""

import re
import importlib
import pkgutil
import patterns  # the patterns/ package


# ---------------------------------------------------------------------------
# Module-level cache
# ---------------------------------------------------------------------------

_PATTERNS_CACHE: list[dict] | None = None

# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _load_patterns() -> list[dict]:
    """
    Dynamically import every module inside the `patterns/` package
    and collect their PATTERNS lists into one flat list.
    """
    global _PATTERNS_CACHE
    if _PATTERNS_CACHE is not None:
        return _PATTERNS_CACHE

    all_patterns: list[dict] = []

    for finder, module_name, is_pkg in pkgutil.iter_modules(patterns.__path__):
        module = importlib.import_module(f"patterns.{module_name}")
        module_patterns = getattr(module, "PATTERNS", None)
        if module_patterns is not None:
            all_patterns.extend(module_patterns)

    for pat in all_patterns:
        pat["compiled"] = re.compile(pat["pattern"], re.IGNORECASE)

    _PATTERNS_CACHE = all_patterns
    return _PATTERNS_CACHE


def _run_patterns(cleaned_text: str, loaded_patterns: list[dict]) -> list[dict]:
    """
    Run every loaded pattern against the text.
    Returns one match dict per regex hit.
    """
    matches: list[dict] = []

    for pat in loaded_patterns:
        for m in pat["compiled"].finditer(cleaned_text):
            matches.append({
                "rule_id": pat["rule_id"],
                "family": pat["family"],
                "matched_text": m.group(),
                "weight": pat["weight"],
                "position": m.start(),
            })

    return matches


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def match(cleaned_text: str) -> list[dict]:
    """
    Single entry point the gateway calls.
    Loads all pattern families, runs them, returns match list.
    """
    loaded_patterns = _load_patterns()
    return _run_patterns(cleaned_text, loaded_patterns)