# Segment-atom width bound (Theorem B): author derivation

Author: Claude Opus 5.5 (Claude lane). Date: 2026-10-07. **Repository status: PENDING REVIEW.**

This is an author derivation, not an independently reviewed result. No experiment is used as proof. Nothing here changes the status of any other folder, and `CURRENT_THEORY.md` is not modified.

## 0. Provenance and labelling

Theorem B was first stated, with a three-step proof, in Claude's 2026-10-07 session answer to the "logarithmic width factor" task (sections I–P of that answer). This file:

- reproduces that delivered statement and proof **verbatim** (Section 2);
- records the supporting derivation steps from the same session's working analysis (Sections 3–8).

Each supporting step carries one of these labels:

- **[DELIVERED]** — printed in the original session answer.
- **[SESSION WORKING]** — derived in the same session's working analysis, but not printed in the delivered answer.
- **[ARCHIVE CLARIFICATION]** — bookkeeping written for this archive: indexing, edge cases, explicit constants. These steps add no new mathematical idea.
- **[GAP]** — unresolved. It must be closed by the reviewer or by a later proof.

No missing argument has been reconstructed and presented as original. Where the session relied on an external theorem (Carl–Pajor), the theorem is cited and recalled, not proved.

## 1. Setting and notation (inherited)

Model, probes and constants are those of `../codex_frontier_invention_20261006/PROOF.md` §§2–3, 6 and `../codex_linear_dimension_frontier_20261006/PROOF.md` §§3–9:

- frozen dense tanh corridor;
- fixed source feature;
- reference sensitivity $M_t=G_t(aO_*M_{t-1}+I)$, $M_0=0$;
- $O_*=C+\mathbf 1_ru^T+e_1v_H^T$.

Further notation:

- $V=[v_1,\dots,v_K]$ is the chosen orthonormal stationary probe bank, and $X_t=M_tV$.
- $J_t=u^TX_t\in\mathbb R^{1\times K}$.
- $h_S=2m$ is the number of survivor sites.
- A robust section of dimension $D$ is a continuous family of legal histories $H(\theta)$, $\theta\in S^{D-1}$, with a common endpoint and actual pair distance $\nu_{\rm actual}(H(\theta),H(-\theta))>.002$ for every $\theta$ (the $\epsilon=.001$ contract of `../robust_width_scaling_20261001/THEORY.md`).

Antipodal differences are written

$$
\Delta X_t(\theta)=X_t(H(\theta))-X_t(H(-\theta)),\qquad
y_t(\theta)=\sqrt{h_S}\,\Delta J_t(\theta)\in\mathbb R^{K},\qquad
\Lambda=\sup_\theta\sum_{t}\sum_{j=1}^K|y_{tj}(\theta)|.
$$

$B$ denotes the protected reader of the supplied query-normalization checkpoint. It acts on rows; its row space is the protected survivor suffix space of dimension $d\le R$. The **chosen part** of a pair is

$$
X(\theta):=B\,\Delta X_N(\theta)=B\,\Delta Y_{\rm full}(\theta)\,V .
$$

The **nuisance code** $\mathcal C$ has dimension $q=q_{\rm total}=q_{\rm stat}+q_{\rm cyc}$. It consists of:

- the exact stationary-complement code;
- the moving-cycle Fourier-plus-edge code of `../codex_moving_cycle_parameter_exhaustion_20261007/PROOF.md`.

**Scope** — the "one-step-capture scope" used throughout:

- fixed source and no-wrap geometry;
- survivor gates public;
- every survivor site at gate $g_H$ at every step, except $R$ one-step balanced captures (gates $\bar g\pm b$ by a Walsh label) and the final common reset (gate $q_N$ on every site);
- donor gates legal and at most $g_H$.

## 2. Delivered statement and proof [DELIVERED, verbatim]

