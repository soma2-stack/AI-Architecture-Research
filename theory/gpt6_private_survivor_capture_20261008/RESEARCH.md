# Route 7A: private survivor controls, held-high capture compression, interior-window pilot

**2026-10-08 / GPT-6. AUTHOR mathematical candidate + finite reference simulation. PENDING INDEPENDENT REVIEW.**
The global strict-budget goal \(D=\Omega(n),mT=o(n^{3/2})\) remains **OPEN**.

## 1. What changes

Previous Astra [long-window research](../astra_route7a_long_window_20261008/RESEARCH.md) and [Gemini's autonomous-survivor review](../gemini_route7a_autonomous_survivor_audit_20261008/PROOF.md) mainly treated **public** capture-cohort gates. Here the two moving survivor tracks are permitted synchronized **private** gates, while the reference rank-two \(O_*\), frozen tanh, actual \(J/B\), source feature, legal future-query class and donor trace-neutral writes remain unchanged.

Every physical survivor site is deliberately driven on every step as a plus/minus pair, with states \(\pm\sqrt{1-g}\) for a COMMON gate \(g\). Their forward-state sum is zero even when \(g\) is private. The prescribed inverse-lift input is held frozen when taking credit derivatives. The donor pair balances and common final endpoint remain intact.

Two distinct variants:

- **Private captures, otherwise held high.** At stage \(r\)'s capture, each Walsh-low label \(i\) has gate \(g=.995+10^{-4}y_{r,i}\); Walsh-high labels and all noncapture times use public \(g_H=1-n^{-2}\). Thus low gates are \(\le.9951<.9952=1-2b_0\), \(b_0=.0024\).
- **Private interior gates, public captures.** At each \(W-1\) interior steps \(j\) before capture, independent words \(z_{r,i,j}\in[-1,1]\) control \(g=g_H-10^{-4}(1+z_{r,i,j})/2\). The capture itself uses the prescribed PUBLIC .995/high Walsh gates. The raw number of private interior controls is \(mR(W-1)\).

These are within the frozen reference architecture, not new trainable recurrent weights. The true dense-model source root, full past energy/lift, and legal future-query transfer remain separate inherited constraints; a finite reference check is not a theorem about them.

## 2. Why private autonomous capture alone is not automatically safe

Suppose a balanced state pair \(+s,-s\) becomes autonomous immediately after a privately controlled capture. With the nonzero shared forward input \(z\) and \(a=1-1/n\), its next sum is

\[
\tanh(z+as)+\tanh(z-as)
=\frac{2\sinh(2z)}{\cosh(2z)+\cosh(2as)}.
\]

For \(z\ne0\), this depends on \(s^2\). A private change in the capture magnitude therefore creates a PRIVATE forward-state sum, generally changing the bath/front and potentially violating the required common endpoint. We **do not** transfer any public-bath lemma to that unforced variant. Our explicitly held and balanced pilot avoids this leakage.

## 3. NEW conditional author compression: even private captures may be too weak

For the capture-private/held-high variant, all locally control-affected parameter columns lie in two donor moving intervals, two survivor moving intervals, plus donor stationary banks. The support cardinality is bounded loosely by \(6m+4N\). The exact rank-two Duhamel recurrence implies that every private \(J_t,B_t\) and shared feedback row lies in the **PUBLIC fixed** right subspace

\[
E_{\rm par}=\operatorname{span}\{e_c:c\in I_{\rm exc}\}
+\operatorname{span}\{(u^\top L_t^0)^\top,(v_H^\top L_t^0)^\top:1\le t\le N\},
\quad P=\dim E_{\rm par}\le6m+6N.
\]

This counts **all** parameter directions, not just selected probes. The extra private survivor columns are explicitly paid.

Inherit Astra's still-reviewable long-window donor code: encode the last \(h\) donor control blocks and their two actual-coupled \(J\) aggregates, paying \(hm+2hP\) real coordinates with donor residual \(.073(N/\sqrt n)\rho^h\), \(\rho<.995206\).

For the last \(\ell\) survivor captures, additionally encode their **private** gate controls (\(\le\ell m\) coordinates), each capture's complete \(J\) row, and each between-capture high-gap weighted \(J\) aggregate (conservatively \((3\ell+5)P\) coordinates). Matching these codes makes all recent survivor gates, local direct forcing, and integrated coupled-feedback injections **equal**. Crucially, no stepwise \(O(\ell WP)\) vector ledger is necessary: the inter-capture transport is uniformly public \(g_H\) at every site.

For earlier survivor information, the same Walsh/Chebyshev bound applies because every privately perturbed low capture remains \(\le 1-2b_0\):

\[
F_\ell=\frac4\ell+\exp(-b_0\ell),\qquad
\nu_S\le32\frac{N\sqrt m}{n}\sqrt{F_\ell}.
\]

This holds after matching recent private controls, and uses ordinary-row dilution of **actual legal future queries**, not arbitrary spiked adjoints. With the exact bath row \(Z_N\) and Astra's front/dense estimates, a safe approximate code is

\[
q_{\rm code}\le(h+\ell)m+(2h+3\ell+8)P,
\]

with equal-code distance bounded by

\[
\nu_{\rm actual}\le
.073\,\frac N{\sqrt n}\rho^h
+32\frac{N\sqrt m}{n}\sqrt{F_\ell}
+30000\frac{N+1250}{n}+e_{\rm dense}.
\]

At \(R\to\infty,m=\Theta(n/R),N=\Theta(\sqrt{nR})\), choose fixed \(\ell\) (possibly extremely large) and \(h=O(\log R)\). Then \(q_{\rm code}=O((m+N)\log R)=o(n)\), and Borsuk–Ulam would rule out robust \(D=\Omega(n)\) **for this held-high/capture-private schedule, conditional on all inherited lemmas and a correct proof of recent segment aggregation**.

**Author-only theorem candidate, not verified.** It does not rule out privately modulated gates THROUGHOUT a window, other families, or the original overall target.

## 4. Interior-private gates evade this particular code, not the memory barrier

When \(g_{r,i,t}\) itself depends on private words at each interior step, the feedback filter coefficients between captures depend on \(i\) and private history. The prior proof's **single common weighted feedback aggregate per high gap is no longer justified**. Naively encoding \(W\) gates per recent block costs \(O(hmW)\), potentially \(\Omega(n)\) for \(m\sim n/R,W\sim R\). This is an obstruction *to that encoding*, not a positive robust-memory lower bound.

All private interior states remain pair-balanced by explicit forcing; donor trace neutrality, exact reference hidden endpoint, and basic no-wrap are retained. The coordinate-time energy scale remains \(O(mN)\) up to constants; proving the inherited absolute input norm and dense lift requires an additional audit.

## 5. Finite full-rank-two reference tests (not global query maxima)

The supplied Python implementations propagate the complete chronological \(M_N\) with full rank-two \(O_*\), its local part \(L_N\), and \(H_N=M_N-L_N\). Values below are **only the all-high one-step legal reference query**, \(\sigma=.05\), opposite private control words. Small widths do not satisfy the stronger asymptotic spacing geometry.

| Variant | n | m | R | W | Number of private controls | Found full-M score | Found H score |
|---|---:|---:|---:|---:|---:|---:|---:|
| Private capture | 16,384 | 4 | 2 | 16 | at most 8 | 1.49e-10 | 2.88e-11 |
| Private capture | 32,768 | 8 | 4 | 16 | at most 32 | 2.87e-11 | 2.32e-13 |
| Private capture | 32,768 | 8 | 4 | 64 | at most 32 | 5.28e-11 | 8.36e-13 |
| Private interior | 16,384 | 4 | 2 | 8 | 56 | 4.41e-10 | 8.50e-11 |
| Private interior | 32,768 | 8 | 4 | 16 | 480 | 7.01e-10 | 1.38e-10 |
| Private interior | 32,768 | 8 | 4 | 64 | 2,016 | 9.40e-10 | 1.54e-10 |
| Private interior | 65,536 | 16 | 8 | 16 | 1,920 | 4.17e-10 | 5.28e-11 |

Checks on the independent local implementation: maximum off-capture private gate difference exactly 0; capture gate difference .0002; endpoint difference 0; full forward/adjoint relative pairing error \(3.64e{-14}\). A geometry-admissible reference-state test at \(n=1,048,576,m=8,R=4,W=16,L=2048\) has \(N=2121,S=2133\le d/100=2621.44\). Both variants match endpoints exactly and local traces within \(2.73e{-12}\), with selected inverse-lift input magnitudes \(<.072\). **No million-width query optimization is claimed.**

The archive includes [private_survivor_variant.py](private_survivor_variant.py) (a minimal variation of Astra's original code) and [test_variants.py](test_variants.py). Standalone cross-checks and historical local raw JSON are also available in the conversation research package. The mathematical deductions do NOT rely on the observed tiny signals.

## 6. Next falsifiable obligation

**Private interior modulation** is the only newly tested variant here not covered by the candidate compact recent-capture code. Test distinct control-direction readout under multiple optimized legal future queries, rather than counting raw inputs or local Jacobian rank; then prove a uniform approximate code or a genuine jointly robust section. Independently audit the new capture-private code and existing Astra premises first.

**Verdict: PARTIAL. No global breakthrough. CURRENT_THEORY.md unchanged.**
