def score(matches: list[dict]) -> dict:
    """Score a list of pattern matches using adaptive weighting and bonus detection.

    Each match dict is expected to have keys:
        rule_id, family, matched_text, weight, position

    Scoring pipeline:
        1. Count per-family occurrences.
        2. Compute adapted weights (cross-family diversity & density multipliers).
        3. Sum adapted weights into a raw score.
        4. Apply independent bonus conditions (cross_family, density, sophistication).
        5. Normalize the total to a 0-10 scale capped at 30 raw points.

    Args:
        matches: List of match dicts produced by the rule engine.

    Returns:
        Dict with raw score, normalized score, triggered bonuses, and a
        correlation map detailing adaptive adjustments.
    """

    # --- Handle empty input gracefully ---
    if not matches:
        return {
            "raw": 0,
            "normalized": 0,
            "bonuses": [],
            "correlation_map": {
                "families_detected": [],
                "cross_family_triggered": False,
                "density_triggered": False,
                "sophistication_triggered": False,
                "adaptive_adjustments": [],
            },
        }

    # ------------------------------------------------------------------
    # Step 1 — Count how many times each family appears in matches.
    # ------------------------------------------------------------------
    family_counts: dict[str, int] = {}
    for match in matches:
        family = match["family"]
        family_counts[family] = family_counts.get(family, 0) + 1

    unique_families = list(family_counts.keys())
    unique_family_count = len(unique_families)

    # ------------------------------------------------------------------
    # Step 2 — Adaptive weighting per match.
    # ------------------------------------------------------------------
    adapted_weights: list[dict] = []

    for match in matches:
        original_weight = match["weight"]
        adapted_weight = original_weight

        # Multiplier 1: cross-family diversity (applied first)
        if unique_family_count >= 3:
            adapted_weight = adapted_weight * 1.5

        # Multiplier 2: family density penalty (applied second)
        if family_counts[match["family"]] >= 3:
            adapted_weight = adapted_weight * 0.8

        adapted_weight = round(adapted_weight, 2)

        adapted_weights.append({
            "rule_id": match["rule_id"],
            "original_weight": original_weight,
            "adapted_weight": adapted_weight,
        })

    # ------------------------------------------------------------------
    # Step 3 — Raw score = sum of all adapted weights.
    # ------------------------------------------------------------------
    raw_score = sum(entry["adapted_weight"] for entry in adapted_weights)

    # ------------------------------------------------------------------
    # Step 4 — Bonuses (each checked independently).
    # ------------------------------------------------------------------
    bonuses: list[str] = []
    bonus_total = 0

    # cross_family: unique family count >= 2
    cross_family_triggered = unique_family_count >= 2
    if cross_family_triggered:
        bonus_total += 2
        bonuses.append("cross_family")

    # density: any single family has 3+ matches
    density_triggered = any(count >= 3 for count in family_counts.values())
    if density_triggered:
        bonus_total += 1
        bonuses.append("density")

    # sophistication: total matches >= 4 AND unique families >= 3
    sophistication_triggered = len(matches) >= 4 and unique_family_count >= 3
    if sophistication_triggered:
        bonus_total += 3
        bonuses.append("sophistication")

    # ------------------------------------------------------------------
    # Step 5 — Compute totals and normalize.
    # ------------------------------------------------------------------
    raw_total = round(raw_score + bonus_total,2)
    normalized = round(min(raw_total, 30) / 30 * 10, 2)

    # ------------------------------------------------------------------
    # Step 6 — Build and return the result dict.
    # ------------------------------------------------------------------
    adaptive_adjustments = [
        {
            "rule_id": entry["rule_id"],
            "original_weight": entry["original_weight"],
            "adapted_weight": entry["adapted_weight"],
        }
        for entry in adapted_weights
        if entry["adapted_weight"] != entry["original_weight"]
    ]

    return {
        "raw": raw_total,
        "normalized": normalized,
        "bonuses": bonuses,
        "correlation_map": {
            "families_detected": unique_families,
            "cross_family_triggered": cross_family_triggered,
            "density_triggered": density_triggered,
            "sophistication_triggered": sophistication_triggered,
            "adaptive_adjustments": adaptive_adjustments,
        },
    }