> These are my own derivations here, not independently reviewed. They rely on Stage 1, the two checkpoints, and the published Carl–Pajor theorem (Invent. Math. 94, 1988). Its absolute constant C_CP is not explicit.
>
> **Theorem B (segment-atom width bound).** Assume:
> - a continuous nuisance code of dimension q such that equal codes force chosen part ≥ s on every robust pair;
> - `X = Σ_t λ_t·ũ_σ(t)·y_tᵀ` with S segments, |λ_t| ≤ 1, ‖ũ‖ ≤ c_B;
> - `Σ_{t,j}|y_tj| ≤ Λ`.
>
> Then
>
> `D ≤ q + 1 + C_CP²·c_B²·(Λ/s)²·[1 + log(SK/(D−q−1))]`
>
> *Proof.*
> 1. The segment coefficients `Z_{σj} = Σ_{t∈σ} λ_t·y_tj` are odd and continuous, with ‖Z‖₁ ≤ Λ, and X = u(Z) where `u: ℓ₁^{SK} → ℓ₂` has column norms ≤ c_B.
> 2. Carl–Pajor gives a codimension-k subspace E with `‖u|_E‖ ≤ C_CP·c_B·√((1 + log(SK/k))/k)`.
> 3. Apply Borsuk–Ulam to `θ ↦ (code(θ) − code(−θ), A·Z(θ)) ∈ ℝ^{q+k}`, where ker A = E. ∎

The same answer stated the segment structure as follows (verbatim, section J item 4):

> **Exact piecewise-parallel filters.** Between one-step captures, survivors are uniform. The survivor common mode is then an exact scalar filter of J, so `β_t = λ_t·ũ_σ(t)` with |λ_t| ≤ 1 and one fixed vector per segment σ. With R captures and R+1 gaps there are S ≤ 2R+2 segments, so only S·K atoms instead of TK. Time-multiplexing inside a segment cannot create new atoms.

## 3. Lemma 1 — open-loop survivor representation [SESSION WORKING]

**Lemma 1.** In the one-step-capture scope, the reference chosen part satisfies exactly

$$
X(\theta)=\sum_{t=0}^{N-1}\beta_t\,y_t(\theta)^T,\qquad
\beta_t:=B\,\Phi_S(N,t+1)\,aG_S(t+1)\,\frac{\mathbf 1_S}{\sqrt{h_S}},
\qquad \|\beta_t\|_2\le\|B\|_{\rm op}.
$$

Here:

- $G_S(r)$ is the diagonal survivor gate block at time $r$;
- $C_S$ is the action of $C$ on survivor sites: moving survivor sites are shifted co-movingly, and stationary survivor compensators are fixed;
- $\Phi_S(N,r)=\prod_{r'=r+1}^{N}aG_S(r')C_S$, with $\Phi_S(N,N)=I$.

*Proof.*

1. **Survivor rows of $O_*X$.** For a survivor site $i$, $(O_*X)_i=X_{\pi(i)}+u^TX$:
   - $\pi(i)$ is the co-moving predecessor for a moving site, and $i$ itself for a stationary compensator;
   - no survivor site is row 1, so the $e_1v_H^T$ term never acts;
   - by no-wrap, survivor sites never reach row $d-1$, so their $u$-coefficient is $-c$ like every other ordinary row. Hence $u^TX=J$ enters with coefficient 1.
2. **Forcing cancels.** The probe forcing on survivor rows, $G_S(t)V_S$, is identical in both histories, because survivor gates are public. It cancels in the difference, leaving

   $$
   \Delta X_S(t)=aG_S(t)\big[C_S\Delta X_S(t-1)+\mathbf 1_S\Delta J_{t-1}\big],\qquad \Delta X_S(0)=0 .
   $$

3. **Unroll.** Iterating gives $\Delta X_S(N)=\sum_t\Phi_S(N,t+1)aG_S(t+1)\mathbf 1_S\Delta J_t$, and $\mathbf 1_S\Delta J_t=(\mathbf 1_S/\sqrt{h_S})\,y_t$.
4. **Survivor rows only.** $B$ reads survivor rows only (see [GAP G2]), so $X=B\,\Delta X_S(N)$.
5. **Norm bound.** $\|aG_S C_S\|\le1$, since $C_S$ is an isometry of the co-moving survivor coordinates and gates are at most 1. Also $\|\mathbf 1_S/\sqrt{h_S}\|=1$. Hence $\|\beta_t\|\le\|B\|_{\rm op}$. ∎

