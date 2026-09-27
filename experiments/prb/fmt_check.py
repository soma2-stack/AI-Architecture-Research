import numpy as np, prb_common as P
tok, model = P.load(threads=6)
enc = lambda s: tok.encode(s, add_special_tokens=False)
print([tok.decode([t]) for t in enc("3+5=1\n")])
DIG = [enc(str(d))[0] for d in range(10)]
PLUS, EQ, NL = enc("+")[0], enc("=")[0], enc("\n")[0]
head = enc("Each line computes (x + y) mod 7.\n")
cache, plen = P.prefix_cache(model, head)
sufs = [[DIG[a], PLUS, DIG[b], EQ] for a in range(7) for b in range(7)]
lg = P.score_suffixes_batched(model, cache, plen, sufs, DIG[:7])
print("zero-shot no-space digit table acc:", float((lg.argmax(1) == P.table(7).reshape(-1)).mean()))
# symbol tokens without leading space: which pool words are single tokens without space?
pool = P.symbol_pool(tok)
nospace = [(w, enc(w)) for w, _ in pool]
ok = [(w, t[0]) for w, t in nospace if len(t) == 1]
print("no-space single-token symbols:", len(ok), ok[:15])
