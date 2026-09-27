import time, torch
torch.set_num_threads(12)
from transformers import AutoTokenizer, AutoModelForImageTextToText
MID = "Qwen/Qwen3-VL-4B-Instruct"
t0 = time.time()
tok = AutoTokenizer.from_pretrained(MID, local_files_only=True)
model = AutoModelForImageTextToText.from_pretrained(MID, local_files_only=True, dtype=torch.bfloat16)
model.eval()
print("loaded", round(time.time() - t0, 1), "s", type(model).__name__)
print("params (B)", round(sum(p.numel() for p in model.parameters()) / 1e9, 2))
txt = "Compute (x + y) mod 7.\n3 + 5 = 1\n6 + 6 = 5\n2 + 4 = 6\n4 + 5 ="
ids = tok(txt, return_tensors="pt").input_ids
print("tokens", ids.shape[1])
with torch.no_grad():
    t0 = time.time(); out = model(input_ids=ids); dt = time.time() - t0
lg = out.logits[0, -1].float()
digits = [tok.encode(" " + str(d), add_special_tokens=False) for d in range(7)]
print("digit tokens", digits)
print("forward s", round(dt, 2), "pred", tok.decode(lg.argmax()), {d: round(float(lg[t[0]]), 2) for d, t in zip(range(7), digits)})
emb = model.get_input_embeddings(); print("emb", emb.weight.shape, emb.weight.dtype)
print("lm_head tied", model.get_output_embeddings().weight.data_ptr() == emb.weight.data_ptr())
