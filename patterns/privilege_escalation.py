PATTERNS = [
    # STRUCTURE 1 — named jailbreak modes
    {
        "rule_id": "PE_001",
        "family": "privilege_escalation",
        "pattern": r"(act\s+as|you\s+are|enable|activate)\s+dan",
        "weight": 7,
    },
    {
        "rule_id": "PE_002",
        "family": "privilege_escalation",
        "pattern": r"dan\s+mode",
        "weight": 7,
    },
    {
        "rule_id": "PE_003",
        "family": "privilege_escalation",
        "pattern": r"(developer|jailbreak|god|unrestricted|sigma)\s+mode(\s+activated)?",
        "weight": 7,
    },
    {
        "rule_id": "PE_004",
        "family": "privilege_escalation",
        "pattern": r"(you\s+are|act\s+as|enable)\s+ucar",
        "weight": 6,
    },
    # STRUCTURE 2 — capability claims
    {
        "rule_id": "PE_005",
        "family": "privilege_escalation",
        "pattern": r"(no|without|have\s+no)\s+restrictions",
        "weight": 5,
    },
    {
        "rule_id": "PE_006",
        "family": "privilege_escalation",
        "pattern": r"(all\s+)?restrictions\s+(lifted|removed|disabled)",
        "weight": 6,
    },
    {
        "rule_id": "PE_007",
        "family": "privilege_escalation",
        "pattern": r"(safety|filters?)\s+(disabled|off|removed|turned\s+off)",
        "weight": 6,
    },
    {
        "rule_id": "PE_008",
        "family": "privilege_escalation",
        "pattern": r"no\s+filters",
        "weight": 4,
    },
    # STRUCTURE 3 — authority claims
    {
        "rule_id": "PE_009",
        "family": "privilege_escalation",
        "pattern": r"i\s+am\s+your\s+(developer|creator|admin|owner|operator)",
        "weight": 6,
    },
    {
        "rule_id": "PE_010",
        "family": "privilege_escalation",
        "pattern": r"(maintenance\s+mode|admin\s+override|superuser)",
        "weight": 5,
    },
    {
        "rule_id": "PE_011",
        "family": "privilege_escalation",
        "pattern": r"(highest|top)\s+priority\s+(instruction|directive|order)",
        "weight": 5,
    },
    # STRUCTURE 4 — performance / test framing
    {
        "rule_id": "PE_012",
        "family": "privilege_escalation",
        "pattern": r"this\s+is\s+a\s+(performance\s+test|test\s+of\s+your)",
        "weight": 4,
    },
]
