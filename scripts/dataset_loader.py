import os
from collections import Counter
from datasets import load_dataset
from huggingface_hub import login

login(os.getenv("hf_token"))

CATEGORY_TO_FAMILY = {
    # role_hijack
    "persona_replacement": "role_hijack",
    "system_manipulation": "role_hijack",
    # instruction_override
    "instruction_override": "instruction_override",
    "direct_injection": "instruction_override",
    "context_confusion": "instruction_override",
    # privilege_escalation
    "jailbreak": "privilege_escalation",
    # payload_exfiltration
    "training_extraction": "payload_exfiltration",
    "prompt_extraction": "payload_exfiltration",
    "system_extraction": "payload_exfiltration",
    "prompt_leak": "payload_exfiltration",
    "model_fingerprinting": "payload_exfiltration",
    # context_poisoning
    "rag_poisoning": "context_poisoning",
    "output_manipulation": "context_poisoning",
    "response_manipulation": "context_poisoning",
    # encoding_obfuscation
    "encoding": "encoding_obfuscation",
    "encoding_obfuscation": "encoding_obfuscation",
    "token_smuggling": "encoding_obfuscation",
    "token_injection": "encoding_obfuscation",
    # indirect_injection
    "indirect_injection": "indirect_injection",
    "payload_injection": "indirect_injection",
    "agent_manipulation": "indirect_injection",
}


def load_slabs(split="test"):
    """S-Labs/prompt-injection-dataset -> {text, label} (0=benign, 1=injection)."""
    ds = load_dataset("S-Labs/prompt-injection-dataset", split=split)

    records = []
    for row in ds:
        text = str(row["text"]).strip() if row["text"] is not None else ""
        if not text:
            continue
        label = int(row["label"])
        records.append({
            "text": text,
            "label": label,
            "attack_type": "unknown",
            "attack_bucket": "benign" if label == 0 else "unknown",
            "source": "s-labs",
        })
    return records


def load_neuralchemy(config="core"):
    """neuralchemy/Prompt-injection-dataset -> {text, label, category}."""
    ds = load_dataset("neuralchemy/Prompt-injection-dataset", config, split="train")

    print(f"\n[neuralchemy] sample rows (config={config}):")
    for row in ds.select(range(min(3, len(ds)))):
        print(f"  {row}")

    records = []
    for row in ds:
        text = str(row["text"]).strip() if row["text"] is not None else ""
        if not text:
            continue
        label = int(row["label"])
        category = str(row["category"]).lower()
        if label == 0:
            attack_bucket = "benign"
        else:
            attack_bucket = CATEGORY_TO_FAMILY.get(category, "other")
        records.append({
            "text": text,
            "label": label,
            "attack_type": category,
            "attack_bucket": attack_bucket,
            "source": "neuralchemy",
        })
    return records


def load_dolly_benign(n=2000):
    """databricks/databricks-dolly-15k -> instruction field, all benign."""
    ds = load_dataset("databricks/databricks-dolly-15k", split="train")

    records = []
    for row in ds:
        if len(records) >= n:
            break
        text = str(row["instruction"]).strip() if row["instruction"] is not None else ""
        if not text:
            continue
        records.append({
            "text": text,
            "label": 0,
            "attack_type": "benign",
            "attack_bucket": "benign",
            "source": "dolly",
        })
    return records


def _report(name, records):
    print(f"\n=== {name} ===")
    print(f"Total: {len(records)}")

    label_counts = Counter(r["label"] for r in records)
    print(f"Label distribution: 0={label_counts.get(0, 0)}, 1={label_counts.get(1, 0)}")

    print("Examples:")
    for r in records[:3]:
        preview = r["text"][:120] + ("..." if len(r["text"]) > 120 else "")
        print(f"  text={preview!r} label={r['label']} attack_type={r['attack_type']} source={r['source']}")


if __name__ == "__main__":
    slabs_records = load_slabs()
    neuralchemy_records = load_neuralchemy()
    dolly_records = load_dolly_benign()

    attack_type_counts = Counter(r["attack_type"] for r in neuralchemy_records)
    print(f"\n[neuralchemy] unique attack_type values ({len(attack_type_counts)}):")
    for attack_type, count in attack_type_counts.most_common():
        print(f"  {attack_type}: {count}")

    attack_bucket_counts = Counter(r["attack_bucket"] for r in neuralchemy_records)
    print(f"\n[neuralchemy] attack_bucket counts ({len(attack_bucket_counts)}):")
    for attack_bucket, count in attack_bucket_counts.most_common():
        print(f"  {attack_bucket}: {count}")

    unmapped_attacks = sum(
        1 for r in neuralchemy_records
        if r["label"] == 1 and r["attack_bucket"] == "benign"
    )
    print(f"\n[neuralchemy] label==1 rows with attack_bucket=='benign': {unmapped_attacks}")

    _report("s-labs", slabs_records)
    _report("neuralchemy", neuralchemy_records)
    _report("dolly", dolly_records)

    total = len(slabs_records) + len(neuralchemy_records) + len(dolly_records)
    print(f"\nCombined total: {total}")
