from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from utils import append_jsonl, now_iso, read_jsonl, sha256_dict


@dataclass
class LLMResult:
    request_id: str
    model: str
    prompt: Dict[str, Any]
    response_text: str
    usage: Dict[str, Any]
    cached: bool


def _response_text(response) -> str:
    # OpenAI Responses API returns output items with message content
    try:
        if hasattr(response, "output_text") and response.output_text:
            return response.output_text
    except Exception:
        pass
    texts: List[str] = []
    for item in getattr(response, "output", []) or []:
        if item.type == "message":
            for content in item.content:
                if content.type == "output_text":
                    texts.append(content.text)
    return "\n".join(texts).strip()


def _usage_dict(response) -> Dict[str, Any]:
    usage = getattr(response, "usage", None)
    if not usage:
        return {}
    return {
        "input_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
    }


class LLMClient:
    def __init__(self, cache_path: Path):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set in the environment.")
        self.cache_path = cache_path
        self.cache = {rec["request_id"]: rec for rec in read_jsonl(cache_path)}

    @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def _call_openai(self, payload: Dict[str, Any]):
        return self.client.responses.create(**payload)

    def generate(
        self,
        model: str,
        system: str,
        user: str,
        temperature: float,
        max_output_tokens: int,
    ) -> LLMResult:
        payload = {
            "model": model,
            "input": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
        }

        request_id = sha256_dict(payload)
        if request_id in self.cache:
            cached = self.cache[request_id]
            return LLMResult(
                request_id=request_id,
                model=cached["model"],
                prompt=cached["prompt"],
                response_text=cached["response_text"],
                usage=cached.get("usage", {}),
                cached=True,
            )

        response = self._call_openai(payload)
        text = _response_text(response)
        usage = _usage_dict(response)
        record = {
            "request_id": request_id,
            "timestamp": now_iso(),
            "model": model,
            "prompt": payload,
            "response_text": text,
            "usage": usage,
        }
        append_jsonl(self.cache_path, [record])
        self.cache[request_id] = record
        return LLMResult(
            request_id=request_id,
            model=model,
            prompt=payload,
            response_text=text,
            usage=usage,
            cached=False,
        )
