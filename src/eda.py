from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from datasets import load_from_disk


def main():
    gsm = load_from_disk("datasets/gsm8k")
    arc = load_from_disk("datasets/ai2_arc")

    summary = {}
    for name, ds in [("gsm8k", gsm), ("arc", arc)]:
        split = ds["test"]
        df = split.to_pandas()
        summary[name] = {
            "rows": len(df),
            "columns": list(df.columns),
            "missing_values": df.isna().sum().to_dict(),
        }
        # Save a few samples
        samples_path = Path("results") / f"{name}_samples.json"
        samples_path.write_text(df.head(3).to_json(orient="records", force_ascii=True, indent=2), encoding="utf-8")

    Path("results").mkdir(parents=True, exist_ok=True)
    (Path("results") / "data_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Plot question length distributions
    gsm_q = [len(x.split()) for x in gsm["test"]["question"]]
    arc_q = [len(x.split()) for x in arc["test"]["question"]]

    plt.figure(figsize=(8, 4))
    plt.hist(gsm_q, bins=30, alpha=0.6, label="GSM8K")
    plt.hist(arc_q, bins=30, alpha=0.6, label="ARC")
    plt.xlabel("Question length (words)")
    plt.ylabel("Count")
    plt.title("Question Length Distributions")
    plt.legend()
    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig("figures/question_length_hist.png", dpi=150)


if __name__ == "__main__":
    main()
