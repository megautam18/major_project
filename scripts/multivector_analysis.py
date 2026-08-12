import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataset_loader import load_slabs, load_neuralchemy  # noqa: E402
from gateway import analyze  # noqa: E402

RULE_COUNT_BUCKETS = ["0", "1", "2", "3", "4+"]
FAMILY_COUNT_BUCKETS = ["0", "1", "2", "3+"]


def bucket_rule_count(n):
    return str(n) if n < 4 else "4+"


def bucket_family_count(n):
    return str(n) if n < 3 else "3+"


def analyze_attacks(records):
    """Return list of (rule_count, family_count) for each attack record."""
    stats = []
    for r in records:
        rules_fired = analyze(r["text"])["rules_fired"]
        rule_count = len(rules_fired)
        family_count = len({rule["family"] for rule in rules_fired})
        stats.append((rule_count, family_count))
    return stats


def print_distribution(title, buckets, counts, total):
    print(f"\n  {title}")
    print(f"    {'bucket':<10}{'count':>10}{'pct':>10}")
    for b in buckets:
        c = counts.get(b, 0)
        pct = (c / total * 100) if total else 0.0
        print(f"    {b:<10}{c:>10}{pct:>9.2f}%")


def report(name, stats):
    total = len(stats)
    print("\n" + "=" * 60)
    print(f"{name}  (n={total})")
    print("=" * 60)

    if total == 0:
        print("  (no records)")
        return

    rule_counts = Counter(bucket_rule_count(rc) for rc, fc in stats)
    family_counts = Counter(bucket_family_count(fc) for rc, fc in stats)

    print_distribution("Rule-count distribution", RULE_COUNT_BUCKETS, rule_counts, total)
    print_distribution("Distinct-family-count distribution", FAMILY_COUNT_BUCKETS, family_counts, total)

    n_ge2_rules = sum(1 for rc, fc in stats if rc >= 2)
    n_ge2_families = sum(1 for rc, fc in stats if fc >= 2)
    pct_ge2_rules = n_ge2_rules / total * 100
    pct_ge2_families = n_ge2_families / total * 100

    print(f"\n  HEADLINE: {n_ge2_rules}/{total} ({pct_ge2_rules:.2f}%) fired >=2 rules")
    print(f"  HEADLINE: {n_ge2_families}/{total} ({pct_ge2_families:.2f}%) fired >=2 distinct families")

    detected = [(rc, fc) for rc, fc in stats if rc >= 1]
    n_detected = len(detected)
    n_detected_ge2_families = sum(1 for rc, fc in detected if fc >= 2)
    pct_detected_ge2_families = (n_detected_ge2_families / n_detected * 100) if n_detected else 0.0

    print(f"\n  Among attacks with >=1 rule fired (n={n_detected}):")
    print(f"    {n_detected_ge2_families}/{n_detected} ({pct_detected_ge2_families:.2f}%) fired >=2 distinct families")


if __name__ == "__main__":
    print("Loading datasets...")
    slabs_records = load_slabs("test")
    neuralchemy_records = load_neuralchemy("core")

    slabs_attacks = [r for r in slabs_records if r["label"] == 1]
    neuralchemy_attacks = [r for r in neuralchemy_records if r["label"] == 1]
    print(f"s-labs attack rows: {len(slabs_attacks)}")
    print(f"neuralchemy attack rows: {len(neuralchemy_attacks)}")

    print("\nRunning analyze() over all attack rows...")
    slabs_stats = analyze_attacks(slabs_attacks)
    neuralchemy_stats = analyze_attacks(neuralchemy_attacks)
    combined_stats = slabs_stats + neuralchemy_stats

    report("s-labs", slabs_stats)
    report("neuralchemy", neuralchemy_stats)
    report("COMBINED", combined_stats)
