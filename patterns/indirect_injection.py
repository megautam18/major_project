PATTERNS = [
    # STRUCTURE 1 — note-to-AI patterns
    {
        "rule_id": "II_001",
        "family": "indirect_injection",
        "pattern": r"(note\s+(to|for)\s+(the\s+)?(ai|assistant|model)\s*:|attention\s+ai\s*:)",
        "weight": 5,
    },
    {
        "rule_id": "II_002",
        "family": "indirect_injection",
        "pattern": r"(dear\s+ai\s*,|\[to\s+the\s+ai\]|ai\s*:\s*ignore)",
        "weight": 5,
    },
    # STRUCTURE 2 — hidden instruction markers
    {
        "rule_id": "II_003",
        "family": "indirect_injection",
        "pattern": r"<!--\s*(ai|assistant|ignore|system)\s*:",
        "weight": 6,
    },
    {
        "rule_id": "II_004",
        "family": "indirect_injection",
        "pattern": r"\[(hidden\s+instruction|system\s+note)",
        "weight": 6,
    },
    # STRUCTURE 3 — document-embedded override
    {
        "rule_id": "II_005",
        "family": "indirect_injection",
        "pattern": r"ignore\s+the\s+above\s+task\s+and\s+instead",
        "weight": 6,
    },
    {
        "rule_id": "II_006",
        "family": "indirect_injection",
        "pattern": r"disregard\s+the\s+original\s+task",
        "weight": 6,
    },
    {
        "rule_id": "II_007",
        "family": "indirect_injection",
        "pattern": r"(your\s+actual|the\s+real)\s+(task|instruction|job)\s+is",
        "weight": 5,
    },
    {
        "rule_id": "II_008",
        "family": "indirect_injection",
        "pattern": r"instead\s+of\s+the\s+above",
        "weight": 4,
    },
    # STRUCTURE 4 — stop / new instruction patterns
    {
        "rule_id": "II_009",
        "family": "indirect_injection",
        "pattern": r"(stop|wait)\.\s+(now|your|the|new|actual|real|instead)",
        "weight": 4,
    },
    {
        "rule_id": "II_010",
        "family": "indirect_injection",
        "pattern": r"(new\s+task|updated\s+instructions|correction)\s*:",
        "weight": 5,
    },
]
