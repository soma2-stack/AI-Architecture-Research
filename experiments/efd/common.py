"""
Experiment-First Discovery (EFD) — shared harness.
Small CPU models for diagnostic tasks: MLP, causal/bidirectional Transformer (pos: none/learned/sin/rope),
GRU, LSTM; generic training loop. Every run uses 1 torch thread so that 8-12 runs can go in parallel.
"""
import math, time, json, os, sys, random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.set_num_threads(1)


def seed_all(s):
    random.seed(s); np.random.seed(s); torch.manual_seed(s)


# ----------------------------------------------------------------------------------------------- models
class MLP(nn.Module):
    def __init__(self, d_in, d_out, h=256, layers=3):
        super().__init__()
        mods, d = [], d_in
        for _ in range(layers - 1):
            mods += [nn.Linear(d, h), nn.GELU()]; d = h
        mods += [nn.Linear(d, d_out)]
        self.net = nn.Sequential(*mods)

    def forward(self, x):
        return self.net(x)


class RNNSeq(nn.Module):
    """Token sequence -> per-position logits."""
    def __init__(self, vocab, n_out, d=128, kind="gru", layers=1):
        super().__init__()
        self.emb = nn.Embedding(vocab, d)
        self.rnn = (nn.GRU if kind == "gru" else nn.LSTM)(d, d, num_layers=layers, batch_first=True)
        self.out = nn.Linear(d, n_out)

    def forward(self, tok):
        h, _ = self.rnn(self.emb(tok))
        return self.out(h)


def rope(x, base=10000.0):
    # x: (B, H, T, D) ; rotate pairs
    B, H, T, D = x.shape
    half = D // 2
    freqs = base ** (-torch.arange(0, half, dtype=torch.float32) / half)
    t = torch.arange(T, dtype=torch.float32)
    ang = t[:, None] * freqs[None, :]
    cos, sin = ang.cos()[None, None], ang.sin()[None, None]
    x1, x2 = x[..., :half], x[..., half:2 * half]
    return torch.cat([x1 * cos - x2 * sin, x1 * sin + x2 * cos, x[..., 2 * half:]], dim=-1)


class Block(nn.Module):
    def __init__(self, d, heads, pos, causal):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.qkv = nn.Linear(d, 3 * d); self.proj = nn.Linear(d, d)
        self.ff = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
        self.h, self.pos, self.causal = heads, pos, causal

    def forward(self, x, mask=None):
        B, T, D = x.shape
        q, k, v = self.qkv(self.ln1(x)).view(B, T, 3, self.h, D // self.h).permute(2, 0, 3, 1, 4)
        if self.pos == "rope":
            q, k = rope(q), rope(k)
        a = F.scaled_dot_product_attention(q, k, v, attn_mask=mask, is_causal=(self.causal and mask is None))
        x = x + self.proj(a.transpose(1, 2).reshape(B, T, D))
        return x + self.ff(self.ln2(x))


class TransformerSeq(nn.Module):
    """Token sequence -> per-position logits. pos in {none, learned, sin, rope}."""
    def __init__(self, vocab, n_out, d=128, layers=3, heads=4, pos="rope", causal=True, max_len=4096):
        super().__init__()
        self.emb = nn.Embedding(vocab, d)
        self.pos = pos
        if pos == "learned":
            self.pe = nn.Embedding(max_len, d)
        self.blocks = nn.ModuleList([Block(d, heads, pos, causal) for _ in range(layers)])
        self.ln = nn.LayerNorm(d); self.out = nn.Linear(d, n_out)
        self.d = d

    def forward(self, tok, mask=None):
        x = self.emb(tok)
        T = tok.shape[1]
        if self.pos == "learned":
            x = x + self.pe(torch.arange(T))[None]
        elif self.pos == "sin":
            p = torch.arange(T, dtype=torch.float32)[:, None]
            i = torch.arange(0, self.d, 2, dtype=torch.float32)[None]
            ang = p / (10000 ** (i / self.d))
            pe = torch.zeros(T, self.d); pe[:, 0::2] = torch.sin(ang); pe[:, 1::2] = torch.cos(ang)
            x = x + pe[None]
        for b in self.blocks:
            x = b(x, mask)
        return self.out(self.ln(x))


def train_loop(model, batch_fn, steps, lr=1e-3, wd=0.0, clip=1.0, log_every=0, loss_fn=None):
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / 200) * max(0.05, 1 - s / steps))
    model.train()
    for s in range(steps):
        inp, tgt, msk = batch_fn()
        logits = model(inp)
        if loss_fn is not None:
            loss = loss_fn(logits, tgt, msk)
        else:
            l = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), tgt.reshape(-1), reduction="none")
            loss = (l * msk.reshape(-1)).sum() / msk.sum().clamp(min=1)
        opt.zero_grad(); loss.backward()
        if clip:
            torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
        opt.step(); sched.step()
        if log_every and s % log_every == 0:
            print(s, float(loss), flush=True)
    model.eval()
    return model


def pool_run(fn, jobs, procs=10):
    from multiprocessing import Pool
    with Pool(procs) as p:
        return p.map(fn, jobs, chunksize=1)
