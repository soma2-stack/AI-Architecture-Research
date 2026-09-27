import torch, prb_common as P, z4_grad as Z
# verify: hidden_states[-1] @ E0[cand]^T equals model logits[cand] (tied, normed final state)
n = 7
cache, plen = P.prefix_cache(Z.model, Z.prefix_ids(n))
rows = Z.E0[Z.DIG[:n]].detach()
with torch.no_grad():
    emb = Z.line_embeds([(1, 2), (3, 4)], rows, None)
    h, logits = Z.lm_hidden(emb, cache)
    print("max diff hidden@rows vs logits:", float((h @ rows.T - logits[:, Z.DIG[:n]]).abs().max()))
