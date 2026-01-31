from __future__ import annotations

import re
from typing import Dict, Tuple


def extract_gsm8k_final(text: str) -> str:
    if not text:
        return ""
    # Prefer explicit Final: marker
    match = re.search(r"Final:\s*([-+]?\d+(?:\.\d+)?)", text, re.IGNORECASE)
    if match:
        return match.group(1)
    # Handle #### format
    if "####" in text:
        return text.split("####")[-1].strip().split()[0]
    # Fallback: last number in text
    numbers = re.findall(r"[-+]?\d+(?:\.\d+)?", text)
    return numbers[-1] if numbers else ""


def extract_arc_final(text: str) -> str:
    if not text:
        return ""
    match = re.search(r"Final:\s*([A-D])", text, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    # Fallback: first standalone letter option
    match = re.search(r"\b([A-D])\b", text)
    return match.group(1).upper() if match else ""


def is_correct_gsm8k(pred: str, gold: str) -> bool:
    try:
        return str(pred).strip() == str(gold).strip()
    except Exception:
        return False


def is_correct_arc(pred: str, gold: str) -> bool:
    return str(pred).strip().upper() == str(gold).strip().upper()


def compute_accuracy(correct_flags) -> float:
    if not correct_flags:
        return 0.0
    return sum(1 for c in correct_flags if c) / len(correct_flags)
