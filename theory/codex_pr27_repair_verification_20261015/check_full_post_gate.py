"""Fresh, CPU-only regression for the full post-gate formula; no author imports."""
import hashlib
import json
import pathlib
import time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent

def main():
    started = time.perf_counter()
    rng = np.random.default_rng(20261015)
    errors, omitted, cases = [], [], []
    for n in (32, 33, 64, 129):
        k, d = n//2, n//4
        a, lam = 1-1/n, 1/(100*n)
        u = np.ones(k)/np.sqrt(k)
        w = np.eye(k)[0]-u
        U = np.eye(k)-np.outer(w,w)/(1-1/np.sqrt(k))
        P = np.eye(k)
        P[:d,:d] = np.roll(np.eye(d),1,axis=0)
        O = U@P@U
        R = np.zeros((n,n)); R[:k,:k] = a*O; R[k:,k:] = lam*np.eye(n-k)
        sig = np.tanh(.05)
        for _ in range(20): sig = np.tanh(lam*sig+.05)
        v = np.eye(k)[d]  # off-cycle memory parameter, no row-0 injection
        h, b = np.zeros(n), np.zeros(k)
        for t in range(1,41):
            c = np.mean(h[k:])/sig
            x = np.zeros(n)
            # Zero-input start gives a legal exact t=2 counterexample.
            if t>2: x[rng.choice(n,2,replace=False)] = rng.uniform(-.3,.3,2)
            h = np.tanh(R@h+x+.05)
            gates = 1-h[:k]**2
            new_b = gates*(a*O@b+c*v)
            corrected = a*U@(gates*(U@P@U@b))+c*U@(gates*v)
            old = a*U@(gates*(U@P@U@b))+c*U@v
            errors.append(float(np.max(np.abs(U@new_b-corrected))))
            omitted.append(float(np.linalg.norm(U@new_b-old)))
            if t==2:
                assert c>0 and np.linalg.norm(U@new_b-old)>1e-5
                cases.append({'n':n,'T':2,'inputs':'all zero',
                              'c2':float(c),'gate_at_probe':float(gates[d]),
                              'old_identity_error_l2':float(np.linalg.norm(U@new_b-old)),
                              'exact_error_formula':'c2 * (1-g2[d])'})
                assert abs(np.linalg.norm(U@new_b-old)-c*(1-gates[d]))<1e-13
            b = new_b
    assert max(errors)<1e-12
    n0=100_000_000; k0=n0//2
    gamma0=1/(1-1/np.sqrt(k0)); lam0=1/(100*n0)
    sig0=np.tanh(.05)
    for _ in range(10): sig0=np.tanh(lam0*sig0+.05)
    # For zero raw inputs O1 has off-cycle entries -gamma/sqrt(k).
    z2=.05-(1-1/n0)*gamma0*np.tanh(.05)/np.sqrt(k0)
    c2=np.tanh(.05)/sig0
    assert z2>0
    cases.append({'n':n0,'T':2,'inputs':'all zero; scalar formula, no large array',
                  'old_identity_error_l2':float(c2*np.tanh(z2)**2),
                  'exact_error_formula':'c2*tanh(.05-a*gamma*tanh(.05)/sqrt(k))**2'})
    proof=ROOT/'theory/claude_narrow_capture_hub_20261013/PROOF.md'
    result={'reviewed_base':'a67be6da53a539198fc82264606b88d74de67a00',
            'proof_sha256_bytes':hashlib.sha256(proof.read_bytes()).hexdigest(),
            'full_recurrence_steps':len(errors),'maximum_corrected_residual':max(errors),
            'maximum_old_residual':max(omitted),'legal_zero_input_counterexamples':cases,
            'scope':'Exact reference-credit identity, including a theorem-scale scalar counterexample to the old formula. Not a robust section or a counterexample to Theorem 1.',
            'training':False,'gpu':False,'seconds':time.perf_counter()-started}
    (HERE/'full_post_gate_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