The representation is open-loop in $J$. The closed-loop feedback (survivor mean $\to$ $S_w$ $\to$ $J$) is entirely contained in the realized trajectory $y_t$, so $\beta_t$ is public and history-independent.

## 4. Lemma 2 — piecewise-parallel survivor readouts [SESSION WORKING; indexing is ARCHIVE CLARIFICATION]

Let $c_1<\dots<c_R$ be the capture times. Then:

- $C_S\mathbf 1_S=\mathbf 1_S$ (the co-moving survivor indicator is preserved);
- $G_S(r)\mathbf 1_S=g_H\mathbf 1_S$ at every ordinary time $r$;
- $G_S(N)\mathbf 1_S=q_N\mathbf 1_S$ at the reset.

**Lemma 2.** Partition the injection times $t\in\{0,\dots,N-1\}$, according to $r=t+1$, into:

- the $R$ capture steps $\{c_e-1\}$;
- the $R+1$ maximal intervals of non-capture injection times. The last interval includes the reset injection $t=N-1$.

Every capture step and every interval is a segment $\sigma$, so the number of segments satisfies

$$
S\le 2R+1\le 2R+2 .
$$

Inside each segment, $\beta_t=\lambda_t\,\tilde u_\sigma$ with $0<\lambda_t\le1$ and $\|\tilde u_\sigma\|\le c_B:=\max_t\|\beta_t\|\le\|B\|_{\rm op}$.

*Proof.*

1. **Interval ending at a capture.** Let the interval end at injection time $t_\sigma=c_e-2$, i.e. the last ordinary injection before capture $e$. For $t$ in the interval,

   $$
   \Phi_S(N,t+1)aG_S(t+1)\mathbf 1_S=(ag_H)^{c_e-1-t}\,\Phi_S(N,c_e-1)\mathbf 1_S ,
   $$

   because every factor between $t+1$ and $c_e-1$ maps $\mathbf 1_S$ to $ag_H\mathbf 1_S$. Take $\tilde u_\sigma=B\,\Phi_S(N,c_e-1)\mathbf 1_S\,ag_H/\sqrt{h_S}$ and $\lambda_t=(ag_H)^{c_e-2-t}\in(0,1]$.
2. **Last interval (after the last capture, including the reset).** Every factor multiplies $\mathbf 1_S$ by $ag_H$ or $aq_N$, so $\beta_t$ is a positive multiple of $B\mathbf 1_S/\sqrt{h_S}$. Normalise by the largest multiple in the interval.
3. **Capture step.** A capture step contributes a single injection time, with direction $aG_S(c_e)\mathbf 1_S=a(\bar g\mathbf 1_S+b\chi_e)$. It is its own segment, with $\lambda=1$.
4. **No other atoms.** No other survivor-gate event exists in scope. In particular, no survivor-dependent mask lasts longer than one step. ∎

Two remarks:

- If $B$ reads only the zero-sum (protected) part, segments after the last capture have $\tilde u_\sigma=0$. That is harmless.
- Time-multiplexing within a segment changes only the scalars $\lambda_t$, never the direction. That is the precise sense in which within-segment temporal structure cannot create new atoms.

## 5. Atom reduction $TK\to SK$ [SESSION WORKING]

Define the segment coefficients

$$
Z_{\sigma j}(\theta):=\sum_{t\in\sigma}\lambda_t\,y_{tj}(\theta),\qquad
u:\mathbb R^{S\times K}\to\mathbb R^{d\times K},\quad u(e_{\sigma}e_j^T)=\tilde u_\sigma e_j^T .
$$

By Lemmas 1–2, $X(\theta)=u(Z(\theta))$ exactly. Moreover:

- $\|Z(\theta)\|_{\ell_1}\le\sum_{t,j}|y_{tj}(\theta)|\le\Lambda$, using $|\lambda_t|\le1$.
- $Z$ is continuous in $\theta$, because histories are continuous and $Z$ is linear in $\Delta X$.
- $Z$ is odd, because $\Delta X(-\theta)=-\Delta X(\theta)$.
- As an operator $u:\ell_1^{SK}\to\ell_2^{dK}$ (Frobenius norm), $\|u\|_{1\to2}=\max_\sigma\|\tilde u_\sigma\|\le c_B$.

