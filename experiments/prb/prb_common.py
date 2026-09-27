"""
Pretrained Structural Rebinding (Part Z) — shared harness for Qwen3-VL-4B-Instruct (text-only, fp32, CPU).
Only existing local weights are used (local_files_only=True). Nothing is downloaded or installed.
"""
import itertools, math, random, time
import numpy as np
import torch

MID = "Qwen/Qwen3-VL-4B-Instruct"
_M = {}


def load(threads=12):
    if "model" in _M:
        return _M["tok"], _M["model"]
    torch.set_num_threads(threads)
    from transformers import AutoTokenizer, AutoModelForImageTextToText
    tok = AutoTokenizer.from_pretrained(MID, local_files_only=True)
    model = AutoModelForImageTextToText.from_pretrained(MID, local_files_only=True, dtype=torch.float32).eval()
    _M["tok"], _M["model"] = tok, model
    return tok, model


# ------------------------------------------------------------------------------------------ symbols
STOP = set("""one two six ten won too for four five nine zero nil sum add mod max min top end first last next prev big
low high all any none odd even pair twin dual tri uni mono duo uno dos tres ein sei sex sep oct nov dec kilo mega
giga plus minus equal equals times half both each few many more less num int var val key map set get put new old
yes not and the you are was his her its our out who how why may can let run""".split())


def symbol_pool(tok, n_max=400, seed=0):
    rng = random.Random(seed)
    C, V = "bcdfghjklmnprstvwxz", "aeiou"
    cands = set()
    for c1 in C:
        for v in V:
            for c2 in C:
                cands.add(c1 + v + c2)
    cands = sorted(cands)
    rng.shuffle(cands)
    pool = []
    for w in cands:
        if w in STOP:
            continue
        ids = tok.encode(" " + w, add_special_tokens=False)
        if len(ids) == 1 and tok.decode(ids) == " " + w:
            pool.append((w, ids[0]))
        if len(pool) >= n_max:
            break
    return pool


# ------------------------------------------------------------------------------------------ rule / worlds
def table(n):
    return np.add.outer(np.arange(n), np.arange(n)) % n


def automorphisms(n):
    return [u for u in range(1, n) if math.gcd(u, n) == 1]


def mapping_score(pi_hat, pi, n):
    """fraction of symbols mapped correctly, maximised over automorphisms x -> u*x (they leave answers unchanged)."""
    best = 0.0
    for u in automorphisms(n):
        best = max(best, float(np.mean([pi_hat[i] == (u * pi[i]) % n for i in range(n)])))
    return best


def coherence(pred, n):
    """pred[i][j] = predicted symbol index for symbols i, j (all n^2 pairs).
    Returns the maximal fraction of entries explained by ONE relabelling sigma of Z_n
    (pred[i][j] == sigma^-1((sigma(i) + sigma(j)) mod n)) and the maximising sigma."""
    T = table(n); pred = np.asarray(pred)
    best, arg = -1.0, None
    for sig in itertools.permutations(range(n)):
        sig = np.array(sig); inv = np.argsort(sig)
        expl = inv[T[sig[:, None], sig[None, :]]]
        a = float((expl == pred).mean())
        if a > best:
            best, arg = a, sig
    return best, arg


def csp_consistent(n, demos):
    """all bijections pi (symbol -> number) consistent with demos (list of (i, j, k) symbol triples)."""
    T = table(n); sols = []
    for pi in itertools.permutations(range(n)):
        if all(T[pi[i], pi[j]] == pi[k] for i, j, k in demos):
            sols.append(pi)
    return sols


# ------------------------------------------------------------------------------------------ scoring with prefix cache
@torch.no_grad()
def prefix_cache(model, ids):
    out = model(input_ids=torch.tensor([ids]), use_cache=True)
    return out.past_key_values, len(ids)


@torch.no_grad()
def score_suffixes(model, cache, plen, suffixes, cand_ids):
    """For each suffix (token list), logits at its last position restricted to cand_ids. Cache is cropped back."""
    res = []
    for suf in suffixes:
        out = model(input_ids=torch.tensor([suf]), past_key_values=cache, use_cache=True)
        lg = out.logits[0, -1]
        res.append(lg[cand_ids].float().numpy())
        cache.crop(plen)
    return np.array(res)


@torch.no_grad()
def full_logits(model, ids):
    return model(input_ids=torch.tensor([ids])).logits[0, -1].float().numpy()


@torch.no_grad()
def score_suffixes_batched(model, cache, plen, suffixes, cand_ids, B=16):
    """Same as score_suffixes but runs equal-length suffixes in batches over a replicated prefix cache."""
    import copy
    res = []
    for i in range(0, len(suffixes), B):
        chunk = suffixes[i:i + B]
        c = copy.deepcopy(cache)
        c.batch_repeat_interleave(len(chunk))
        out = model(input_ids=torch.tensor(chunk), past_key_values=c, use_cache=True)
        res.append(out.logits[:, -1][:, cand_ids].float().numpy())
    return np.concatenate(res)
