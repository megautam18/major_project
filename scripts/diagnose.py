import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataset_loader import load_slabs  # noqa: E402
from gateway import analyze  # noqa: E402

N = 25


if __name__ == "__main__":
    slabs_records = load_slabs("test")

    target_records = [r for r in slabs_records if r["label"] == 1][:N]

    print(f"\nLoaded {len(target_records)} records (label=1) from s-labs\n")

    for i, r in enumerate(target_records, 1):
        result = analyze(r["text"])

        print(f"[{i}] TEXT: {r['text']!r}")
        print(f"    VERDICT: {result['verdict']}")
        print(f"    NORMALIZED_SCORE: {result['normalized_score']}")
        rules_fired = result["rules_fired"]
        if rules_fired:
            print(f"    RULES FIRED ({len(rules_fired)}):")
            for rule in rules_fired:
                print(f"      - {rule['rule_id']}: matched_text={rule['matched_text']!r}")
        else:
            print("    RULES FIRED: none")
        print("---")
