import numpy as np, torch, time
import prb_common as P
tok, model = P.load()
pool = P.symbol_pool(tok)
print("pool size", len(pool), "sample", [w for w, _ in pool[:25]])
# prefix-cache equivalence
prefix = tok.encode("Each line computes (x + y) mod 7.\n 3 + 5 = 1\n 6 + 6 = 5\n 2 + 4 = 6\n", add_special_tokens=False)
suf = tok.encode(" 4 + 5 =", add_special_tokens=False) + [220]
print("suffix tokens", [tok.decode([t]) for t in suf])
digits = [tok.encode(str(d), add_special_tokens=False)[0] for d in range(7)]
t0 = time.time(); full = P.full_logits(model, prefix + suf)[digits]; t1 = time.time()
cache, plen = P.prefix_cache(model, prefix)
sc = P.score_suffixes(model, cache, plen, [suf, suf], digits); t2 = time.time()
print("full", np.round(full, 3), "pred", int(full.argmax()))
print("cached", np.round(sc[0], 3), "again", np.round(sc[1], 3), "max abs diff", float(np.abs(full - sc[0]).max()), float(np.abs(sc[0]-sc[1]).max()))
print("time full", round(t1-t0,2), "cached two", round(t2-t1,2))
w = [x for x, _ in pool[:3]]
line = f" {w[0]} + {w[1]} = {w[2]}\n"
print(repr(line), [tok.decode([t]) for t in tok.encode(line, add_special_tokens=False)])
