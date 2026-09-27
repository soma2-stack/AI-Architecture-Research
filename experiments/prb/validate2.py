import numpy as np, time, prb_common as P
tok, model = P.load()
prefix = tok.encode("Each line computes (x + y) mod 7.\n 3 + 5 = 1\n 6 + 6 = 5\n 2 + 4 = 6\n 1 + 1 = 2\n 5 + 3 = 1\n", add_special_tokens=False)
digits = [tok.encode(str(d), add_special_tokens=False)[0] for d in range(7)]
sufs = [tok.encode(f" {a} + {b} =", add_special_tokens=False) + [220] for a in range(7) for b in range(7)]
cache, plen = P.prefix_cache(model, prefix)
t0 = time.time(); s1 = P.score_suffixes(model, cache, plen, sufs[:16], digits); t1 = time.time()
s2 = P.score_suffixes_batched(model, cache, plen, sufs[:16], digits, B=16); t2 = time.time()
print("max diff", float(np.abs(s1 - s2).max()), "same argmax", bool((s1.argmax(1) == s2.argmax(1)).all()), "t seq", round(t1-t0,1), "t batch", round(t2-t1,1))
s = P.score_suffixes_batched(model, cache, plen, sufs, digits)
pred = s.argmax(1).reshape(7, 7)
print("digit table accuracy (5 demos, all 49 pairs):", float((pred == P.table(7)).mean()))
