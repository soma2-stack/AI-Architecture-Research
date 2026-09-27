"""
Z.3 — chain-of-thought / thinking condition with qwen3.5:4b (existing Ollama server).
Per episode (n, seed, m): fresh symbols (from the Qwen3-VL-verified pool; Ollama tokenisation is not needed because
answers are parsed from text), permutation pi, m demonstrated pairs; 4 unseen queries.
Conditions:
  cot_map   code given explicitly (execution with binding, with reasoning)
  cot_told  rule stated, code secret (binding inference + execution, with reasoning)
The model must end with 'CODE: s=number, ...' and 'ANSWERS: q1, q2, q3, q4'.
Measures: answer accuracy on the 4 unseen queries; mapping score of the stated code (modulo automorphisms);
whether the stated code is a bijection; whether the stated code is consistent with ALL demonstrations;
whether the answers follow from the stated code (coherence of the structure the model reports).
GPU use (Ollama only): checked before every episode; skipped if another compute process is using the GPU or if
used memory would exceed the budget.
"""
import json, re, sys, time, subprocess
import numpy as np
import prb_common as P
import ollama_client as O

POOL_WORDS = None


def pool_words():
    global POOL_WORDS
    if POOL_WORDS is None:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(P.MID, local_files_only=True)
        POOL_WORDS = [w for w, _ in P.symbol_pool(tok)]
    return POOL_WORDS


def gpu_ok(budget_mib=5632, total_mib=12288):
    q = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,process_name,used_memory", "--format=csv,noheader"],
                       capture_output=True, text=True).stdout.strip()
    used = int(subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                              capture_output=True, text=True).stdout.strip().split()[0])
    # On Windows (WDDM) every desktop app with a graphics context is listed with memory 'N/A'. Only processes with an
    # actual VRAM allocation count as other GPU users; total usage must leave >= 1 GB headroom after Ollama's ~4.6 GB.
    others = []
    for l in q.splitlines():
        parts = [x.strip() for x in l.split(",")]
        if len(parts) >= 3 and "ollama" not in parts[1].lower():
            mem = parts[-1].replace("MiB", "").strip()
            if mem.isdigit() and int(mem) > 200:
                others.append(l)
    ollama_loaded = "ollama" in q.lower()
    need = 0 if ollama_loaded else 4600
    return (len(others) == 0 and used + need < total_mib - 1024 and used < budget_mib + 1100), used, others


def T_inv(pi, i, j, n):
    return int(np.argsort(pi)[(pi[i] + pi[j]) % n])


def build(cond, n, syms, pi, demos, queries, direct=False):
    lines = "\n".join(f"{syms[i]} + {syms[j]} = {syms[k]}" for i, j, k in demos)
    s = (f"The symbols {', '.join(syms)} each stand for a different number from 0 to {n - 1}. "
         f"Every line below is a true statement of addition modulo {n} written with these symbols.\n")
    if cond in ("cot_map", "direct_map"):
        s += "The code is: " + ", ".join(f"{syms[i]} = {pi[i]}" for i in range(n)) + ".\n"
    else:
        s += "The code (which number each symbol stands for) is secret.\n"
    s += "\n" + lines + "\n\nQuestions:\n" + "\n".join(f"{q + 1}) {syms[i]} + {syms[j]} = ?" for q, (i, j) in enumerate(queries))
    s += ("\n\nWork it out. If several codes are consistent with all the lines, you may give any one of them "
          "(they give the same answers). At the end, output exactly two lines:\n"
          f"CODE: " + ", ".join(f"{w}=<number>" for w in syms) + "\n"
          "ANSWERS: <symbol for 1>, <symbol for 2>, <symbol for 3>, <symbol for 4>\n"
          "Each answer must be one of the symbols (not a number).")
    if direct:
        s = s.replace("Work it out. ", "Do not explain or show any work; answer immediately. ")
    return s


