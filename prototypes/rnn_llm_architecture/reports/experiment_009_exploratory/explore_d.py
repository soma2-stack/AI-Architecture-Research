"""Why does a solved model fail at longer lengths? (uncommitted exploratory)"""
import sys, time, json
import torch, torch.nn.functional as F
sys.path.insert(0, "/home/user/AI-Architecture-Research")
from prototypes.rnn_llm_architecture.experiment_009 import *
from prototypes.rnn_llm_architecture.experiment_004 import _paired_inputs

torch.set_num_threads(1)
variant, seed, steps, task = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
model, oracle = build_variant(variant, seed)
opt = torch.optim.AdamW(model.parameters(), lr=.002)
t0 = time.time()
for step in range(steps):
    model.train()
    if task == "legacy":
        x, y, _ = _paired_inputs(64, 16, seed=seed*1_000_003 + step*8191 + 64*17 + 97)
    else:
        prefix, _ = make_two_slot_batch(64, 16, seed=batch_seed(seed, step, 64))
        tg = replay_slots(prefix)["final"]; x = with_queries(prefix); y = torch.cat((tg[:, 0], tg[:, 1]))
    opt.zero_grad(); loss = F.cross_entropy(query_logits(model, x, oracle), y); loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step()
    if step % 250 == 249:
        ev = evaluate_two_slot(model, oracle, 64, seed=seed+1_500_000, histories=256) if task != "legacy" else evaluate_legacy(model, oracle, 64, seed=seed+1_500_000, histories=256)
        print(step+1, round(loss.item(), 3), "unequal@64", round(ev["paired_on_unequal"], 3), flush=True)
print(variant, task, f"{time.time()-t0:.0f}s")
for d in (32, 64, 128, 256, 512):
    if task == "legacy":
        ev = evaluate_legacy(model, oracle, d, seed=seed+1_000_000, histories=512)
    else:
        ev = evaluate_two_slot(model, oracle, d, seed=seed+1_000_000, histories=512)
    print("eval", d, round(ev["paired_on_unequal"], 3), "same", round(ev.get("predicts_same_for_both", -1), 3),
          ev.get("baselines", {}))
g = gate_diagnostics(model, oracle, 64, seed=seed+4_000_000)
if g:
    for i, l in enumerate(g["layers"]):
        print("gates L", i, json.dumps({k: (v if not isinstance(v, dict) else {kk: round(vv, 4) for kk, vv in v.items() if vv is not None}) for k, v in l.items()}))
# fast retention per token class (protected family)
with torch.no_grad():
    prefix, _ = make_two_slot_batch(64, 256, seed=seed+5)
    _, _, hist = run_model(model, prefix, oracle, return_history=True)
    x = model.embedding(prefix)
    for i, (cell, norm) in enumerate(zip(model.cells, model.norms)):
        if hasattr(cell, "fast_gate"):
            r = torch.sigmoid(cell.fast_gate(x))
            wa, wb = marked_writes(prefix)
            dis = (prefix >= 8) & (prefix < 14)
            print("fast retention L", i, "distractor mean", round(float(r[dis].mean()), 3), "max-channel", round(float(r[dis].mean(0).max()), 3))
        x = norm(hist[:, :, i])
print(json.dumps(linear_state_probe(model, oracle, 64, seed=seed+3_000_000, train_n=2048, test_n=1024, transfer_delay=256)))