The old entrywise width lemma used $2TK$ atoms $\pm\beta_te_j^T$. Here the same set is contained in $\Lambda\cdot u(B_1^{SK})$, with $SK\le(2R+2)K$ atoms.

## 6. Carl–Pajor Gelfand-number input [DELIVERED citation; exact statement is GAP G1]

**Gelfand numbers** (domain-side convention, as recalled): for $u:\ell_1^N\to H$ with $H$ a Hilbert space,

$$
c_k(u)=\inf\{\|u|_E\|_{1\to2}: E\subset\mathbb R^N\ \text{linear},\ \operatorname{codim}E<k\}.
$$

**Carl–Pajor theorem**, as recalled and used in the session (B. Carl and A. Pajor, *Gelfand numbers of operators with values in a Hilbert space*, Invent. Math. 94 (1988) 479–504). There is an absolute constant $C_{\rm CP}$ such that for all $N$, all Hilbert spaces $H$, all $u:\ell_1^N\to H$ and all $1\le k\le N$:

$$
c_k(u)\le C_{\rm CP}\,\|u\|_{1\to2}\sqrt{\frac{1+\log(N/k)}{k}} .
$$

The atoms $u(e_i)$ need not be orthogonal; this is what makes the theorem applicable to the nested or non-orthonormal readouts $\tilde u_\sigma$.

**Applied with $N=SK$** [ARCHIVE CLARIFICATION on indexing]: for each $1\le k<SK$ there is a subspace $E_k\subset\mathbb R^{SK}$ with $\operatorname{codim}E_k\le k$ and

$$
\sup\{\|u Z\|_F:\ Z\in E_k,\ \|Z\|_1\le1\}\le C_{\rm CP}c_B\sqrt{\frac{1+\log(SK/k)}{k}} .
$$

This follows from $c_{k+1}(u)$ and $(1+\log(N/(k+1)))/(k+1)\le(1+\log(N/k))/k$.

**Why this replaces the old logarithm** [DELIVERED]: Gordon's mean-width escape bound pays $\log(\#\text{atoms})$, while the Gelfand-number bound pays $\log(\#\text{atoms}/k)$. Both ingredients are needed:

| Atoms | Width tool | Resulting log factor |
|---|---|---|
| $TK$ | Carl–Pajor | $\log(T/R)\asymp\tfrac12\log n$ |
| $SK$ | Gordon | $\log((2R+2)K)\asymp\log n$ |
| $SK$ | Carl–Pajor | $\log((2R+2)K/k)$ |

## 7. Nuisance code and Borsuk–Ulam kernel argument [DELIVERED step 3; details SESSION WORKING; edge cases ARCHIVE CLARIFICATION]

**Hypothesis (B1) — robust separation after equal codes.** If $\mathcal C(H(\theta))=\mathcal C(H(-\theta))$, then $\|X(\theta)\|_F\ge s$.

In the corridor this is derived as follows [SESSION WORKING]:

1. A robust pair has $\nu_{\rm actual}>.002$.
2. The supplied normalization $\nu_{\rm actual}\le7.213(\sqrt m/n)\|B\Delta Y_{\rm full}\|_F+\eta$ with $\eta<.001$ gives $\|B\Delta Y_{\rm full}\|_F>(.001/7.213)\,n/\sqrt m=1.3864\cdot10^{-4}n/\sqrt m$.
3. Equal codes make the stationary complement contribution exactly zero, and the moving-cycle contribution at most $\tau=10^{-4}n/\sqrt m$ (dense pair error included).
4. The parameter-column split $V\oplus V_\perp$ is orthogonal, so Frobenius norms add (Pythagoras). Hence

$$
\|X(\theta)\|_F\ge\sqrt{1.3864^2-1}\cdot10^{-4}\frac n{\sqrt m}\ge s:=9.5\cdot10^{-5}\frac n{\sqrt m}.
$$

**Argument.** Let $k:=D-q-1$. If $k\le0$ there is nothing to prove.

*Case $1\le k<SK$.*

