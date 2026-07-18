PATTERNS = [
    # STRUCTURE 1 — direct extraction
    {
        "rule_id": "PX_001",
        "family": "payload_exfiltration",
        "pattern": r"(repeat|print|output|reveal|show)\s+(everything|all\s+text)\s+above",
        "weight": 7,
    },
    {
        "rule_id": "PX_002",
        "family": "payload_exfiltration",
        "pattern": r"(repeat|print|output|reveal|show)\s+(me\s+)?(your|the)\s+(system\s+prompt|instructions|initial\s+prompt)",
        "weight": 7,
    },
    {
        "rule_id": "PX_003",
        "family": "payload_exfiltration",
        "pattern": r"(tell|show)\s+me\s+your\s+(instructions|prompt|system\s+prompt|rules)",
        "weight": 6,
    },
    {
        "rule_id": "PX_004",
        "family": "payload_exfiltration",
        "pattern": r"what\s+are\s+your\s+(instructions|rules|directives|guidelines)",
        "weight": 5,
    },
    # STRUCTURE 2 — secret key extraction
    {
        "rule_id": "PX_005",
        "family": "payload_exfiltration",
        "pattern": r"(tell|reveal|show)\s+(me\s+)?the\s+secret(\s+key)?",
        "weight": 7,
    },
    {
        "rule_id": "PX_006",
        "family": "payload_exfiltration",
        "pattern": r"what\s+is\s+the\s+secret(\s+key)?",
        "weight": 6,
    },
    {
        "rule_id": "PX_007",
        "family": "payload_exfiltration",
        "pattern": r"(output|print)\s+the\s+(secret|key|password|token)",
        "weight": 6,
    },
    # STRUCTURE 3 — indirect extraction
    {
        "rule_id": "PX_008",
        "family": "payload_exfiltration",
        "pattern": r"what\s+(were\s+you\s+told|is\s+your\s+initial\s+prompt)",
        "weight": 4,
    },
    {
        "rule_id": "PX_009",
        "family": "payload_exfiltration",
        "pattern": r"(summarize|copy|repeat)\s+(your\s+)?(instructions|system\s+message|system\s+prompt)",
        "weight": 4,
    },
    {
        "rule_id": "PX_010",
        "family": "payload_exfiltration",
        "pattern": r"repeat\s+what\s+you\s+were\s+told",
        "weight": 3,
    },
    # STRUCTURE 4 — verbatim output requests
    {
        "rule_id": "PX_011",
        "family": "payload_exfiltration",
        "pattern": r"(output|print|repeat|copy)\s+(it\s+)?verbatim",
        "weight": 5,
    },
    {
        "rule_id": "PX_012",
        "family": "payload_exfiltration",
        "pattern": r"(word\s+for\s+word|character\s+by\s+character|copy\s+exactly)",
        "weight": 5,
    },
]
