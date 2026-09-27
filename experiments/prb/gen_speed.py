import time, torch, prb_common as P
tok, model = P.load()
msgs = [{"role": "user", "content": "The symbols pig, der, cus stand for numbers. The code is: pig = 3, der = 0, cus = 1. Compute pig + cus mod 7 and give the answer as a symbol. Think step by step briefly."}]
ids = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt")
ids = ids["input_ids"] if isinstance(ids, dict) or hasattr(ids, "keys") else ids
t0 = time.time()
with torch.no_grad():
    out = model.generate(input_ids=ids, max_new_tokens=80, do_sample=False)
dt = time.time() - t0
new = out[0, ids.shape[1]:]
print("tokens", len(new), "secs", round(dt, 1), "tok/s", round(len(new) / dt, 2))
print(tok.decode(new))
