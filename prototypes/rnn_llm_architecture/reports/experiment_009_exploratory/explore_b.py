"""Exploratory oracle-mask factorial pilot (uncommitted)."""
import sys, time
import torch, torch.nn.functional as F
sys.path.insert(0, "/home/user/AI-Architecture-Research")
from prototypes.rnn_llm_architecture.experiment_002 import build, _slot_targets
from prototypes.rnn_llm_architecture.experiment_004 import _paired_inputs
from prototypes.rnn_llm_architecture.learning_pilot import make_batch, BIT0, BIT1, QUERY_A, QUERY_B, WRITE_A, WRITE_B

torch.set_num_threads(1)
variant, delay, seed, steps, mode = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
R, L = 8, 2

def masks_for(ids, mode):
    B, T = ids.shape
    prev = torch.cat((torch.zeros(B, 1, dtype=torch.long), ids[:, :-1]), 1)
    is_bit = (ids == BIT0) | (ids == BIT1)
    wa = is_bit & (prev == WRITE_A); wb = is_bit & (prev == WRITE_B)
    m = torch.zeros(B, T, R)
    if mode in ("full", "route"):
        m[..., :R//2] = wa[..., None].float(); m[..., R//2:] = wb[..., None].float()
        if mode == "route":
            other = ~(wa | wb)
            m[other] = 1.0
    elif mode == "tag":
        m[:] = (wa | wb)[..., None].float()
    else:
        return None
    return m[:, :, None, :].expand(B, T, L, R).contiguous()

def fwd(model, ids):
    wm = masks_for(ids, mode)
    return model(ids, write_masks=wm)[0][:, -1, BIT0:BIT1+1]

model = build(variant, seed)
opt = torch.optim.AdamW(model.parameters(), lr=.002)
t0 = time.time()
for step in range(steps):
    model.train()
    bs = seed*1_000_003 + step*8191 + delay*17 + 97
    x, y, _ = _paired_inputs(delay, 16, seed=bs)
    opt.zero_grad(); loss = F.cross_entropy(fwd(model, x), y); loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step()
    if step % 100 == 99: print(step+1, round(loss.item(), 3), flush=True)

model.eval()
out = []
for d in (delay, 2*delay, 4*delay):
    ids, _, meta = make_batch("selective", d, 512, seed=seed+1_000_000)
    exp = _slot_targets(ids[:, :-1], d)
    a = ids.clone(); b = ids.clone(); a[:, -1] = QUERY_A; b[:, -1] = QUERY_B
    with torch.no_grad():
        lg = fwd(model, torch.cat((a, b)))
    pred = torch.stack((lg[:512].argmax(-1), lg[512:].argmax(-1)), 1)
    uneq = exp[:, 0] != exp[:, 1]
    out.append(f"d{d}: unequal {pred.eq(exp).all(1)[uneq].float().mean():.3f} all {pred.eq(exp).all(1).float().mean():.3f}")
print(variant, mode, f"train{delay} seed{seed} steps{steps}", " | ".join(out), f"{time.time()-t0:.0f}s")
