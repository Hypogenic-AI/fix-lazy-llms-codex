from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class PromptSpec:
    name: str
    system: str
    user: str


def system_tone(tone: str) -> str:
    if tone == "rude":
        return "You are terse and impatient. Answer with no unnecessary niceties."
    if tone == "polite":
        return "You are courteous and helpful. Be respectful and professional."
    return "You are a helpful assistant."


def gsm8k_direct(question: str) -> str:
    return (
        "Solve the problem and give only the final numeric answer. "
        "Format: Final: <number>\n\n"
        f"Problem: {question}"
    )


def gsm8k_cot(question: str) -> str:
    return (
        "Solve the problem step by step. End with 'Final: <number>'.\n\n"
        f"Problem: {question}"
    )


def gsm8k_decompose(question: str) -> str:
    return (
        "Break the problem into 2-4 sub-questions that would help solve it. "
        "List them as Q1:, Q2:, etc.\n\n"
        f"Problem: {question}"
    )


def gsm8k_solve_from_subqs(question: str, subqs: str) -> str:
    return (
        "Use the sub-questions to solve the original problem step by step. "
        "End with 'Final: <number>'.\n\n"
        f"Problem: {question}\n\n"
        f"Sub-questions:\n{subqs}"
    )


def arc_direct(question: str, choices: Dict[str, list]) -> str:
    choice_lines = "\n".join([f"{label}. {text}" for label, text in zip(choices["label"], choices["text"])])
    return (
        "Choose the correct option. Provide only the letter. Format: Final: <letter>\n\n"
        f"Question: {question}\nChoices:\n{choice_lines}"
    )


def arc_cot(question: str, choices: Dict[str, list]) -> str:
    choice_lines = "\n".join([f"{label}. {text}" for label, text in zip(choices["label"], choices["text"])])
    return (
        "Reason step by step, then give the final answer letter. End with 'Final: <letter>'.\n\n"
        f"Question: {question}\nChoices:\n{choice_lines}"
    )


def arc_decompose(question: str, choices: Dict[str, list]) -> str:
    choice_lines = "\n".join([f"{label}. {text}" for label, text in zip(choices["label"], choices["text"])])
    return (
        "Break the question into 2-4 sub-questions that would help decide the correct option. "
        "List them as Q1:, Q2:, etc.\n\n"
        f"Question: {question}\nChoices:\n{choice_lines}"
    )


def arc_solve_from_subqs(question: str, choices: Dict[str, list], subqs: str) -> str:
    choice_lines = "\n".join([f"{label}. {text}" for label, text in zip(choices["label"], choices["text"])])
    return (
        "Use the sub-questions to solve the original question step by step. "
        "End with 'Final: <letter>'.\n\n"
        f"Question: {question}\nChoices:\n{choice_lines}\n\n"
        f"Sub-questions:\n{subqs}"
    )


def critic_prompt(answer: str, severity: str) -> str:
    if severity == "harsh":
        tone = "Be extremely critical and point out every flaw or missing step."
    else:
        tone = "Be constructive and point out issues or gaps." 
    return (
        f"Critique the answer below. {tone} Provide a short list of issues.\n\n"
        f"Answer:\n{answer}"
    )


def revise_prompt(question: str, critique: str, dataset: str) -> str:
    if dataset == "gsm8k":
        instruction = "Revise the solution using the critique and provide the final numeric answer. End with 'Final: <number>'."
    else:
        instruction = "Revise the answer using the critique and provide the final letter. End with 'Final: <letter>'."
    return (
        f"{instruction}\n\nQuestion:\n{question}\n\nCritique:\n{critique}"
    )
