from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

from datasets import Dataset

from data import load_arc, load_gsm8k, to_arc_examples, to_gsm8k_examples
from evaluate import (
    compute_accuracy,
    extract_arc_final,
    extract_gsm8k_final,
    is_correct_arc,
    is_correct_gsm8k,
)
from llm import LLMClient
from prompts import (
    arc_cot,
    arc_decompose,
    arc_direct,
    arc_solve_from_subqs,
    critic_prompt,
    gsm8k_cot,
    gsm8k_decompose,
    gsm8k_direct,
    gsm8k_solve_from_subqs,
    revise_prompt,
    system_tone,
)
from utils import append_jsonl, ensure_dir, now_iso, set_seed


def sample_dataset(split: Dataset, n: int, seed: int) -> Dataset:
    if n >= len(split):
        return split
    return split.shuffle(seed=seed).select(range(n))


def majority_vote(answers: List[str]) -> str:
    if not answers:
        return ""
    counts = Counter([a for a in answers if a])
    return counts.most_common(1)[0][0] if counts else ""


def run_direct(client: LLMClient, model: str, tone: str, question: str, dataset: str, max_tokens: int, temperature: float):
    system = system_tone(tone)
    if dataset == "gsm8k":
        user = gsm8k_direct(question)
    else:
        user = question
    return client.generate(model=model, system=system, user=user, temperature=temperature, max_output_tokens=max_tokens)


def run_cot(client: LLMClient, model: str, tone: str, question: str, dataset: str, max_tokens: int, temperature: float):
    system = system_tone(tone)
    if dataset == "gsm8k":
        user = gsm8k_cot(question)
    else:
        user = question
    return client.generate(model=model, system=system, user=user, temperature=temperature, max_output_tokens=max_tokens)


def run_least_to_most(client: LLMClient, model: str, tone: str, question: str, dataset: str, max_tokens: int):
    system = system_tone(tone)
    if dataset == "gsm8k":
        subq_prompt = gsm8k_decompose(question)
        subq_resp = client.generate(model=model, system=system, user=subq_prompt, temperature=0.0, max_output_tokens=max_tokens)
        solve_prompt = gsm8k_solve_from_subqs(question, subq_resp.response_text)
    else:
        subq_prompt = arc_decompose(question, choices=None)
        subq_resp = client.generate(model=model, system=system, user=subq_prompt, temperature=0.0, max_output_tokens=max_tokens)
        solve_prompt = arc_solve_from_subqs(question, choices=None, subqs=subq_resp.response_text)
    final_resp = client.generate(model=model, system=system, user=solve_prompt, temperature=0.0, max_output_tokens=max_tokens)
    return final_resp, subq_resp


def run_critic_refine(client: LLMClient, model: str, tone: str, question: str, dataset: str, severity: str, max_tokens: int, rounds: int = 1):
    system = system_tone(tone)
    if dataset == "gsm8k":
        user = gsm8k_cot(question)
    else:
        user = question

    answer_resp = client.generate(model=model, system=system, user=user, temperature=0.0, max_output_tokens=max_tokens)
    critique_resp = None
    current_answer = answer_resp.response_text
    for _ in range(rounds):
        critique_prompt = critic_prompt(current_answer, severity)
        critique_resp = client.generate(model=model, system=system, user=critique_prompt, temperature=0.0, max_output_tokens=max_tokens)
        rev_prompt = revise_prompt(question, critique_resp.response_text, dataset=dataset)
        answer_resp = client.generate(model=model, system=system, user=rev_prompt, temperature=0.0, max_output_tokens=max_tokens)
        current_answer = answer_resp.response_text
    return answer_resp, critique_resp


def run_self_consistency(client: LLMClient, model: str, tone: str, question: str, dataset: str, max_tokens: int, k: int = 3):
    system = system_tone(tone)
    responses = []
    for _ in range(k):
        if dataset == "gsm8k":
            user = gsm8k_cot(question)
        else:
            user = question
        resp = client.generate(model=model, system=system, user=user, temperature=0.7, max_output_tokens=max_tokens)
        responses.append(resp)
    return responses


def build_arc_prompt_direct(example) -> str:
    return arc_direct(example.question, example.choices)


def build_arc_prompt_cot(example) -> str:
    return arc_cot(example.question, example.choices)


def build_arc_prompt_decompose(example) -> str:
    return arc_decompose(example.question, example.choices)


