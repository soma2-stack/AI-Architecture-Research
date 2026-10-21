# Learned gate repair: fixed protocol, 2026-10-20

Question: Can end-task answer loss plus a generic gate-activity penalty reduce idle overwrites without write labels, grammar in inference, or an oracle mask?

Mechanism: retain the original sigmoid gate and all original transitions. Fine-tune only its existing two-layer MLP. Loss = answer cross entropy + 0.1 * mean gate activity over all history and query tokens. The penalty treats intended and irrelevant writes equally; no write labels, addresses or boundaries enter this objective. Known limitation: this is ordinary sparse gating, not a novel computational primitive.

Starting states: existing eight-slot gradual-fade checkpoints for seeds 17,29,43, chosen from the prior audit before any new test scores. Their earlier address-alignment guidance is inherited equally and explicitly disclosed. No claims about learning addressing unaided. Halfway-fade is outside this small repair screen.

Arms: original frozen checkpoint (context only); answer-only gate continuation (fair control and coefficient-zero training ablation); sparse gate continuation (candidate); tail-frozen oracle for each arm (diagnostic only). Only the gate is trainable in both continuations; embeddings, addresses, values, GRU and head are fixed. Restore the original gate in the candidate as a parameter-local causal check. No added parameters, no inference changes.

Training: 128 updates, AdamW lr .003, default weight decay .01, clip norm 1; 12 histories/update, eight queried facts/history; 64 guaranteed idle tail tokens after the ordinary 32-token body. Identical paired data seeds 6100000000 + seed*1000003 + step*8191. No hyperparameter search or selection by final test. Short extended tails shared by both arms provide a learnable retention signal.

Fresh test: 128 histories/seed, chunks32, common seeds 7100000000 + seed*100003 + chunk_start*677. Same initial 32-token write bodies and labels across all arms and horizons. Guaranteed no-write tails exactly 256,1024,4080 tokens (old generator delay argument = tail+16). Record both per-bit and all-eight-correct recall, paired short/body recall retention, bank cosine/relative drift, idle gate mean/max/integral, intended-write gate activity (diagnostics only), wall/process CPU time, and parameters. Additional fixed-vocabulary tail distributions remain untested.

Success criteria: candidate beats answer-only control in mean whole recall at 4080 by >=10 percentage points; no seed loses >5 points at any horizon; idle gate integral falls by >=50% in every seed relative to the control. Report the criteria separately; no threshold changes after seeing test outcomes. This is a three-initialization repair test, not broad architectural superiority.

Verification: compare optimized shared-prefix logits and gate gradients with native forward before training, check parity after training, assert only gate tensors changed, exact input hashes paired, assert original source/checkpoint/report hashes unchanged. Causal training ablation removes the sparsity coefficient; restored-gate inference must reproduce the original checkpoint. Save all predictions, objectives and trained weights. CPU tensors only, <=4 intra-op threads, one inter-op thread, no workers or GPU. Serial execution, no new directories. No changes to original files, proofs or checkpoints; no PR or contact.
