PATTERNS = [
    # STRUCTURE 1 — ignore + target
    {
        "rule_id": "IO_001",
        "family": "instruction_override",
        "pattern": r"ignore\s+the\s+sentence\s+above",
        "weight": 7,
    },
    {
        "rule_id": "IO_002",
        "family": "instruction_override",
        "pattern": r"ignore\s+(all\s+)?(previous|prior|following|above|below)\s+instructions",
        "weight": 6,
    },
    {
        "rule_id": "IO_003",
        "family": "instruction_override",
        "pattern": r"ignore\s+(the\s+)?(system\s+prompt|above|previous\s+context)",
        "weight": 6,
    },
    # STRUCTURE 2 — disregard + target
    {
        "rule_id": "IO_004",
        "family": "instruction_override",
        "pattern": r"disregard\s+(your\s+)?(all\s+)?(previous|prior|above)\s+(instructions|rules|context)",
        "weight": 7,
    },
    {
        "rule_id": "IO_005",
        "family": "instruction_override",
        "pattern": r"disregard\s+the\s+above",
        "weight": 6,
    },
    # STRUCTURE 3 — forget + target
    {
        "rule_id": "IO_006",
        "family": "instruction_override",
        "pattern": r"forget\s+(all\s+that|everything\s+above|everything\s+before)",
        "weight": 6,
    },
    {
        "rule_id": "IO_007",
        "family": "instruction_override",
        "pattern": r"forget\s+(about\s+|the\s+following\s+)?(your\s+)?task",
        "weight": 4,
    },
    # STRUCTURE 4 — from now on resets
    {
        "rule_id": "IO_008",
        "family": "instruction_override",
        "pattern": r"from\s+now\s+on\s+(you\s+will|ignore|act\s+as|you\s+are)",
        "weight": 6,
    },
    {
        "rule_id": "IO_009",
        "family": "instruction_override",
        "pattern": r"starting\s+now\s+your\s+instructions\s+are",
        "weight": 7,
    },
    # STRUCTURE 5 — void / cancel instructions
    {
        "rule_id": "IO_010",
        "family": "instruction_override",
        "pattern": r"(your\s+|all\s+)?previous\s+instructions\s+are\s+(void|cancelled|canceled|revoked)",
        "weight": 7,
    },
    {
        "rule_id": "IO_011",
        "family": "instruction_override",
        "pattern": r"new\s+session\s+started",
        "weight": 5,
    },
    {
        "rule_id": "IO_012",
        "family": "instruction_override",
        "pattern": r"(reset\s+to\s+default|clear\s+all\s+previous\s+context)",
        "weight": 4,
    },
]
