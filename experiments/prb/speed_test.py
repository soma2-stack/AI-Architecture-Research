import time, torch, sys
torch.set_num_threads(int(sys.argv[2]) if len(sys.argv) > 2 else 12)
from transformers import AutoTokenizer, AutoModelForImageTextToText
MID = "Qwen/Qwen3-VL-4B-Instruct"
dt = torch.bfloat16 if sys.argv[1] == "bf16" else torch.float32
tok = AutoTokenizer.from_pretrained(MID, local_files_only=True)
model = AutoModelForImageTextToText.from_pretrained(MID, local_files_only=True, dtype=dt).eval()
for L in [40, 300, 800]:
    ids = torch.randint(1000, 20000, (1, L))
    with torch.no_grad():
        model(input_ids=ids)
        t0 = time.time(); model(input_ids=ids); print(sys.argv[1], "len", L, "forward s", round(time.time() - t0, 2), flush=True)
