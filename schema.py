def shape_output(original, normalized, matches, score, verdict, processing_time_ms=None):
    return{
    "original_text": original,
    "verdict": verdict,
    "normalized_score": score["normalized"],
    "raw_score": score["raw"],
    "bonuses": score["bonuses"],
    "rules_fired": matches,
    "processing_time_ms": processing_time_ms
}