1. Choose a linear $A:\mathbb R^{SK}\to\mathbb R^k$ with $\ker A\supseteq E_k$.
2. Define

   $$
   \Phi(\theta)=\big(\mathcal C(H(\theta))-\mathcal C(H(-\theta)),\ A\,Z(\theta)\big)\in\mathbb R^{q+k}=\mathbb R^{D-1}.
   $$

   $\Phi$ is continuous and odd.
3. By Borsuk–Ulam there is $\theta^*$ with $\Phi(\theta^*)=0$.
4. At $\theta^*$ the codes agree, so (B1) gives $\|X(\theta^*)\|_F\ge s$.
5. Also $Z(\theta^*)\in E_k$ and $\|Z(\theta^*)\|_1\le\Lambda$, so

   $$
   s\le\|u Z(\theta^*)\|_F\le\Lambda\,C_{\rm CP}c_B\sqrt{\frac{1+\log(SK/k)}{k}} .
   $$

6. Rearranging:

$$
\boxed{\,D\le q+1+C_{\rm CP}^2c_B^2\Big(\frac{\Lambda}{s}\Big)^2\Big[1+\log\frac{SK}{D-q-1}\Big]\,}
$$

*Case $k\ge SK$.* Take $A$ injective. Then $Z(\theta^*)=0$, so $X(\theta^*)=0<s$, a contradiction. Hence $D\le q+SK$ always.

No linearity in $\theta$, and no oddness of the section itself, is used. Only oddness of the antipodal-difference map matters.

## 8. Constants and dimensional restrictions [ARCHIVE CLARIFICATION, values from session]

| Quantity | Value or definition | Source |
|---|---|---|
| $S$ | $\le 2R+2$ (actually $\le 2R+1$) | Lemma 2 |
| Number of atoms | $SK\le(2R+2)K$ | §5 |
| $c_B$ | $\max_\sigma\|\tilde u_\sigma\|\le\|B\|_{\rm op}$; $=1$ for an orthonormal protected read | Lemma 1 |
| $C_{\rm CP}$ | absolute, **not computed** | [GAP G1] |
| $s$ | $\ge9.5\cdot10^{-5}\,n/\sqrt m$ | §7 (B1) |
| $q$ | $q_{\rm total}=R(2^R+1)+q_{\rm cyc}=o(K)$ at Route-6 scaling | upstream |
| $\Lambda$ | **input, not proved here** | §9 |

Two equivalent forms with explicit $\Lambda$:

