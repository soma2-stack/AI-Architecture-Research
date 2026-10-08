"""Exploratory (uncommitted) mechanism diagnostics on the original protected model."""
import sys, time, json
import torch, torch.nn.functional as F
sys.path.insert(0, "/home/user/AI-Architecture-Research")
from prototypes.rnn_llm_architecture.experiment_002 import build, _slot_targets
from prototypes.rnn_llm_architecture.experiment_004 import paired_query_loss, _paired_inputs
from prototypes.rnn_llm_architecture.learning_pilot import make_batch, BIT0, BIT1, QUERY_A, QUERY_B

torch.set_num_threads(1)
variant = sys.argv[1]; delay = int(sys.argv[2]); seed = int(sys.argv[3]); steps = int(sys.argv[4])

model = build(variant, seed)
opt = torch.optim.AdamW(model.parameters(), lr=.002)
t0 = time.time()
for step in range(steps):
    model.train()
    bs = seed*1_000_003 + step*8191 + delay*17 + 97
    opt.zero_grad(); loss = paired_query_loss(model, delay, 16, seed=bs); loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step()
print(f"trained {variant} d={delay} s={seed} steps={steps} loss={loss.item():.3f} {time.time()-t0:.1f}s")

# D1 behaviour stratification
model.eval()
N = 1024
ids, _, meta = make_batch("selective", delay, N, seed=seed+1_000_000)
exp = _slot_targets(ids[:, :-1], delay)
a = ids.clone(); b = ids.clone(); a[:, -1] = QUERY_A; b[:, -1] = QUERY_B
with torch.no_grad():
    lg = model(torch.cat((a, b)))[0][:, -1, BIT0:BIT1+1]
pred = torch.stack((lg[:N].argmax(-1), lg[N:].argmax(-1)), 1)
us = meta["update_slot"]; uv = meta["last_written_value"]
unt = 1 - us
pred_unt = pred.gather(1, unt[:, None])[:, 0]; tgt_unt = exp.gather(1, unt[:, None])[:, 0]
pred_upd = pred.gather(1, us[:, None])[:, 0]; tgt_upd = exp.gather(1, us[:, None])[:, 0]
same = tgt_unt.eq(uv)
print("D1 updated acc", pred_upd.eq(tgt_upd).float().mean().item())
print("D1 untouched acc | untouched==update", pred_unt[same].eq(tgt_unt[same]).float().mean().item(),
      " | untouched!=update", pred_unt[~same].eq(tgt_unt[~same]).float().mean().item())
print("D1 P(both answers == last written value)", pred.eq(uv[:, None]).all(1).float().mean().item())
print("D1 P(pred A == pred B)", pred[:, 0].eq(pred[:, 1]).float().mean().item())
uneq = exp[:, 0] != exp[:, 1]
print("D1 pair on unequal", pred.eq(exp).all(1)[uneq].float().mean().item())

# D2 slow/fast decomposition probes at stages
prefix = ids[:, :-1]
upd_pos = 4 + delay//2
stages = {"after_init": 4, "after_update": upd_pos+2, "final": prefix.shape[1]}
with torch.no_grad():
    _, _, hist = model(prefix, return_history=True)  # [B,T,L,W]

def logistic_probe(X, y, Xt, yt, steps=300):
    mu, sd = X.mean(0), X.std(0) + 1e-6
    X = (X-mu)/sd; Xt = (Xt-mu)/sd
    w = torch.zeros(X.shape[1], requires_grad=True); b0 = torch.zeros(1, requires_grad=True)
    o = torch.optim.Adam([w, b0], lr=.05)
    for _ in range(steps):
        o.zero_grad(); l = F.binary_cross_entropy_with_logits(X@w+b0, y.float()) + 1e-3*w.square().sum(); l.backward(); o.step()
    return ((Xt@w+b0 > 0).long() == yt).float().mean().item()

