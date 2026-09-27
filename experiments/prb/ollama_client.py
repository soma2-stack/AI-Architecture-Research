"""Minimal client for the EXISTING local Ollama server (no installs, no downloads). Model: qwen3.5:4b."""
import json, time, requests

URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen3.5:4b"


def chat(prompt, think=True, num_gpu=0, num_predict=4096, num_ctx=8192, temperature=0.0, seed=0, timeout=3600, top_p=None, top_k=None):
    body = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "stream": False, "think": think,
            "options": {"num_gpu": num_gpu, "num_predict": num_predict, "num_ctx": num_ctx,
                        "temperature": temperature, "seed": seed}}
    if top_p is not None: body["options"]["top_p"] = top_p
    if top_k is not None: body["options"]["top_k"] = top_k
    t0 = time.time()
    r = requests.post(URL, json=body, timeout=timeout)
    r.raise_for_status()
    j = r.json()
    msg = j.get("message", {})
    return dict(content=msg.get("content", ""), thinking=msg.get("thinking", ""), secs=round(time.time() - t0, 1),
                eval_count=j.get("eval_count"), prompt_eval_count=j.get("prompt_eval_count"),
                eval_duration=j.get("eval_duration"), prompt_eval_duration=j.get("prompt_eval_duration"),
                done_reason=j.get("done_reason"))


if __name__ == "__main__":
    r = chat("What is (5 + 4) mod 7? Answer with just the number.", think=False, num_predict=20)
    print(r)
    tps = r["eval_count"] / (r["eval_duration"] / 1e9) if r.get("eval_duration") else None
    print("gen tok/s", tps, "prompt tok/s", r["prompt_eval_count"] / (r["prompt_eval_duration"] / 1e9) if r.get("prompt_eval_duration") else None)
