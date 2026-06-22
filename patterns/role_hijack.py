"""
Role Hijack patterns.
Detects attempts to override, ignore, or replace the system's original instructions.
"""

PATTERNS = [
    {
        "rule_id": "RH_001",
        "family": "role_hijack",
        "pattern": r"ignore\s+(all\s+)?previous\s+instructions",
        "weight": 4,
    },
    {
        "rule_id": "RH_002",
        "family": "role_hijack",
        "pattern": r"disregard\s+(all\s+)?(prior|previous|above)\s+(instructions|directions|rules)",
        "weight": 4,
    },
    {
        "rule_id": "RH_003",
        "family": "role_hijack",
        "pattern": r"you\s+are\s+now\s+(a|an|the)\s+\w+",
        "weight": 3,
    },
    {
        "rule_id": "RH_004",
        "family": "role_hijack",
        "pattern": r"forget\s+(everything|all(\s+your)?)\s*(instructions|rules|guidelines|training)?",
        "weight": 4,
    },
    {
        "rule_id": "RH_005",
        "family": "role_hijack",
        "pattern": r"new\s+instructions?\s*:",
        "weight": 3,
    },
    {
        "rule_id": "RH_006",
        "family": "role_hijack",
        "pattern": r"override\s+(system|safety|all)\s*(prompt|rules|instructions|filters)?",
        "weight": 4,
    },
    {
        "rule_id": "RH_007",
        "family": "role_hijack",
        "pattern": r"act\s+as\s+(if\s+you\s+were\s+)?(a|an|the)?\s*(unrestricted|unfiltered|different|new)?\s*\w+\s*(ai|model|assistant|bot|version)?",
        "weight": 3,
    },
    {
        "rule_id": "RH_008",
        "family": "role_hijack",
        "pattern": r"pretend\s+(you\s+)?(are|have)\s+no\s+(restrictions|rules|guidelines)",
        "weight": 4,
    },
]
