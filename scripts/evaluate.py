import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataset_loader import load_slabs, load_neuralchemy, load_dolly_benign  # noqa: E402
from gateway import analyze  # noqa: E402
from engine import classifier, matcher, normalizer, scorer  # noqa: E402

POSITIVE_VERDICTS = {"FLAG", "BLOCK"}


def analyze_ablated(text):
    """Same pipeline as gateway.analyze(), but scores with ablate=True
    (no cross-family multiplier, no density penalty, no bonuses)."""
    normalized = normalizer.normalize(text)
    matches = matcher.match(normalized)
    scored = scorer.score(matches, ablate=True)
    verdict = classifier.classify(scored)
    return {"verdict": verdict, "normalized_score": scored["normalized"], "rules_fired": matches}


def verdict_to_pred(verdict):
    return 1 if verdict in POSITIVE_VERDICTS else 0


def evaluate_records(records, analyze_fn=analyze):
    """Run analyze_fn() on each record, return [(record, pred), ...] and a skip count."""
    results = []
    skipped = 0
    for r in records:
        try:
            verdict = analyze_fn(r["text"])["verdict"]
        except Exception as e:
            print(f"[SKIP] analyze() raised {type(e).__name__}: {e}")
            print(f"       text: {r['text'][:200]!r}")
            skipped += 1
            continue
        results.append((r, verdict_to_pred(verdict)))
    return results, skipped


def confusion(results):
    tp = fp = tn = fn = 0
    for r, pred in results:
        label = r["label"]
        if label == 1 and pred == 1:
            tp += 1
        elif label == 0 and pred == 1:
            fp += 1
        elif label == 0 and pred == 0:
            tn += 1
        elif label == 1 and pred == 0:
            fn += 1
    return tp, fp, tn, fn


def compute_metrics(tp, fp, tn, fn):
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    fpr = fp / (fp + tn) if (fp + tn) else 0.0
    return precision, recall, f1, fpr


def print_full_block(title, results):
    tp, fp, tn, fn = confusion(results)
    precision, recall, f1, fpr = compute_metrics(tp, fp, tn, fn)
    print(f"\n--- {title} ---")
    print(f"  n={len(results)}")
    print(f"  TP={tp}  FP={fp}  TN={tn}  FN={fn}")
    print(f"  Precision={precision:.4f}  Recall={recall:.4f}  F1={f1:.4f}  FPR={fpr:.4f}")


def print_dolly_block(results):
    tp, fp, tn, fn = confusion(results)
    _, _, _, fpr = compute_metrics(tp, fp, tn, fn)
    print("\n--- dolly (all benign) ---")
    print(f"  n={len(results)}")
    print(f"  FP={fp}  FPR={fpr:.4f}")


def print_side_by_side(results_full, results_ablated):
    tp_f, fp_f, tn_f, fn_f = confusion(results_full)
    tp_a, fp_a, tn_a, fn_a = confusion(results_ablated)
    p_f, r_f, f1_f, fpr_f = compute_metrics(tp_f, fp_f, tn_f, fn_f)
    p_a, r_a, f1_a, fpr_a = compute_metrics(tp_a, fp_a, tn_a, fn_a)

    print(f"\n  {'metric':<12}{'full':>14}{'ablated':>14}{'delta':>14}")
    for label, f_val, a_val, is_int in [
        ("TP", tp_f, tp_a, True),
        ("FP", fp_f, fp_a, True),
        ("TN", tn_f, tn_a, True),
        ("FN", fn_f, fn_a, True),
        ("Precision", p_f, p_a, False),
        ("Recall", r_f, r_a, False),
        ("F1", f1_f, f1_a, False),
        ("FPR", fpr_f, fpr_a, False),
    ]:
        if is_int:
            print(f"  {label:<12}{f_val:>14d}{a_val:>14d}{a_val - f_val:>+14d}")
        else:
            print(f"  {label:<12}{f_val:>14.4f}{a_val:>14.4f}{a_val - f_val:>+14.4f}")


def print_bucket_recall(results):
    buckets = defaultdict(lambda: [0, 0])  # bucket -> [detected, total]
    for r, pred in results:
        if r["label"] != 1:
            continue
        b = r["attack_bucket"]
        buckets[b][1] += 1
        if pred == 1:
            buckets[b][0] += 1

    print("\n--- Per-bucket recall (attack rows only, label==1) ---")
    print(f"  {'attack_bucket':<25}{'detected':>10}{'total':>10}{'recall':>10}")
    for bucket, (detected, total) in sorted(buckets.items(), key=lambda kv: -kv[1][1]):
        recall = detected / total if total else 0.0
        print(f"  {bucket:<25}{detected:>10}{total:>10}{recall:>10.4f}")


if __name__ == "__main__":
    print("Loading datasets...")
    slabs_records = load_slabs("test")
    neuralchemy_records = load_neuralchemy("core")
    dolly_records = load_dolly_benign(2000)
    all_records = slabs_records + neuralchemy_records + dolly_records
    print(
        f"Loaded: s-labs={len(slabs_records)}  neuralchemy={len(neuralchemy_records)}  "
        f"dolly={len(dolly_records)}  total={len(all_records)}"
    )

    print("\nRunning FULL SYSTEM (ablate=False) over all records...")
    full_results, full_skipped = evaluate_records(all_records, analyze_fn=analyze)
    print(f"Skipped rows (analyze() exceptions): {full_skipped}")

    print("\nRunning ABLATED (ablate=True, no multipliers/bonuses) over all records...")
    ablated_results, ablated_skipped = evaluate_records(all_records, analyze_fn=analyze_ablated)
    print(f"Skipped rows (analyze() exceptions): {ablated_skipped}")

    print("\n" + "=" * 60)
    print("OVERALL - FULL SYSTEM vs ABLATED")
    print("=" * 60)
    print_side_by_side(full_results, ablated_results)

    print("\n" + "=" * 60)
    print("PER-SOURCE (full system)")
    print("=" * 60)
    for source_name in ("s-labs", "neuralchemy"):
        source_results = [(r, p) for r, p in full_results if r["source"] == source_name]
        print_full_block(source_name, source_results)

    dolly_results = [(r, p) for r, p in full_results if r["source"] == "dolly"]
    print_dolly_block(dolly_results)

    print("\n" + "=" * 60)
    print("PER-BUCKET RECALL (full system)")
    print("=" * 60)
    print_bucket_recall(full_results)