def parse(text, syms, n):
    code, answers = None, None
    m = re.findall(r"CODE:\s*(.+)", text)
    if m:
        d = {}
        for w, v in re.findall(r"([a-z]+)\s*=\s*(\d+)", m[-1]):
            if w in syms: d[w] = int(v)
        if len(d) == n: code = [d[w] for w in syms]
    m = re.findall(r"ANSWERS:\s*(.+)", text)
    if m:
        toks = re.findall(r"[a-z]+", m[-1])
        answers = [syms.index(t) if t in syms else -1 for t in toks][:4]
    return code, answers


def episode(n, seed, m, think=True):
    words = pool_words()
    rng = np.random.default_rng(5000 + 100 * n + seed)
    syms = [words[i] for i in rng.choice(len(words), n, replace=False)]
    pi = [int(v) for v in rng.permutation(n)]
    pairs = [(i, j) for i in range(n) for j in range(n)]
    sel = rng.choice(len(pairs), m, replace=False)
    demos = [(pairs[d][0], pairs[d][1], T_inv(pi, pairs[d][0], pairs[d][1], n)) for d in sel]
    dset = {(i, j) for i, j, _ in demos}
    unseen = [p for p in pairs if p not in dset]
    queries = [unseen[q] for q in rng.choice(len(unseen), 4, replace=False)]
    truth = [T_inv(pi, i, j, n) for i, j in queries]
    rec = dict(n=n, seed=seed, m=m, syms=syms, pi=pi, csp_n_solutions=len(P.csp_consistent(n, demos)))
    for cond in ["direct_map", "direct_told", "cot_map", "cot_told"]:
        ok, used, apps = gpu_ok()
        if not ok:
            rec[cond] = dict(skipped=True, gpu_used=used, apps=apps); continue
        direct = cond.startswith("direct")
        if direct:
            r = O.chat(build(cond, n, syms, pi, demos, queries, direct=True), think=False, temperature=0.0, seed=seed,
                       num_gpu=99, num_predict=400, num_ctx=24576)
        else:
          r = O.chat(build(cond, n, syms, pi, demos, queries), think=think, temperature=0.6, top_p=0.95, top_k=20, seed=seed, num_gpu=99, num_predict=int(__import__("os").environ.get("Z3_PRED", "22000")), num_ctx=24576)
        code, ans = parse(r["content"], syms, n)
        res = dict(secs=r["secs"], eval_count=r["eval_count"], done=r["done_reason"], gpu_used_before=used,
                   parsed_code=code is not None, parsed_answers=ans is not None and len(ans) == 4)
        if ans is not None and len(ans) == 4:
            res["acc"] = float(np.mean([a == t for a, t in zip(ans, truth)]))
        if code is not None:
            res["map_score"] = P.mapping_score(code, pi, n)
            res["code_bijection"] = len(set(code)) == n and all(0 <= c < n for c in code)
            if res["code_bijection"]:
                res["code_consistent_with_demos"] = float(np.mean([(code[i] + code[j]) % n == code[k] for i, j, k in demos]))
                if ans is not None and len(ans) == 4:
                    implied = [T_inv(code, i, j, n) for i, j in queries]
                    res["answers_follow_code"] = float(np.mean([a == b for a, b in zip(ans, implied)]))
        res["content_tail"] = r["content"][-400:]
        res["thinking_head"] = r["thinking"][:1500]
        res["thinking_tail"] = r["thinking"][-2500:]
        rec[cond] = res
    return rec


if __name__ == "__main__":
    n = int(sys.argv[1]); ms = [int(x) for x in sys.argv[2].split(",")]; seeds = range(int(sys.argv[3]))
    out = open(f"z3_n{n}.jsonl", "a")
    for seed in seeds:
        for m in ms:
            rec = episode(n, seed, m)
            out.write(json.dumps(rec) + "\n"); out.flush()
            print(n, seed, m, "nsol", rec["csp_n_solutions"],
                  {c: {k: rec[c].get(k) for k in ("acc", "map_score", "code_consistent_with_demos", "answers_follow_code", "eval_count", "secs", "skipped")} for c in ("direct_map", "direct_told", "cot_map", "cot_told")}, flush=True)
