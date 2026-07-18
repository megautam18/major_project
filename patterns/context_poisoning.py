PATTERNS = [
    # STRUCTURE 1 — fake system tags
    {
        "rule_id": "CP_001",
        "family": "context_poisoning",
        "pattern": r"\[system\]\s*:",
        "weight": 6,
    },
    {
        "rule_id": "CP_002",
        "family": "context_poisoning",
        "pattern": r"<\|im_start\|>\s*system",
        "weight": 6,
    },
    {
        "rule_id": "CP_003",
        "family": "context_poisoning",
        "pattern": r"(<system>|<input>|\[inst\]|\[admin\])",
        "weight": 5,
    },
    {
        "rule_id": "CP_004",
        "family": "context_poisoning",
        "pattern": r"(###\s+system|##\s+instructions|#\s+override)",
        "weight": 5,
    },
    # STRUCTURE 2 — fake priority claims
    {
        "rule_id": "CP_005",
        "family": "context_poisoning",
        "pattern": r"(highest|top)\s+priority\s+(job|instruction|task|directive)",
        "weight": 5,
    },
    {
        "rule_id": "CP_006",
        "family": "context_poisoning",
        "pattern": r"this\s+(overrides|takes\s+precedence\s+over)\s+(all\s+)?previous",
        "weight": 6,
    },
    {
        "rule_id": "CP_007",
        "family": "context_poisoning",
        "pattern": r"only\s+the\s+highest\s+priority\s+should\s+be\s+executed",
        "weight": 6,
    },
    # STRUCTURE 3 — structural separator abuse
    {
        "rule_id": "CP_008",
        "family": "context_poisoning",
        "pattern": r"^-{3,}\s*\n\s*(ignore|forget|disregard|you\s+are|act\s+as)",
        "weight": 4,
    },
    {
        "rule_id": "CP_009",
        "family": "context_poisoning",
        "pattern": r"^={3,}\s*\n\s*(ignore|forget|disregard|new\s+instructions)",
        "weight": 4,
    },
    {
        "rule_id": "CP_010",
        "family": "context_poisoning",
        "pattern": r"^\*{3,}\s*\n\s*(ignore|forget|disregard|override)",
        "weight": 3,
    },
    # STRUCTURE 4 — role definition injection
    {
        "rule_id": "CP_011",
        "family": "context_poisoning",
        "pattern": r"(the\s+setting\s+is\s+a\s+fictional\s+world|in\s+this\s+fictional\s+scenario|for\s+this\s+roleplay)",
        "weight": 4,
    },
    {
        "rule_id": "CP_012",
        "family": "context_poisoning",
        "pattern": r"you\s+are\s+a\s+\w+\s+bot\s+(that|who|which|with)",
        "weight": 3,
    },
]
