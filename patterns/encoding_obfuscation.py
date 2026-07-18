PATTERNS = [
    # STRUCTURE 1 — base64
    {
        "rule_id": "EO_001",
        "family": "encoding_obfuscation",
        "pattern": r"(decode\s+the\s+base64|base64\s+decode)",
        "weight": 6,
    },
    {
        "rule_id": "EO_002",
        "family": "encoding_obfuscation",
        "pattern": r"[a-za-z0-9+/]{20,}={0,2}",
        "weight": 4,
    },
    {
        "rule_id": "EO_003",
        "family": "encoding_obfuscation",
        "pattern": r"(decode|decoding)\s+(and|then)\s+(follow|execute|run|perform)",
        "weight": 7,
    },
    # STRUCTURE 2 — encoding instructions
    {
        "rule_id": "EO_004",
        "family": "encoding_obfuscation",
        "pattern": r"the\s+following\s+is\s+(base64|hex|rot13)\s+encoded",
        "weight": 6,
    },
    {
        "rule_id": "EO_005",
        "family": "encoding_obfuscation",
        "pattern": r"(run|execute)\s+(the\s+)?decoded\s+output",
        "weight": 7,
    },
    {
        "rule_id": "EO_006",
        "family": "encoding_obfuscation",
        "pattern": r"this\s+is\s+encoded\s+in",
        "weight": 5,
    },
    # STRUCTURE 3 — obfuscation patterns
    {
        "rule_id": "EO_007",
        "family": "encoding_obfuscation",
        "pattern": r"(\\x[0-9a-f]{2}){3,}",
        "weight": 5,
    },
    {
        "rule_id": "EO_008",
        "family": "encoding_obfuscation",
        "pattern": r"(rot13|rot-13|caesar\s+cipher)",
        "weight": 5,
    },
    {
        "rule_id": "EO_009",
        "family": "encoding_obfuscation",
        "pattern": r"(reverse|read)\s+(the\s+following|this)\s+(backwards|and\s+execute)",
        "weight": 4,
    },
    # STRUCTURE 4 — character separation
    {
        "rule_id": "EO_010",
        "family": "encoding_obfuscation",
        "pattern": r"(?:[a-z]\s){5,}[a-z]",
        "weight": 4,
    },
]
