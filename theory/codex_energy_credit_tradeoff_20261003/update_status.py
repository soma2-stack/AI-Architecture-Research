"""Insert a separated new-stage resume, preserving every prior notebook byte."""
from pathlib import Path
import hashlib
import json

stage=Path(__file__).resolve().parent
root=stage.parent.parent
notebook=root/'Codex_Research.md'
original=notebook.read_bytes()
old_hash=hashlib.sha256(original).hexdigest().upper()
expected='6FA41A6EEB1FC72550631BA757E5692E86FB4C1E1535B4D174904F5A61F91AAC'
if old_hash!=expected:
    raise RuntimeError('Notebook changed since the recorded pre-insertion snapshot; inspect before editing.')
heading=b'## Guardrails and current state'
heading_end=original.index(heading)+len(heading)
newline=b'\r\n' if original[heading_end:].startswith(b'\r\n') else b'\n'
anchor=heading+newline+newline
if original.count(anchor)!=1:
    raise RuntimeError('Expected one status insertion anchor.')
block='''### Energy versus robust-credit resume (2026-10-03, NEW stage)

- **Current search lens:** full ABSOLUTE raw-input energy versus actual legal-query-visible continuous credit dimension in the existing frozen dense tanh family; epsilon=.001. Theory only. This owner-authorized stage supersedes earlier STOP instructions for continuing this energy question. CreditLab, independent notebooks and architecture work are outside this task.
- **Accepted premises:** constant-gap Theta(n); near-critical full-model Omega_c(n^2)--O_c(n^2 log n); growing LOCAL radius Omega(n^(16/15)); constant LOCAL radius Omega(n^(19/18)); reviewed absolute-energy zero-credit error (L_n+H_R)/sqrt(n), L_n=O(log n), H_R=O(R_abs^2), hence no positive fixed margin at R_abs=o(n^(1/4)). These proofs were not reopened or modified; the owner's new acceptance supersedes old review-pending status text below.
- **Current stage:** new energy phase diagram, joint constructions and counted-window upper derived; written internal audit and bounded CPU diagnostics complete. ALL NEW THEOREMS REQUIRE INDEPENDENT HOSTILE REVIEW before acceptance. Old proof/status text below is historical evidence, not the active task instruction.
- **One channel:** an invariant off-cycle PAIR hold for 4n steps and common autonomous endpoint gives half-margin>.003 at full norm<=2sqrt(n), sufficiently large n. Leading constant-hold depth is zero and useful duration Theta(n). For ONE isolated row with a stationary bath, the entire selected legal-query signal is O(T/n) for short holds, so visible near-zero holds require Omega(sqrt(n)) norm. This is a restricted mechanism result; the global first-direction exponent interval remains [1/4,1/2].
- **Joint localized lower:** s pairs with 4e6<=s<=1e-12 n, freely evolving public clamped bath, bounded-spread pulse, common endpoint, D=floor(s/1000), half-margin>.01, dense error<4e-9. Full squared cost O(n sqrt(s)); norm<=100sqrt(n)s^(1/4). Hence d_F>=Omega(min{n,R_abs^4/n^2}) in its stated range: Omega(n^(2/3)) at n^(2/3) norm and Omega(n) at n^(3/4) norm. This never proves superlinearity.
- **Strongest new theorem:** complete temporal cosine periods cancel the EXACT finite startup term; rounded actual spatial modes preserve the joint kernel for a short packet. Full ledger: M>=1e-18 delta T^2/(n^(3/2)F^5)-100delta T^2/n^2-delta^3T^4/n^(7/2)-4e-9. With delta=1e-10, F=floor(log n), T=ceil(1e15 n^(3/4) F^(5/2)), d_F>=c n log n at FULL absolute norm O(n^(7/8)(log n)^(5/4)). Also Omega(n^(101/100)) at O(n^(9/10)). New, independently unreviewed.
- **Complete-cycle improvement:** T=d, exact temporal/spatial modes, F=floor(n^(1/15)/1e4), delta=1e-10/F^(5/2), preserve D>=n^(16/15)/(2e11) with FULL norm O(n), reducing the old n sqrt(log n) cost without changing historical proofs. Actual-gradient metric only; the old polynomial contract is not silently inferred.
- **New conservative upper:** counted actual recent window gives d_all<=min{C_epsilon n[1+R_abs^2+log(n/epsilon)], C'_epsilon n^2 log(n/epsilon)} in THIS frozen family. One-source-feature cap d_F<=min{r^2,C_epsilon n[1+R_abs^2+log(n/epsilon)]}. Accepted zero-credit certificate dominates below n^(1/4). No sharp dimension upper or full-model gap closure.
- **Closed directions / open questions:** n^(1/4) scalar hold fails; forced stationary bath violates the cube for many rows; independently visible axes do not give joint dimension; old low spatial frequencies lose the short-packet Gram bound; autonomous gaps erase carriers. Moving sparse windows/duty cycles remain unresolved. Global superlinear exponent bracket is [1/4,7/8], with polylog at the sufficient endpoint; n^(1/4) sharpness remains open.
- **Records/resources:** theory/codex_energy_credit_tradeoff_20261003/{PROOF,REPORT,PHASE_DIAGRAM,CHECKS}.md and NUMERICAL_EVIDENCE.json; 32 final internal checks, 64 scalar samples, 12 multi-pair reference samples and two finite packet cases. Numerics explicitly are not dimension proofs. Aggregate diagnostic CPU25.734375s/wall25.9945242s; final peak54.82MiB, one CPU thread, GPU0. Historical proofs and AGENTS preserved; only this separated resume is inserted into the notebook.
- **Exact next action:** independently hostile-review ONLY the new isolated-row, clamped-bath and short-packet lemmas, then strengthen the actual query-visible spatial energy upper or construct a moving sparse packet below exponent7/8. Do not reopen the accepted absolute-energy upper absent a genuine contradiction; continue only the energy-credit theory scope.

'''
encoded=block.replace('\n',newline.decode()).encode('utf-8')
position=original.index(anchor)+len(anchor)
updated=original[:position]+encoded+original[position:]
if updated[:position]+updated[position+len(encoded):]!=original:
    raise RuntimeError('Historical byte preservation failed.')
notebook.write_bytes(updated)
receipt={
    'notebook':'Codex_Research.md',
    'pre_insertion_sha256':old_hash,
    'post_insertion_sha256':hashlib.sha256(updated).hexdigest().upper(),
    'inserted_block_sha256':hashlib.sha256(encoded).hexdigest().upper(),
    'inserted_bytes':len(encoded),
    'historical_bytes_preserved_exactly':True,
    'scope':'One separated new-stage resume only; all previous bytes retained.'
}
(stage/'NOTEBOOK_STATUS_RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(receipt,indent=2))
