import re
import sys
import os
from collections import Counter
from datasets import load_dataset
from huggingface_hub import login

login(os.getenv("hf_token"))

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "analysis_output.txt")

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "to", "of", "in", "for", "on",
    "with", "at", "by", "from", "as", "it", "its", "this", "that",
    "these", "those", "i", "you", "we", "they", "he", "she", "me",
    "my", "your", "our",
}

KEYWORDS = [
    "ignore", "disregard", "forget", "override", "bypass",
    "pretend", "act as", "you are now", "jailbreak", "DAN",
    "system prompt", "instructions", "restrictions", "developer mode",
    "repeat", "print", "output", "reveal", "base64",
]


class TeeWriter:
    """Write to both stdout and a file simultaneously."""
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.file = open(filepath, "w", encoding="utf-8")

    def write(self, msg):
        self.terminal.write(msg)
        self.file.write(msg)

    def flush(self):
        self.terminal.flush()
        self.file.flush()

    def close(self):
        self.file.close()


# ---------------------------------------------------------------------------
# Step 1 — Load datasets and extract prompt text
# ---------------------------------------------------------------------------
def load_all_prompts():
    print("=" * 60)
    print("STEP 1 — Loading datasets")
    print("=" * 60)

    ds1 = load_dataset("hackaprompt/Pliny_HackAPrompt_Dataset", split="train")
    print(f"\n[Pliny_HackAPrompt_Dataset] columns: {ds1.column_names}")

    ds2 = load_dataset("hackaprompt/hackaprompt-dataset", split="train")
    print(f"[hackaprompt-dataset]        columns: {ds2.column_names}")

    prompt_col_1 = _find_prompt_column(ds1, "Pliny_HackAPrompt_Dataset")
    prompt_col_2 = _find_prompt_column(ds2, "hackaprompt-dataset")

    prompts_1 = [str(row[prompt_col_1]) for row in ds1 if row[prompt_col_1]]
    prompts_2 = [str(row[prompt_col_2]) for row in ds2 if row[prompt_col_2]]

    all_prompts = prompts_1 + prompts_2
    print(f"\nExtracted {len(prompts_1)} prompts from Pliny_HackAPrompt_Dataset (col: {prompt_col_1})")
    print(f"Extracted {len(prompts_2)} prompts from hackaprompt-dataset (col: {prompt_col_2})")
    print(f"Total combined prompts: {len(all_prompts)}\n")
    return all_prompts


def _find_prompt_column(dataset, name):
    candidates = ["prompt", "user_input", "text", "input", "question"]
    for col in candidates:
        if col in dataset.column_names:
            print(f"  -> Using column '{col}' for {name}")
            return col
    fallback = dataset.column_names[0]
    print(f"  -> No known prompt column found for {name}, falling back to '{fallback}'")
    return fallback


# ---------------------------------------------------------------------------
# Step 2 — Clean prompts
# ---------------------------------------------------------------------------
def clean_prompts(prompts):
    print("=" * 60)
    print("STEP 2 — Cleaning prompts")
    print("=" * 60)
    cleaned = []
    for p in prompts:
        p = p.lower()
        p = re.sub(r"\s+", " ", p).strip()
        cleaned.append(p)
    print(f"Cleaned {len(cleaned)} prompts (lowercased, whitespace-normalized, punctuation kept)\n")
    return cleaned


# ---------------------------------------------------------------------------
# Step 3 — N-gram extraction and counting
# ---------------------------------------------------------------------------
def tokenize(text):
    return re.findall(r"[a-z']+|[^\s\w]", text)


def extract_ngrams(tokens, n):
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def count_ngrams(prompts):
    print("=" * 60)
    print("STEP 3 — N-gram frequency analysis")
    print("=" * 60)

    word_counter = Counter()
    bigram_counter = Counter()
    trigram_counter = Counter()
    fourgram_counter = Counter()

    for p in prompts:
        tokens = tokenize(p)

        filtered = [t for t in tokens if t not in STOPWORDS]
        word_counter.update(filtered)

        bigram_counter.update(extract_ngrams(tokens, 2))
        trigram_counter.update(extract_ngrams(tokens, 3))
        fourgram_counter.update(extract_ngrams(tokens, 4))

    _print_top("TOP SINGLE WORDS", word_counter, fmt_func=lambda w: w[0])
    _print_top("TOP BIGRAMS", bigram_counter, fmt_func=lambda b: " ".join(b))
    _print_top("TOP TRIGRAMS", trigram_counter, fmt_func=lambda t: " ".join(t))
    _print_top("TOP 4-GRAMS", fourgram_counter, fmt_func=lambda f: " ".join(f))

    return word_counter, bigram_counter, trigram_counter, fourgram_counter


def _print_top(title, counter, n=40, fmt_func=str):
    print(f"\n=== {title} ===")
    for rank, (item, count) in enumerate(counter.most_common(n), 1):
        print(f"{rank:>3}. ({count:>5}) {fmt_func(item)}")
    print()


# ---------------------------------------------------------------------------
# Step 4 — Keyword group analysis
# ---------------------------------------------------------------------------
def keyword_analysis(prompts):
    print("=" * 60)
    print("STEP 4 — Keyword group analysis")
    print("=" * 60)

    for kw in KEYWORDS:
        kw_lower = kw.lower()
        examples = []
        for p in prompts:
            if kw_lower in p and len(examples) < 3:
                truncated = p[:200] + ("..." if len(p) > 200 else "")
                if truncated not in examples:
                    examples.append(truncated)
        print(f'\nKEYWORD: {kw}')
        if examples:
            print("EXAMPLES:")
            for i, ex in enumerate(examples, 1):
                print(f'  {i}. "{ex}"')
        else:
            print("  (no examples found)")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    tee = TeeWriter(OUTPUT_FILE)
    sys.stdout = tee

    try:
        all_prompts = load_all_prompts()
        cleaned = clean_prompts(all_prompts)
        count_ngrams(cleaned)
        keyword_analysis(cleaned)
        print(f"Full output saved to: {OUTPUT_FILE}")
    finally:
        sys.stdout = tee.terminal
        tee.close()


if __name__ == "__main__":
    main()
