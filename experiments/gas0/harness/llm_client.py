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
        self._renders_tools: dict[str, bool] = {}

    def _get(self, path):
        with urlopen(Request(self.base_url + path), timeout=self.timeout) as response:
            return json.load(response)

    def check_context(self, minimum=16384):
        """Fail fast unless every server slot holds a full `minimum`-token sequence. llama.cpp
        splits --ctx-size across --parallel slots, so 4 slots of 16,384 need --ctx-size 65536."""
        props = self._get("/props")
        n_ctx = (props.get("default_generation_settings") or {}).get("n_ctx") or props.get("n_ctx")
        if not n_ctx or int(n_ctx) < minimum:
            raise RuntimeError(f"server slot context {n_ctx} < required {minimum}")
        return int(n_ctx)

    def _template_renders_tools(self, tools):
        key = json.dumps(tools, sort_keys=True)
        if key not in self._renders_tools:
            probe = [{"role": "user", "content": "x"}]
            with_tools = self._post("/apply-template", {"messages": probe, "tools": tools})["prompt"]
            without = self._post("/apply-template", {"messages": probe, "tools": []})["prompt"]
            self._renders_tools[key] = with_tools != without
        return self._renders_tools[key]

    def _post(self, path, body):
        req = Request(self.base_url + path, data=json.dumps(body).encode(),
                      headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=self.timeout) as response:
            return json.load(response)

    def count_tokens(self, value, tools=None):
        if isinstance(value, str):
            return len(self._post("/tokenize", {"content": value})["tokens"])
        rendered = self._post("/apply-template", {"messages": value,
                                                   "tools": tools or []})["prompt"]
        # add_special matches how the server tokenizes a completion prompt (BOS if the model uses it)
        count = len(self._post("/tokenize", {"content": rendered, "add_special": True})["tokens"])
        # With --jinja, /apply-template renders tool schemas exactly as /v1/chat/completions does.
        # Only if this server's template demonstrably omits them here is their JSON added
        # (conservative fallback); otherwise adding it would double count, by more in the
        # cells with ledger tools.
        if tools and not self._template_renders_tools(tools):
            count += len(self._post("/tokenize", {
                "content": json.dumps(tools, ensure_ascii=False)})["tokens"])
        return count

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