half = N//2
init_a = torch.where(prefix[:, 0] == 5, prefix[:, 1]-BIT0, prefix[:, 3]-BIT0)
init_b = torch.where(prefix[:, 0] == 5, prefix[:, 3]-BIT0, prefix[:, 1]-BIT0)
masks = [c.masks for c in model.cells] if hasattr(model.cells[0], "masks") else None
for name, t in stages.items():
    H = hist[:, t-1]  # [B,L,W]
    feats = {"all": H.reshape(N, -1)}
    if masks is not None:
        slow = torch.cat([F.linear(H[:, l], masks[l]) for l in range(H.shape[1])], 1)
        fast = torch.cat([H[:, l] - F.linear(F.linear(H[:, l], masks[l]), masks[l].T) for l in range(H.shape[1])], 1)
        feats.update({"slow": slow, "fast": fast})
    tgts = {"A_init": init_a, "B_init": init_b} if name == "after_init" else {"A_final": exp[:, 0], "B_final": exp[:, 1], "untouched": tgt_unt, "update_val": uv}
    for fn, X in feats.items():
        res = {k: round(logistic_probe(X[:half], y[:half], X[half:], y[half:]), 3) for k, y in tgts.items()}
        print("D2", name, fn, X.shape[1], res)

# D3 slow gates at the update bit token, by update slot
if masks is not None:
    with torch.no_grad():
        x = model.embedding(prefix)
        for l, (cell, norm) in enumerate(zip(model.cells, model.norms)):
            gates = torch.sigmoid(cell.slow_gate(x))  # [B,T,R] (input-only gates)
            g_upd = gates[:, upd_pos+1]
            print(f"D3 L{l} gate@update-bit | slot A:", [round(v, 3) for v in g_upd[us == 0].mean(0).tolist()])
            print(f"D3 L{l} gate@update-bit | slot B:", [round(v, 3) for v in g_upd[us == 1].mean(0).tolist()])
            dis = gates[:, 4:upd_pos].reshape(-1, gates.shape[-1]).mean(0)
            print(f"D3 L{l} gate@distractor mean:", [round(v, 4) for v in dis.tolist()])
            print(f"D3 L{l} gate@initial bits pos1,pos3:", [round(v, 3) for v in gates[:, 1].mean(0).tolist()], [round(v, 3) for v in gates[:, 3].mean(0).tolist()])
            x = norm(hist[:, :, l])

# D4 gradient conflict between updated- and untouched-slot query losses
model.train()
ids2, _, meta2 = make_batch("selective", delay, 256, seed=seed+2_000_000)
exp2 = _slot_targets(ids2[:, :-1], delay)
us2 = meta2["update_slot"]
qa = ids2.clone(); qa[:, -1] = QUERY_A; qb = ids2.clone(); qb[:, -1] = QUERY_B
lg2 = model(torch.cat((qa, qb)))[0][:, -1, BIT0:BIT1+1]
y2 = torch.cat((exp2[:, 0], exp2[:, 1]))
qslot = torch.cat((torch.zeros(256, dtype=torch.long), torch.ones(256, dtype=torch.long)))
is_upd = qslot.eq(torch.cat((us2, us2)))
li = F.cross_entropy(lg2, y2, reduction="none")
params = [p for p in model.parameters()]
gu = torch.autograd.grad(li[is_upd].mean(), params, retain_graph=True)
gn = torch.autograd.grad(li[~is_upd].mean(), params)
vu = torch.cat([g.flatten() for g in gu]); vn = torch.cat([g.flatten() for g in gn])
print("D4 loss updated", li[is_upd].mean().item(), "untouched", li[~is_upd].mean().item())
print("D4 all-params cos(g_upd,g_unt)", F.cosine_similarity(vu, vn, 0).item(), "|sum|/(|u|+|n|)", ((vu+vn).norm()/(vu.norm()+vn.norm())).item())
if masks is not None:
    names = [n for n, _ in model.named_parameters()]
    sel = [i for i, n in enumerate(names) if "slow_gate" in n]
    vu2 = torch.cat([gu[i].flatten() for i in sel]); vn2 = torch.cat([gn[i].flatten() for i in sel])
    print("D4 slow-gate cos", F.cosine_similarity(vu2, vn2, 0).item(), "|sum|/(|u|+|n|)", ((vu2+vn2).norm()/(vu2.norm()+vn2.norm())).item())
