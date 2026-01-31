from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_records(path: Path) -> List[dict]:
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def bootstrap_ci(diff_samples: np.ndarray, alpha: float = 0.05) -> Tuple[float, float]:
    lower = np.percentile(diff_samples, 100 * (alpha / 2))
    upper = np.percentile(diff_samples, 100 * (1 - alpha / 2))
    return float(lower), float(upper)


def paired_bootstrap_diff(base: np.ndarray, other: np.ndarray, n_boot: int = 2000, seed: int = 42) -> Tuple[float, float]:
    rng = np.random.default_rng(seed)
    n = len(base)
    diffs = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        diffs.append(other[idx].mean() - base[idx].mean())
    diffs = np.array(diffs)
    return bootstrap_ci(diffs)


def main():
    raw_path = Path("results/model_outputs/raw_outputs.jsonl")
    if not raw_path.exists():
        raise FileNotFoundError("Run experiments first: results/model_outputs/raw_outputs.jsonl not found")

    records = load_records(raw_path)
    df = pd.DataFrame(records)
    df["correct"] = df["correct"].astype(bool)

    summary_rows = []
    ci_rows = []

    for dataset in sorted(df["dataset"].unique()):
        base = df[(df["dataset"] == dataset) & (df["condition"] == "direct-neutral")]
        if base.empty:
            continue
        base_correct = base.sort_values("index")["correct"].to_numpy(dtype=float)

        for condition in sorted(df[df["dataset"] == dataset]["condition"].unique()):
            subset = df[(df["dataset"] == dataset) & (df["condition"] == condition)]
            acc = subset["correct"].mean()
            summary_rows.append({
                "dataset": dataset,
                "condition": condition,
                "n": len(subset),
                "accuracy": acc,
            })

            if condition == "direct-neutral":
                continue
            other = subset.sort_values("index")["correct"].to_numpy(dtype=float)
            n = min(len(base_correct), len(other))
            base_trim = base_correct[:n]
            other_trim = other[:n]
            ci_low, ci_high = paired_bootstrap_diff(base_trim, other_trim)
            ci_rows.append({
                "dataset": dataset,
                "condition": condition,
                "diff_vs_direct": float(other_trim.mean() - base_trim.mean()),
                "ci_low": ci_low,
                "ci_high": ci_high,
            })

    summary_df = pd.DataFrame(summary_rows)
    ci_df = pd.DataFrame(ci_rows)

    Path("results/evaluations").mkdir(parents=True, exist_ok=True)
    summary_df.to_csv("results/evaluations/accuracy_summary.csv", index=False)
    ci_df.to_csv("results/evaluations/diff_bootstrap_ci.csv", index=False)

    # Plot accuracies
    for dataset in summary_df["dataset"].unique():
        subset = summary_df[summary_df["dataset"] == dataset]
        plt.figure(figsize=(10, 4))
        plt.bar(subset["condition"], subset["accuracy"])
        plt.xticks(rotation=30, ha="right")
        plt.ylim(0, 1)
        plt.ylabel("Accuracy")
        plt.title(f"Accuracy by Condition ({dataset})")
        plt.tight_layout()
        Path("results/plots").mkdir(parents=True, exist_ok=True)
        plt.savefig(f"results/plots/{dataset}_accuracy.png", dpi=150)


if __name__ == "__main__":
    main()
