"""Exploratory pilot of learned exact-closure gates on legacy task (uncommitted)."""
import sys, time
import torch, torch.nn.functional as F
sys.path.insert(0, "/home/user/AI-Architecture-Research")
from prototypes.rnn_llm_architecture.experiment_002 import build, _slot_targets
from prototypes.rnn_llm_architecture.experiment_004 import _paired_inputs
from prototypes.rnn_llm_architecture.learning_pilot import make_batch, BIT0, BIT1, QUERY_A, QUERY_B
from prototypes.rnn_llm_architecture.event_gated import EventGatedConfig, EventGatedLanguageModel, KeepGatedGRULanguageModel
from prototypes.rnn_llm_architecture.gated import GatedConfig

torch.set_num_threads(1)
variant, delay, seed, steps = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); LR = float(sys.argv[5]) if len(sys.argv) > 5 else .002

def make(v):
    if v.startswith("eg_"):
        _, mode, shift = v.split("_")
        return EventGatedLanguageModel(EventGatedConfig(vocab_size=16, width=32, layers=2, protected_channels=8,
            cell_type="protected", seed=seed, gate_mode=mode, token_shift=shift == "shift"))
    if v.startswith("bias"):
        b = float(v[4:])
        return EventGatedLanguageModel(EventGatedConfig(vocab_size=16, width=32, layers=2, protected_channels=8,
            cell_type="protected", seed=seed, gate_mode="soft", slow_write_bias=-b))
    if v.startswith("kgru_"):
        _, mode, kb = v.split("_")
        return KeepGatedGRULanguageModel(GatedConfig(vocab_size=16, width=32, layers=2, cell_type="gru", seed=seed),
                                         gate_mode=mode, keep_bias=float(kb))
    return build(v, seed)

model = make(variant)
opt = torch.optim.AdamW(model.parameters(), lr=LR)
t0 = time.time(); hist = []
for step in range(steps):
    model.train()
    bs = seed*1_000_003 + step*8191 + delay*17 + 97
    x, y, _ = _paired_inputs(delay, 16, seed=bs)
    opt.zero_grad(); loss = F.cross_entropy(model(x)[0][:, -1, BIT0:BIT1+1], y); loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); hist.append(loss.item())
model.eval(); out = []
for d in (delay, 2*delay, 4*delay):
    ids, _, meta = make_batch("selective", d, 512, seed=seed+1_000_000)
    exp = _slot_targets(ids[:, :-1], d)
    a = ids.clone(); b = ids.clone(); a[:, -1] = QUERY_A; b[:, -1] = QUERY_B
    with torch.no_grad():
        lg = model(torch.cat((a, b)))[0][:, -1, BIT0:BIT1+1]
    pred = torch.stack((lg[:512].argmax(-1), lg[512:].argmax(-1)), 1)
    uneq = exp[:, 0] != exp[:, 1]
    out.append(f"{d}:{pred.eq(exp).all(1)[uneq].float().mean():.3f}")
lc = [round(sum(hist[i:i+50])/50, 3) for i in range(0, steps, 50)]
print(f"{variant:18s} lr{LR} seed{seed} train{delay} steps{steps} unequal " + " ".join(out), "loss50", lc, f"{time.time()-t0:.0f}s", flush=True)
