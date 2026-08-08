import itertools
import math
import os
import platform
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataset_loader import load_slabs, load_neuralchemy, load_dolly_benign  # noqa: E402
from gateway import analyze  # noqa: E402

WARMUP_CALLS = 200
TARGET_CALLS = 10_000


def percentile(sorted_data, pct):
    """Linear-interpolation percentile over an already-sorted list."""
    if not sorted_data:
        return 0.0
    k = (len(sorted_data) - 1) * (pct / 100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    return sorted_data[f] * (c - k) + sorted_data[c] * (k - f)


if __name__ == "__main__":
    print("Loading datasets...")
    slabs_records = load_slabs("test")
    neuralchemy_records = load_neuralchemy("core")
    dolly_records = load_dolly_benign(2000)
    all_records = slabs_records + neuralchemy_records + dolly_records
    texts = [r["text"] for r in all_records]
    print(f"Loaded {len(texts)} texts (s-labs={len(slabs_records)}  neuralchemy={len(neuralchemy_records)}  dolly={len(dolly_records)})")

    print(f"\nWarming up ({WARMUP_CALLS} calls, timings discarded)...")
    warmup_cycle = itertools.cycle(texts)
    for _ in range(WARMUP_CALLS):
        analyze(next(warmup_cycle))

    print(f"Measuring {TARGET_CALLS} timed calls (looping dataset as needed)...")
    text_cycle = itertools.cycle(texts)
    latencies_ns = []
    for _ in range(TARGET_CALLS):
        text = next(text_cycle)
        t0 = time.perf_counter_ns()
        analyze(text)
        t1 = time.perf_counter_ns()
        latencies_ns.append(t1 - t0)

    latencies_ms = sorted(ns / 1_000_000 for ns in latencies_ns)
    total_timed_s = sum(latencies_ns) / 1_000_000_000

    n = len(latencies_ms)
    mean_ms = sum(latencies_ms) / n
    median_ms = percentile(latencies_ms, 50)
    p95_ms = percentile(latencies_ms, 95)
    p99_ms = percentile(latencies_ms, 99)
    p999_ms = percentile(latencies_ms, 99.9)
    min_ms = latencies_ms[0]
    max_ms = latencies_ms[-1]
    throughput = n / total_timed_s if total_timed_s else 0.0

    print("\n" + "=" * 50)
    print("LATENCY BENCHMARK RESULTS")
    print("=" * 50)
    print(f"  {'Metric':<20}{'Value':>15}")
    print(f"  {'-' * 35}")
    print(f"  {'Median':<20}{median_ms:>12.4f} ms")
    print(f"  {'Mean':<20}{mean_ms:>12.4f} ms")
    print(f"  {'p95':<20}{p95_ms:>12.4f} ms")
    print(f"  {'p99':<20}{p99_ms:>12.4f} ms")
    print(f"  {'p99.9':<20}{p999_ms:>12.4f} ms")
    print(f"  {'Min':<20}{min_ms:>12.4f} ms")
    print(f"  {'Max':<20}{max_ms:>12.4f} ms")
    print(f"  {'-' * 35}")
    print(f"  {'Throughput':<20}{throughput:>12.2f} calls/sec")
    print(f"  {'Total timed calls':<20}{n:>15}")

    print(f"\nNOTE: latency numbers are hardware/OS/load-dependent for this machine "
          f"({platform.system()} {platform.release()}, {platform.processor() or platform.machine()}, "
          f"Python {platform.python_version()}). Re-benchmark on target deployment hardware "
          f"before using these numbers for capacity planning.")