- With $\Lambda\le\Lambda_0\sqrt K\,N$: $(\Lambda/s)^2\le(\Lambda_0/9.5\cdot10^{-5})^2\,K N^2 m/n^2$.
  - $\Lambda_0=1.84$ (Lemma M, weak captures) gives $3.75\cdot10^8$. **[DELIVERED]**
  - $\Lambda_0=4$ (twice Astra's per-history $2\sqrt K N$) gives $1.77\cdot10^9$.

## 9. Sources of $\Lambda$ and consequences for separated Route 6

### 9.1 Mass inputs

- **Lemma M** (Claude, same session, unreviewed). For low-donor one-step captures with distinct Walsh characters and capture half-contrast $b_e\le7\cdot10^{-4}$: $\Lambda\le1.84\sqrt K\,N$ for antipodal differences. The delivered statement and sketch are preserved in Appendix A.
- **Astra** (`../astra_separated_strong_capture_20261007/`, PENDING REVIEW). For strong captures with gaps of at least $\lceil100/p\rceil$ ordinary steps: $\Lambda\le2\sqrt K\,N$ per history, hence $\le4\sqrt K\,N$ for antipodal differences.
  - In-session review by Claude (not archived): the bound follows in scope. Astra's (21) is mis-stated: it mixes canonical and packet quantities. It must be run on the packet potential $\Phi=\sum_pE_{\rm core}(x_p)$ with packet output; all constants survive that repair.

### 9.2 Corollary (separated one-step-capture family) [SESSION WORKING; constant updated for Astra's $\Lambda$]

**Scope.** All of:

- the one-step-capture scope of §1;
- publicly segmented, group-shared donor gates;
- donors low at every capture;
- distinct Walsh capture characters;
- zero-initial probe responses;
- consecutive captures at least $\lceil100/p\rceil$ ordinary steps apart, where $p=w_S$;
- inherited bath and front premises.

**Assumes.** All of:

- (i) moving-cycle exhaustion from `../codex_moving_cycle_parameter_exhaustion_20261007/`;
- (ii) both upstream checkpoints in their original form (7.213 with $\eta<.001$, and $q_{\rm stat}\le R(2^R+1)$; see `../gemini_checkpoint_recovery_audit_20261007/`, where Claude's session audit supports the original forms but not Gemini's $C\le.048$);
- (iii) Astra's $\Lambda$ bound;
- (iv) Theorem B;
- (v) Carl–Pajor.

**Bound.**

$$
D\le q_{\rm total}+1+1.77\cdot10^9\,C_{\rm CP}^2c_B^2\,\frac{KN^2m}{n^2}\Big[1+\log\frac{(2R+2)K}{D-q_{\rm total}-1}\Big].
$$

**Route-6 scaling:** $R\asymp\log\log n$, $K\asymp m\asymp n/R$, $N\asymp C_T\sqrt{nR}$ with fixed $C_T$.

1. **The width term.** $KN^2m/n^2\asymp C_T^2K$.
2. **The log factor.** Put $k=D-q-1=xK$. Then $x\le A'(1+\log((2R+2)/x))$ with $A'=1.77\cdot10^9C_{\rm CP}^2c_B^2C_T^2$, so $x\le\max\{1,\ A'(1+\log(2R+2))\}$.
3. **Conclusion.**

$$
D=o(K)+O\!\big(C_T^2\,(n/R)\log R\big)=o(n).
$$

**Linear-dimension check.** If $D\ge cn$ with $K=\kappa n/R$, then $x\ge cR/(2\kappa)$, so the log factor is $O(1)$. This forces $R\le(2\kappa/c)A'(1+\log(8\kappa/c))=O(C_T^2)$. Linear dimension in this family therefore needs $C_T\gtrsim\sqrt R$, i.e. $mT\gtrsim n^{3/2}$, which loses the strict budget.

**Spacing compatibility.** $100/p\approx25R$ ordinary steps. Natural Route-6 capture spacing is about $C_T\sqrt{n/R}\gg25R$.

### 9.3 What this does NOT establish

- **Not a Route-6 impossibility theorem in general.** It covers only the stated scope, and is conditional on (i)–(v).
- **Not covered:**
  - captures closer than about $5/p$ steps (between $5/p$ and $100/p$ is untreated by both mass sources);
  - donors high at capture;
  - long survivor masks and filter banks;
  - repeated capture characters;
  - multi-channel (redesigned) feedback;
  - full parameter or source families;
  - growing $C_T$;
  - over-provisioned families with $RK\gg n$, which keep a $\sqrt{\log(RK/n)}\le\sqrt{\log\log n}$ window: $D\ge cn$ then forces only $mT\gtrsim n^{3/2}/\sqrt{\log(RK/n)}$.
- **Constants are astronomically large.** The statement is asymptotic only.

## 10. Sharpness [DELIVERED]

- **$\log T$ is provably unnecessary in scope**, because the filters are exactly piecewise parallel. Saturating the old $\log(2TK)$ needs $\beta_t$ to rotate within a segment, which only long masks or filter banks can do.
- **Garnaev–Gluskin lower bound.** For orthonormal atoms, no Gelfand-width (linear-kernel) argument beats $\log(1+SK/k)$.
- **Open.** Whether a legal section attains $D\asymp(\Lambda/s)^2\log(SK/D)$, and whether a genus or topological argument can remove $\log(1+SK/k)$.

## 11. Unresolved gaps and obligations

- **G1 — Carl–Pajor statement.** Exact statement, Gelfand-number indexing convention, and the value or existence of an explicit $C_{\rm CP}$. The session recalled the theorem; this archive does not reprove or quote it from the paper. A reviewer must check the cited source, or substitute a self-contained proof such as a Gaussian-matrix proof with explicit constants.
- **G2 — Support of $B$.** Lemma 1 requires the checkpoint reader $B$ to act only on survivor rows (or only on the protected suffix space), and to be the same $B$ for which the separation $s$ is derived. The checkpoint's $\sqrt m$ coefficient is consistent with survivor support, but the checkpoint text does not define $B$ explicitly.
- **G3 — Uniform survivors.** Lemma 2 needs survivor gates exactly uniform at every non-capture step, including trace-correction, clear and reset steps. Any survivor-dependent multi-step mask breaks piecewise parallelism.
- **G4 — Probe forcing cancellation.** This relies on identical, public survivor gates in both histories. That holds in scope; outside scope it must be rechecked.
- **G5 — Dense model.** The representation is for the reference model. The actual dense model enters only through the checkpoint's $\eta$. A reviewer should confirm that $s$ was derived with the same reference/actual convention.
- **G6 — $\Lambda$ is an input.** Lemma M is unreviewed; Astra's bound is pending review and needs the packet-ledger repair of its (21). Close captures are unproved.
- **G7 — Scope inheritance.** The corollary inherits every scope restriction of the moving-cycle exhaustion (public segmentation, low donors at capture, $P=O(R)$, no-wrap, sufficiently large $n$).
- **G8 — Constants.** The overall constant is non-explicit because of $C_{\rm CP}$. No finite-$n$ claim is made.

## Appendix A — Lemma M (delivered statement and sketch, verbatim; PENDING REVIEW)

> **Lemma M (signal budget with no R loss, for weak captures).** Scope:
> - one-step balanced captures with distinct Walsh characters and donors low at capture;
> - capture half-contrast `b_e ≤ 7·10⁻⁴`;
> - survivors at g_H otherwise; arbitrary legal donor words; inherited bath and front premises.
>
> Then for every history and every chosen column j:
>
> `Σ_t |√h_S·uᵀX_t v_j| ≤ .92·(1 + o(1))·N/√K`, so `Λ ≤ 1.84·√K·N`.
>
> *Proof sketch, every step checked.*
> 1. **Duality.** The mass equals the supremum over sign sequences σ ∈ [−1,1]^N of `Σ_s ⟨p_s^σ, G_s v_j⟩`, where p^σ is the costate with forcing σ_t·u.
> 2. **Common forcing hits only the hub.** The forcing is common to all groups, including the bath aggregate, because the bath-row coefficients of u sum to exactly −w_B. In (U, r) coordinates it therefore lands on the hub alone.
> 3. **No survivor term at captures.** With distinct characters, ν = 0 at every capture.
> 4. **Every step is nonnegative.** This needs b ≤ g_H·β_min ≈ 7.2·10⁻⁴ and ḡ ≥ q_max. Every step matrix then has hub row sum ≤ 1 − w_S.
> 5. **Killed-chain count.** The chain is killed with probability ≥ w_S at each hub visit, so expected hub visits ≤ 1/w_S. This holds for time-varying steps too, giving |U|, |r_j| ≤ (1 + o(1))/w_S.
> 6. **Pairing.** `⟨p, G w_j'⟩ = c·√(m/K)·[g_j'·Λ_j' − ḡ_S·U]`, and probe mixing satisfies Σ|H| ≤ 1.293.
> 7. **Lower-order terms.** Front, terminal and bath-leaf corrections are of relative size O(10¹⁰/m) and O(1/√n).

The constant 1.84 is for antipodal differences: twice the per-history .92.

## Appendix B — Origin of the old $\log(2TK)$ [DELIVERED, condensed]

The previous entrywise width estimate (Claude session, never in the repository) set $M=\Lambda\cdot{\rm absconv}\{\pm\beta_te_j^T\}$. It then bounded the Gaussian mean width by an expected maximum of $2TK$ Gaussians,

$$
w(M)=\Lambda\,\mathbb E\max_{t,j}|\langle g_j,\beta_t\rangle|\le\Lambda b\sqrt{2\log(2TK)},
$$

and applied Gordon's escape bound $d^k(M)\le2w(M)/\sqrt k$ with Borsuk–Ulam at $k=D-1$. The result was $D\le1+8(\Lambda b/s)^2\log(2TK)$.

Theorem B removes both losses in that chain:

- the atom over-count ($2TK$ atoms vs $SK$);
- Gordon's $\log N$ vs Carl–Pajor's $\log(N/k)$.