def build_arc_prompt_solve(example, subqs: str) -> str:
    return arc_solve_from_subqs(example.question, example.choices, subqs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gsm8k-path", default="datasets/gsm8k")
    parser.add_argument("--arc-path", default="datasets/ai2_arc")
    parser.add_argument("--gsm8k-n", type=int, default=100)
    parser.add_argument("--arc-n", type=int, default=100)
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4.1"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-tokens", type=int, default=256)
    args = parser.parse_args()

    set_seed(args.seed)

    results_dir = Path("results/model_outputs")
    ensure_dir(results_dir)
    cache_path = results_dir / "cache.jsonl"
    client = LLMClient(cache_path)

    gsm = load_gsm8k(args.gsm8k_path)
    arc = load_arc(args.arc_path)

    gsm_split = sample_dataset(gsm["test"], args.gsm8k_n, args.seed)
    arc_split = sample_dataset(arc["test"], args.arc_n, args.seed)

    gsm_examples = to_gsm8k_examples(gsm_split)
    arc_examples = to_arc_examples(arc_split)

    metadata = {
        "timestamp": now_iso(),
        "model": args.model,
        "seed": args.seed,
        "gsm8k_n": len(gsm_examples),
        "arc_n": len(arc_examples),
        "max_tokens": args.max_tokens,
    }
    (Path("results") / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    records: List[Dict[str, Any]] = []

    # Conditions to run
    conditions = [
        ("direct-neutral", {"tone": "neutral", "method": "direct"}),
        ("cot-neutral", {"tone": "neutral", "method": "cot"}),
        ("critic-harsh", {"tone": "neutral", "method": "critic", "severity": "harsh", "rounds": 1}),
        ("critic-harsh-lowbudget", {"tone": "neutral", "method": "critic", "severity": "harsh", "rounds": 1, "max_tokens": 128}),
        ("rude-direct", {"tone": "rude", "method": "direct"}),
        ("polite-direct", {"tone": "polite", "method": "direct"}),
    ]

    # GSM8K runs
    for condition_name, cfg in conditions:
        for idx, ex in enumerate(gsm_examples):
            max_tokens = cfg.get("max_tokens", args.max_tokens)
            if cfg["method"] == "direct":
                resp = client.generate(
                    model=args.model,
                    system=system_tone(cfg["tone"]),
                    user=gsm8k_direct(ex.question),
                    temperature=0.0,
                    max_output_tokens=max_tokens,
                )
                pred = extract_gsm8k_final(resp.response_text)
                correct = is_correct_gsm8k(pred, ex.final_answer)
                records.append({
                    "dataset": "gsm8k",
                    "condition": condition_name,
                    "index": idx,
                    "question": ex.question,
                    "gold": ex.final_answer,
                    "response": resp.response_text,
                    "prediction": pred,
                    "correct": correct,
                    "usage": resp.usage,
                    "cached": resp.cached,
                })
            elif cfg["method"] == "cot":
                resp = client.generate(
                    model=args.model,
                    system=system_tone(cfg["tone"]),
                    user=gsm8k_cot(ex.question),
                    temperature=0.0,
                    max_output_tokens=max_tokens,
                )
                pred = extract_gsm8k_final(resp.response_text)
                correct = is_correct_gsm8k(pred, ex.final_answer)
                records.append({
                    "dataset": "gsm8k",
                    "condition": condition_name,
                    "index": idx,
                    "question": ex.question,
                    "gold": ex.final_answer,
                    "response": resp.response_text,
                    "prediction": pred,
                    "correct": correct,
                    "usage": resp.usage,
                    "cached": resp.cached,
                })
            elif cfg["method"] == "least_to_most":
                subq_prompt = gsm8k_decompose(ex.question)
                subq_resp = client.generate(
                    model=args.model,
                    system=system_tone(cfg["tone"]),
                    user=subq_prompt,
                    temperature=0.0,
                    max_output_tokens=max_tokens,
                )
                solve_prompt = gsm8k_solve_from_subqs(ex.question, subq_resp.response_text)
                final_resp = client.generate(
                    model=args.model,
                    system=system_tone(cfg["tone"]),
                    user=solve_prompt,
                    temperature=0.0,
                    max_output_tokens=max_tokens,
                )
                pred = extract_gsm8k_final(final_resp.response_text)
                correct = is_correct_gsm8k(pred, ex.final_answer)
                records.append({
                    "dataset": "gsm8k",
                    "condition": condition_name,
                    "index": idx,
                    "question": ex.question,
                    "gold": ex.final_answer,
                    "subquestions": subq_resp.response_text,
                    "response": final_resp.response_text,
                    "prediction": pred,
                    "correct": correct,
                    "usage": {
                        "subq": subq_resp.usage,
                        "final": final_resp.usage,
                    },
                    "cached": subq_resp.cached and final_resp.cached,
                })
            elif cfg["method"] == "critic":
                resp, critique = run_critic_refine(
                    client,
                    args.model,
                    cfg["tone"],
                    ex.question,
                    "gsm8k",
                    cfg["severity"],
                    max_tokens=max_tokens,
                    rounds=cfg["rounds"],
                )
                pred = extract_gsm8k_final(resp.response_text)
                correct = is_correct_gsm8k(pred, ex.final_answer)
                records.append({
                    "dataset": "gsm8k",
                    "condition": condition_name,
                    "index": idx,
                    "question": ex.question,
                    "gold": ex.final_answer,
                    "response": resp.response_text,
                    "critique": critique.response_text if critique else "",
                    "prediction": pred,
                    "correct": correct,
                    "usage": {
                        "answer": resp.usage,
                        "critique": critique.usage if critique else {},
                    },
                    "cached": resp.cached,
                })

    # ARC runs
    for condition_name, cfg in conditions:
        for idx, ex in enumerate(arc_examples):
            max_tokens = cfg.get("max_tokens", args.max_tokens)
            if cfg["method"] == "direct":
                resp = client.generate(
                    model=args.model,
                    system=system_tone(cfg["tone"]),
                    user=arc_direct(ex.question, ex.choices),
                    temperature=0.0,
                    max_output_tokens=max_tokens,
                )
                pred = extract_arc_final(resp.response_text)
                correct = is_correct_arc(pred, ex.answer_key)
                records.append({
                    "dataset": "arc",
                    "condition": condition_name,
                    "index": idx,
                    "question": ex.question,
                    "choices": ex.choices,
                    "gold": ex.answer_key,
                    "response": resp.response_text,
                    "prediction": pred,
                    "correct": correct,
                    "usage": resp.usage,
                    "cached": resp.cached,
                })
            elif cfg["method"] == "cot":
                resp = client.generate(
                    model=args.model,
                    system=system_tone(cfg["tone"]),
                    user=arc_cot(ex.question, ex.choices),
                    temperature=0.0,
                    max_output_tokens=max_tokens,
                )
                pred = extract_arc_final(resp.response_text)
                correct = is_correct_arc(pred, ex.answer_key)
                records.append({
                    "dataset": "arc",
                    "condition": condition_name,
                    "index": idx,
                    "question": ex.question,
                    "choices": ex.choices,
                    "gold": ex.answer_key,
                    "response": resp.response_text,
                    "prediction": pred,
                    "correct": correct,
                    "usage": resp.usage,
                    "cached": resp.cached,
                })
            elif cfg["method"] == "least_to_most":
                subq_prompt = arc_decompose(ex.question, ex.choices)
                subq_resp = client.generate(
                    model=args.model,
                    system=system_tone(cfg["tone"]),
                    user=subq_prompt,
                    temperature=0.0,
                    max_output_tokens=max_tokens,
                )
                solve_prompt = arc_solve_from_subqs(ex.question, ex.choices, subq_resp.response_text)
                final_resp = client.generate(
                    model=args.model,
                    system=system_tone(cfg["tone"]),
                    user=solve_prompt,
                    temperature=0.0,
                    max_output_tokens=max_tokens,
                )
                pred = extract_arc_final(final_resp.response_text)
                correct = is_correct_arc(pred, ex.answer_key)
                records.append({
                    "dataset": "arc",
                    "condition": condition_name,
                    "index": idx,
                    "question": ex.question,
                    "choices": ex.choices,
                    "gold": ex.answer_key,
                    "subquestions": subq_resp.response_text,
                    "response": final_resp.response_text,
                    "prediction": pred,
                    "correct": correct,
                    "usage": {
                        "subq": subq_resp.usage,
                        "final": final_resp.usage,
                    },
                    "cached": subq_resp.cached and final_resp.cached,
                })
            elif cfg["method"] == "critic":
                resp, critique = run_critic_refine(
                    client,
                    args.model,
                    cfg["tone"],
                    arc_cot(ex.question, ex.choices),
                    "arc",
                    cfg["severity"],
                    max_tokens=max_tokens,
                    rounds=cfg["rounds"],
                )
                pred = extract_arc_final(resp.response_text)
                correct = is_correct_arc(pred, ex.answer_key)
                records.append({
                    "dataset": "arc",
                    "condition": condition_name,
                    "index": idx,
                    "question": ex.question,
                    "choices": ex.choices,
                    "gold": ex.answer_key,
                    "response": resp.response_text,
                    "critique": critique.response_text if critique else "",
                    "prediction": pred,
                    "correct": correct,
                    "usage": {
                        "answer": resp.usage,
                        "critique": critique.usage if critique else {},
                    },
                    "cached": resp.cached,
                })

    output_path = results_dir / "raw_outputs.jsonl"
    append_jsonl(output_path, records)

    summary = {}
    for dataset in ["gsm8k", "arc"]:
        for condition_name, _ in conditions:
            subset = [r for r in records if r["dataset"] == dataset and r["condition"] == condition_name]
            if not subset:
                continue
            acc = compute_accuracy([r["correct"] for r in subset])
            summary[f"{dataset}:{condition_name}"] = {
                "n": len(subset),
                "accuracy": acc,
            }
    (Path("results") / "evaluations" / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
