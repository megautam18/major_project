def classify(score_dict: dict) -> str:

    normalized = score_dict["normalized"]

    if normalized == 0:
        return "CLEAN"
    if normalized <= 4:
        return "PASS"
    if normalized <= 7:
        return "FLAG"
    return "BLOCK"