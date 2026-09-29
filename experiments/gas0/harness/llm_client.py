"""OpenAI-compatible llama.cpp client with exact server-side token accounting."""
from __future__ import annotations

import json
import time
from urllib.request import Request, urlopen


class LlamaClient:
    def __init__(self, base_url: str, model: str, timeout=300):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def _post(self, path, body):
        req = Request(self.base_url + path, data=json.dumps(body).encode(),
                      headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=self.timeout) as response:
            return json.load(response)

    def count_tokens(self, value, tools=None):
        if isinstance(value, str):
            text = value
        else:
            text = json.dumps({"messages": value, "tools": tools or []}, ensure_ascii=False)
        return len(self._post("/tokenize", {"content": text})["tokens"])

    def chat(self, messages, tools, seed, max_tokens=1024):
        start = time.monotonic()
        body = {"model": self.model, "messages": messages, "tools": tools,
                "tool_choice": "auto", "temperature": 0.2, "top_p": 0.95,
                "seed": seed, "max_tokens": max_tokens, "stream": False}
        answer = self._post("/v1/chat/completions", body)
        usage = answer.get("usage", {})
        return answer["choices"][0]["message"], {
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "peak_context_tokens": (usage.get("prompt_tokens") or 0) +
                                   (usage.get("completion_tokens") or 0),
            "wall_seconds": time.monotonic() - start,
        }
