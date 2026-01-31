from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from datasets import DatasetDict, load_from_disk


@dataclass
class GSM8KExample:
    question: str
    answer: str
    final_answer: str


@dataclass
class ARCExample:
    question: str
    choices: Dict[str, List[str]]
    answer_key: str


def load_gsm8k(path: str) -> DatasetDict:
    return load_from_disk(path)


def load_arc(path: str) -> DatasetDict:
    return load_from_disk(path)


def parse_gsm8k_answer(answer: str) -> str:
    # GSM8K final answer appears after '####'
    if "####" in answer:
        return answer.split("####")[-1].strip()
    # Fallback: last line
    return answer.strip().split("\n")[-1].strip()


def to_gsm8k_examples(dataset_split) -> List[GSM8KExample]:
    examples = []
    for row in dataset_split:
        final = parse_gsm8k_answer(row["answer"])
        examples.append(GSM8KExample(question=row["question"], answer=row["answer"], final_answer=final))
    return examples


def to_arc_examples(dataset_split) -> List[ARCExample]:
    examples = []
    for row in dataset_split:
        examples.append(ARCExample(question=row["question"], choices=row["choices"], answer_key=row["answerKey"]))
    return examples
