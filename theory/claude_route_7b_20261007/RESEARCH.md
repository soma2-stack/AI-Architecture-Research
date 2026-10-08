# Route 7B: inventions, a log-free width theorem, and why each candidate fails or stalls

Author: Claude Opus 5.5 (Claude lane). Date: 2026-10-07. **Repository status: PENDING REVIEW.**
Author-local labels such as PROVED below are **not** repository VERIFIED status. No experiment is used as proof; the scripts in this folder are falsification probes only. `CURRENT_THEORY.md` is not modified. Route 7A (precharge-and-burst, Astra) is not studied here.

## 0. Summary

**Target.** A legal construction in the frozen fixed-source corridor with $D=\Omega(n)$ and $mT=o(n^{3/2})$.

**Outcome.** Route 7B does **not** reach the target. Its main results:

1. **PROVED (author-local) — log-free topological width theorem.** Every odd continuous map from a $\mathbb Z_2$-space of index $k$ into $\mathbb R^N\setminus0$ has a point with $\|x\|_1^2\ge(k+1)\|x\|_2^2$ (Lemma F; nerve / Ky Fan type argument). Consequences:
   - The coindex of $\{\|x\|_1\le1,\ \|x\|_2\ge r\}$ is exactly $\lfloor1/r^2\rfloor$. There is **no logarithm and no dependence on $N$** — this settles the "genus versus Gelfand" question left open earlier in this session.
   - **Theorem F:** $D\le q+\lfloor(\|U\|_{2\to2}\Lambda/s)^2\rfloor$ for any readout $X=UZ$ with $\ell_1$-bounded odd coefficients $Z$.
   - **Theorem B-F:** for the one-step-capture family with distinct Walsh characters, $\|U_{\rm prot}\|_{2\to2}\le2$ (Lemma U; numerically $\le1$). This gives $D-q\le4(\Lambda/s)^2$, with no $C_{\rm CP}$ and no $\log$. It sharpens the archived Theorem B in [`../opus_segment_atom_width_20261007/`](../opus_segment_atom_width_20261007/).
2. **PROVED (author-local) — Lemma TV (survivor-filter rigidity).** For **any public survivor gate schedule** (arbitrary long masks, filter banks, any number of classes), every unit protected observable reads the shared feedback signal through an effective temporal filter $f$ with $|f|\le1$ and $\mathrm{TV}(f)\le1$. Survivor-side temporal coding cannot synthesise oscillatory (Walsh-in-time) filters.
3. **Three original Route 7B mechanisms,** analysed and ranked (Section 4):

   | Rank | Mechanism | Status |
   |---|---|---|
   | 1 | Shared-signal multi-timescale accumulator bank (MTAB) | **OPEN** — not excluded by Theorem B/B-F or by Astra/Codex scopes; Lemma TV plus a conditioning heuristic point to failure; decisive lemma stated |
   | 2 | Private gate-coded captures (survivor masks as controls) | **REFUTED as a route to $o(n^{3/2})$** — exact rank-one collapse lemma plus write-yield scaling |
   | 3 | Track-sweep spatial gate field (time → space through moving-cycle parameter columns) | **Boundary only** — scaling gives $D=\Theta(n)$ at $mT=\Theta(n^{3/2})$ with $m=\Theta(\sqrt n)$; not $o$ |

4. **Strongest structural finding (interpretation, not a theorem).** Every analysed mechanism is governed by one budget, $D\lesssim\|U\|^2(\Lambda/s)^2$:
   - $\Lambda\lesssim\sqrt K\,N$ — passivity of the single feedback channel;
   - $s\asymp n/\sqrt m$ — query normalization on the $\le2m$ driven survivor rows;
   - $\|U\|$ — the readout's mass-reuse factor.

   Linear dimension below the $n^{3/2}$ budget therefore needs **mass reuse** ($\|U\|\gg1$ with a well-conditioned section), **super-passive signal** ($\Lambda\gg\sqrt KN$), or a **history-dependent readout**. Lemma TV and the collapse lemma close the cheapest forms of each inside the corridor.

**Most dangerous unresolved obstacle.** The *conditioning* of overlapping monotone survivor filters. Rotating filters escape every proved width bound only if they realise mass reuse; positive monotone filters appear too ill-conditioned to do so.

**Next falsifiable theorem.** The TV-filter width theorem (Section 6). Proving it closes MTAB, and with passivity for long masks it would essentially close the single-channel fixed-source corridor up to a $\log d$ factor. A legal counterexample would revive Route 7B.

## 1. Contract and the single-channel normal form (inherited)

Model, probes, gates, query and energy conventions are those of `../codex_frontier_invention_20261006/PROOF.md` §§2–3, 6 and `../codex_linear_dimension_frontier_20261006/PROOF.md` §§3–10:

- frozen dense tanh with $R$ of norm $a=1-1/n$;
- one fixed source feature;
- legal future queries with preactivations in $[.25,.75]$;
- common exact endpoint;
- $mT$ counts driven tuple-coordinates times steps.

Further notation:

- $X_t=M_tV$ with $M_t=G_t(aO_*M_{t-1}+I)$ and $O_*=C+\mathbf 1u^T+e_1v_H^T$.
- $J_t=u^TX_t$; $h_S=2m$ survivor sites.
- **Signal.** For an antipodal pair, $y_t:=\sqrt{h_S}\,\Delta J_t\in\mathbb R^{P}$, where $P$ is the number of parameter columns considered.
- **Mass.** $\Lambda:=\sup_\theta\sum_{t,c}|y_{tc}(\theta)|$.

**Separation (checkpoint, original form).** After the final public clear, $\nu_{\rm actual}\le7.213(\sqrt m/n)\|B\Delta Y_{\rm full}\|_F+\eta$ with $\eta<.001$. With equal nuisance codes and the moving-cycle residual $\tau=10^{-4}n/\sqrt m$, robust pairs satisfy $\|X\|_F\ge s:=9.5\cdot10^{-5}n/\sqrt m$ for the chosen-probe protected part $X=B\Delta X_N$ (derivation: `../opus_segment_atom_width_20261007/PROOF.md` §7).

**Normal form (exact; same derivation as Lemma 1 there).** Survivor gates are public; survivor sites receive feedback only through the common term $a G_S\mathbf 1_S J$. Hence

$$
X(\theta)=\sum_{t}\beta_t\,y_t(\theta)^T,\qquad \beta_t=B\,\Phi_S(N,t+1)\,aG_S(t+1)\,\mathbf 1_S/\sqrt{h_S},\qquad \|\beta_t\|\le\|B\|\le1 .
$$

Here $\Phi_S$ is the public survivor-block propagator. Survivor site $i$ applies the scalar filter

$$
\phi_i(t)=\prod_{r=t+1}^{N}a\,g_i(r)\in(0,1],
$$

which is non-decreasing in $t$, and $\beta_t$ collects these filters through $B$.

## 2. Lemma TV — survivor-filter rigidity [PROVED, author-local]

**Lemma TV.** Assume survivor gates are public (any schedule). For any unit row $\psi$ supported on survivor sites, the effective filter

$$
f_\psi(t):=\frac1{\sqrt{h_S}}\sum_{i}\psi(i)\,\phi_i(t)
$$

satisfies $|f_\psi(t)|\le1$ and $\mathrm{TV}(f_\psi)\le1$. The protected readout through $\psi$ is exactly $\sum_t f_\psi(t)\,y_t$.

*Proof.*
1. Each $\phi_i$ is monotone with values in $(0,1]$, so $\mathrm{TV}(\phi_i)\le1$ and $|\phi_i|\le1$.
2. Hence $|f_\psi|\le\|\psi\|_1/\sqrt{h_S}\le1$ and $\mathrm{TV}(f_\psi)\le\|\psi\|_1/\sqrt{h_S}\le1$, by Cauchy–Schwarz.
3. The readout identity follows from the normal form. ∎

**Consequences.**
- Splitting survivors into $C$ classes does **not** enlarge the filter class. A unit row averages the class filters, so the variation budget stays 1 regardless of $C$. Oscillatory filters such as $\pm1$ Walsh patterns in time have variation equal to their number of sign changes, and are unreachable.
- Within the single feedback channel, survivor-side temporal multiplexing reads the cumulative signal $Y(t)=\sum_{t'\le t}y_{t'}$ through probability-like measures of total mass at most 2 (summation by parts).

## 3. The log-free topological width theorem [PROVED, author-local]

### 3.1 Index facts used

For a compact free $\mathbb Z_2$-space $W$ (involution $w\mapsto-w$), put $\mathrm{ind}(W)=\min\{k:\exists\text{ odd continuous }W\to S^k\}$. Two standard facts (see J. Matoušek, *Using the Borsuk–Ulam Theorem*, Ch. 5):

- **(I1) Monotonicity.** An odd map $W\to X$ gives $\mathrm{ind}(W)\le\mathrm{ind}(X)$. A free simplicial $\mathbb Z_2$-complex of dimension $j$ has index at most $j$.
- **(I2) Zero sets.** If $c:S^{D-1}\to\mathbb R^q$ is odd and continuous and $W=c^{-1}(0)$, then $\mathrm{ind}(W)\ge D-1-q$. *Proof.* Otherwise there is an odd $g:W\to S^{D-2-q}$. Extend it to an odd $G:S^{D-1}\to\mathbb R^{D-1-q}$ (Tietze plus antisymmetrisation). Then $(c,G):S^{D-1}\to\mathbb R^{D-1}$ is odd with no zero: on $W$, $G=g\ne0$; off $W$, $c\ne0$. This contradicts Borsuk–Ulam. ∎

### 3.2 Lemma F (sparsity of odd maps)

**Lemma F.** Let $W$ be a compact free $\mathbb Z_2$-space with $\mathrm{ind}(W)\ge k$, and $Z:W\to\mathbb R^N\setminus\{0\}$ odd and continuous. Then for every $\tau\in(0,1)$ there is $w\in W$ with at least $k+1$ coordinates satisfying $|Z_i(w)|>\tau\|Z(w)\|_\infty$. Consequently

$$
\sup_{w\in W}\frac{\|Z(w)\|_1^2}{\|Z(w)\|_2^2}\ \ge\ \sup_{w\in W}\frac{\|Z(w)\|_1}{\|Z(w)\|_\infty}\ \ge\ k+1 .
$$

*Proof.*
1. **Cover.** Put $A_i^{\pm}=\{w:\pm Z_i(w)>\tau\|Z(w)\|_\infty\}$. These are open sets covering $W$ (via the maximal coordinate), with $A_i^-=-A_i^+$ by oddness, and $A_i^+\cap A_i^-=\emptyset$ because $\|Z\|_\infty>0$.
2. **Nerve map.** Take a partition of unity $\{\rho_i^\pm\}$ subordinate to this cover, symmetrised so that $\rho_i^-(w)=\rho_i^+(-w)$. Define $\Phi(w)=\sum_i(\rho_i^+(w)-\rho_i^-(w))e_i$. Because $\rho_i^+$ and $\rho_i^-$ have disjoint supports, $\Phi(w)$ lies in the face of the cross-polytope $\partial\lozenge^N$ spanned by $\{\pm e_i:w\in A_i^\pm\}$. So $\Phi$ is an odd map into $\partial\lozenge^N$.
3. **Contradiction.** If every $w$ lay in at most $k$ sets, $\Phi$ would map into the $(k-1)$-skeleton, giving $\mathrm{ind}(W)\le k-1$ by (I1). Contradiction.
4. **Ratio.** At such a $w$, $\|Z\|_1>(k+1)\tau\|Z\|_\infty$. Also $\|Z\|_2^2\le\|Z\|_1\|Z\|_\infty$. Let $\tau\to1$ and use compactness. ∎

**Corollary F1 (exact coindex of the $\ell_1$-ball minus an $\ell_2$-ball).** Let $A_r=\{x\in\mathbb R^N:\|x\|_1\le1,\ \|x\|_2\ge r\}$. The largest $D$ with an odd continuous map $S^{D-1}\to A_r$ is $\lfloor1/r^2\rfloor$, for every $N\ge\lfloor1/r^2\rfloor$.
- Upper bound: Lemma F with $W=S^{D-1}$, $k=D-1$.
- Lower bound: the coordinate sphere $x=\theta/\sqrt D$.
- Contrast: Gelfand widths of $B_1^N$ carry $\log(eN/k)$ (Garnaev–Gluskin), and Gordon's mean-width argument carries $\log N$. **The topological question has no logarithm.**

*Numerical falsification attempt.* `fan_ratio_search.py` and `fan_ratio_search_d8.py` hill-climb $\|f\|_1^2/\|f\|_2^2$ over odd "soft-argmax-over-a-net" maps designed to stay sparse. They find maxima $7.94,\ 8.24,\ 8.96$ at $D=5,6,8$, all $\ge D$. Uniform sampling (`fan_ratio_check.py`) misses these points: the extremal points sit near Voronoi vertices. This is a sanity check, not evidence for the proof.

### 3.3 Theorem F (log-free width bound)

**Theorem F.** Let $\theta\mapsto H(\theta)$, $\theta\in S^{D-1}$, be a robust section. Let $c(\theta)=\mathcal C(H(\theta))-\mathcal C(H(-\theta))\in\mathbb R^q$ be the odd difference of a continuous nuisance code. Let $Z:S^{D-1}\to\mathbb R^N$ be odd and continuous with $\sup\|Z\|_1\le\Lambda$, and $U$ a fixed linear map with $\|UZ(\theta)\|_2\ge s$ whenever $c(\theta)=0$. Then

$$
\boxed{\;D\ \le\ q+\Big\lfloor\Big(\frac{\|U\|_{2\to2}\,\Lambda}{s}\Big)^2\Big\rfloor\;}
$$

*Proof.*
1. If $D\le q$ there is nothing to prove.
2. Otherwise $W=c^{-1}(0)$ satisfies $\mathrm{ind}(W)\ge D-1-q$ by (I2), and $Z\ne0$ on $W$.
3. Lemma F gives $w\in W$ with $\|Z(w)\|_1^2\ge(D-q)\tau\|Z(w)\|_2^2$.
4. Since $s\le\|U\|\,\|Z(w)\|_2$, we get $D-q\le\|U\|^2\Lambda^2/(\tau s^2)$ for every $\tau<1$. ∎

Comparison with Theorem B (`../opus_segment_atom_width_20261007/`):
- **Theorem B** needs only atom norms ($\|u\|_{1\to2}\le c_B$) and pays $C_{\rm CP}^2(1+\log(SK/D))$.
- **Theorem F** needs the $\ell_2$ operator norm and pays nothing else. It is explicit, has no external theorem, and has no logarithm.
- The two agree whenever the coefficient basis is well conditioned.
- **Correction note.** The independent audit [`../astra_theorem_b_audit_20261007/`](../astra_theorem_b_audit_20261007/) found that Theorem B's §7 chose $\ker A\supseteq E_k$, which is the wrong direction; the repair is $\ker A=E_k$. Theorem F uses no kernel selection at all: it needs only the zero-set index (I2) and Lemma F.

### 3.4 Lemma U and Theorem B-F (one-step captures, log-free) [PROVED, author-local; numerics in `capture_opnorm_check.out`]

> **Correction note (2026-10-07, added after review; original text below preserved).**
>
> **What was wrong.** Lemma U as stated is **refuted** for linearly dependent distinct labels.
> - Step 2 fails; [`../gemini_route7b_audit_20261007/`](../gemini_route7b_audit_20261007/) found this.
> - At $ag_H=1$ (or $ag_H\to1$), $\sup_R\|U_{\rm prot}\|\ge1+\sqrt2>2$ for every legal contrast.
> - The script below tested only independent labels (`1 << e`).
>
> **Repair** in [`../claude_lemma_u_repair_20261007/`](../claude_lemma_u_repair_20261007/), author-local and PENDING REVIEW:
> - $\|U_{\rm prot}\|\le2\sqrt{1+(ag_H)^2}\le2\sqrt2$ for all distinct labels;
> - $\le\sqrt2$ for linearly independent labels;
> - Theorem B-F holds with $D-q\le8(\Lambda/s)^2$ instead of 4, and the Route-6 corollary constant becomes $1.42\cdot10^{10}$.
>
> Theorem F is unaffected.

**Setting.**
- One-step balanced captures $e=1..R$ with distinct Walsh characters, at half-contrast $b$; survivor gate $g_H$ otherwise.
- The open-loop survivor content lies in the Walsh-character space $\mathrm{span}\{\xi_I\}$.
- Capture $e$ acts as $\mathcal M_e=a(\bar g\,I+b\,F_e)$, with $F_e\xi_I=\xi_{I\oplus\{e\}}$ and $\bar g=g_H-b$.
- Segment coefficients $Z_\sigma\in\mathbb R^K$: ordinary segments $\sigma=0..R$, plus the $R$ capture-step injections, exactly as in Lemma 2 of the Theorem B archive.

**Lemma U.** The linear map $U_{\rm prot}:(Z_\sigma)_\sigma\mapsto$ (protected, i.e. non-empty-character, content) satisfies $\|U_{\rm prot}\|_{2\to2}\le2$.

*Proof.*
1. **Protected content.** It equals $\sum_e\mathcal V_e(\xi_e)\,W_e^T$, where $\mathcal V_e=\mathcal M_R\cdots\mathcal M_{e+1}$ and $W_e\in\mathbb R^K$ is the amount moved from the common mode into $\xi_e$ at capture $e$.
2. **Orthogonality.** Each $\mathcal M_{e'}$ is symmetric with eigenvalues $a(\bar g\pm b)\in[0,1]$, so it is a contraction. $\mathcal V_e(\xi_e)$ is supported on characters whose minimal element is $e$. Hence the vectors $\mathcal V_e(\xi_e)$ are mutually orthogonal with norm at most 1, and $\|\sum_e\mathcal V_e(\xi_e)W_e^T\|_F\le\|W\|_F$.
3. **Common-mode bookkeeping.** The common-mode amplitude is multiplied by $a\bar g\le1-b$ at each capture and by $(ag_H)^\Delta\le1$ between captures; ordinary injections enter it and the $\lambda_t\le1$ weights are absorbed in $Z$. So $W=T_{\rm ord}Z_{\rm ord}+T_{\rm cap}Z_{\rm cap}$, where each $T$ is lower-triangular with entries bounded by $ab(a\bar g)^{e-\sigma}$.
4. **Young's inequality.** Each $T$ has $\ell_2$ norm at most $ab\sum_{k\ge0}(a\bar g)^k\le b/(1-\bar g)\le1$, because $1-\bar g\ge b$. Summing the two parts gives $\|U_{\rm prot}\|\le2$. ∎

Exact finite-$R$ computation (`capture_opnorm_check.py`) gives:

| $b$ | $\|U_{\rm prot}\|_{\rm op}$ over $R\le10$ |
|---|---|
| .0025 | $\le.0233$ |
| .05 | $\le.348$ |
| .2 | $\le.672$ |
| .4 | $\le.822$ |

So the true constant appears to be $\le1$, and much smaller for small $b$ (roughly $\approx bR$ when $bR\ll1$).

**Theorem B-F.** In the one-step-capture scope of the Theorem B archive (survivors uniform at $g_H$ except one-step balanced captures with distinct characters; the reader $B$ reads only protected rows):

$$
D-q\ \le\ \|U_{\rm prot}\|^2\Big(\frac{\Lambda}{s}\Big)^2\ \le\ 4\Big(\frac{\Lambda}{s}\Big)^2 .
$$

*Proof.* Apply Theorem F with $Z$ the segment coefficients ($\|Z\|_1\le\Lambda$, odd, continuous) and Lemma U. ∎

**Route-6 corollary, log-free and $C_{\rm CP}$-free.** For separated low-donor captures, take Astra's $\Lambda\le4\sqrt KN$ for antipodal differences ([`../astra_separated_strong_capture_20261007/`](../astra_separated_strong_capture_20261007/); pending review; packet-ledger repair of its (21)) and $s=9.5\cdot10^{-5}n/\sqrt m$:

$$
D-q\le7.1\cdot10^{9}\,\frac{KN^2m}{n^2}\qquad\big(\le1.8\cdot10^9\,KN^2m/n^2\ \text{if}\ \|U_{\rm prot}\|\le1\big).
$$

At $R\asymp\log\log n$, $K\asymp m\asymp n/R$, $N=C_T\sqrt{nR}$, this is $O(C_T^2n/R)=o(n)$ for every fixed $C_T$. Linear $D$ forces $C_T\gtrsim\sqrt R$, i.e. $mT\gtrsim n^{3/2}$. The $\log R$ in the archived corollary is removed.

## 4. Three Route 7B mechanisms

**Budget principle (interpretation).** By Theorem F, any mechanism whose protected readout is $X=UZ$, with $Z$ odd and of $\ell_1$ mass $\Lambda$, satisfies $D\lesssim\|U\|^2(\Lambda/s)^2$. In the corridor:

- $s\asymp n/\sqrt m$;
- passivity gives $\Lambda\lesssim\sqrt KN$ (Lemma M for weak captures; Astra for separated captures);
- so $(\Lambda/s)^2\asymp mKN^2/n^2\le(mN/n)^2$.

$D=\Omega(n)$ with $mT=o(n^{3/2})$ therefore requires one of:

- **(E1) mass reuse:** $\|U\|^2\to\infty$, with a section that actually realises it;
- **(E2) super-passive signal:** $\Lambda\gg\sqrt KN$;
- **(E3) a history-dependent readout,** so that $U$ is not fixed.

Each mechanism below targets one of these.

### 4.1 Rank 1 — Shared-signal multi-timescale accumulator bank (MTAB) — targets (E1) — **OPEN**

**Construction.**
- **Lift and budget.** The inherited four-site lift, fixed source, probe bank $V$ (K donor groups), bath, and global front chronology. There are $m$ tuples, $m/2$ donor and $m/2$ survivor.
- **Survivor classes.** Survivor tuples are split into $C=2^{r}$ equal **public classes**. All four sites of a tuple share the class.
- **Write interval $[1,T_w]$, donors.** Donor group $j$ uses a **private continuous gate word** $g_j(t)\in[g_L,g_H]$, with no segment restriction.
- **Write interval, survivors.** Survivor class $c$ uses a **public profile** $g_c(t)\in[g_L,g_H]$, chosen as multi-timescale accumulators. Two examples:
  - constant near-critical rates $1-g_c\in\{n^{-2}\}\cup\{8^{\ell}/T_w\}$;
  - staggered starts: low before $t_c$, high after.
- **After the write.** All survivors go to $g_H$. Donors use $L_d-1$ low steps and then the inherited exact trace correction (eq. (9) of the frontier). Then the public clear and the common reset.
- **Survivor traces are public**, because survivor gates are public, so no survivor correction is needed.
- **Captures are not needed.** Zero-sum class combinations already differ, because the class filters differ.

**Exact recurrence.** This is (6) of the frontier with the survivor group split into classes of weight $w_c=p/C$:

$$
z_c'=g_c\big[a(z_c-S)+f_S+a\rho\big],\qquad S=\sum_g w_gz_g .
$$

Open-loop survivor content of a site in class $c$:

$$
x_c=\frac1{\sqrt{h_S}}\sum_t\phi_c(t)\,y_t,\qquad \phi_c(t)=\prod_{r>t}a\,g_c(r).
$$

**Dimension mechanism.**
- **Protected rows.** $\psi_v$ = zero-sum class combinations ($v\in\mathbb R^C$, $\sum_cv_c=0$, $d=C-1$). They are protected after the write, because survivors are uniform from then on.
- **Readout.** $Y_v^{(j)}=\sum_tf_v(t)\,y^{(j)}_t$, with $f_v=\frac1C\sum_cv_c\phi_c$ (Lemma TV: $|f_v|\le1$, $\mathrm{TV}(f_v)\le1$).
- **Target.** $D\approx d_{\rm eff}K$, where $d_{\rm eff}$ is the number of filters that are robustly independent on the donor-generated signal space.
- **Mass reuse.** All $d$ filters read the **same** feedback mass, which is how MTAB could beat $\|U\|\approx1$.

**Cost.** $T=T_w+L_d+L_{\rm clear}+2$, so $mT\approx mT_w+O(m\,(n/m)\log n)$. There are no sequential writes: every timescale shares the single interval $T_w$.

**Retention and interference.**
- After the write, protected content is multiplied by $(ag_H)^{N-T_w}\ge.999$.
- Interference between channels is exactly the conditioning of $\{f_v\}$ on the signal subspace.

**Separation.** This requires $\|\sum_v\psi_v\otimes Y_v\|_F\ge s$. It uses the checkpoint normalization, provided $B$ is the zero-sum class reader (a G2-type premise; the checkpoint was stated for the capture protocol).

**Why existing results do not cover it.**
- Theorem B needs piecewise-parallel readouts; long masks rotate $\beta_t$.
- Lemma U / Theorem B-F need one-step captures.
- Astra's and Lemma M's passivity bounds assume survivors are uniform between captures.
- Codex's moving-cycle exhaustion assumes one-step captures and public segments.
- The finite-stage obstruction $D\le RK$ is not binding, because donor controls per group are unbounded.
- **The proved bounds still allow it.** Theorem F with $Z=y$ gives $D\lesssim\|F\|_{\rm op}^2(\Lambda/s)^2$, and $\|F\|_{\rm op}$ can be $\gg1$ for overlapping filters. Carl–Pajor with $TK$ atoms allows a factor $\log(TK/D)\asymp\log n\ge R$. So **$D=\Theta(n)$ at Route-6 cost is not excluded by any proved bound.**

**Hostile assessment (why it probably fails).**
1. **Mass reuse needs independent weights on the same mass.** Lemma TV forces every effective filter to be a variation-$\le1$ average of monotone $[0,1]$ profiles.
   - Positive monotone kernels such as $e^{-\lambda(T-t)}$ have exponentially decaying singular values (Laplace-transform ill-conditioning). The apparent $R$-fold reuse is paid back in condition number.
   - Well-conditioned choices (nested windows) are piecewise-parallel, and are capped at $\log R$ by Theorem B (or at $O(1)$ by Theorem F when orthogonalised).
2. **Passivity for long masks is unproved.** The survivor hub is split, so the cone and arrowhead bookkeeping must be redone.
3. **Exhaustion for long masks is unproved.** The moving-cycle and stationary nuisance codes must be re-derived.

**Status: OPEN, leaning negative.** The decisive lemma is in Section 6.

### 4.2 Rank 2 — Private gate-coded captures — targets (E3) — **REFUTED as a route to $o(n^{3/2})$**

**Construction.**
- Capture masks become **private controls**: capture $e$ uses survivor gates $\bar g+b\,c_{e,i}$, with $c_e\in[-1,1]^{m/2}$ given by the clipped full-spark code of the frontier (§4 there).
- This escapes Theorem F's fixed-$U$ hypothesis: the protected subspace is history-dependent.

**Lemma C (rank-one collapse) [PROVED, author-local].** Suppose $y_t=0$ outside a write interval preceding all captures (a shared row). Then every survivor site satisfies

$$
x_i=\Big(\prod_e a(\bar g+b\,c_{e,i})\Big)(ag_H)^{\#}\,\frac{Y}{\sqrt{h_S}},\qquad Y=\sum_ty_t .
$$

So the survivor content is rank one, and the $R$ masks enter only through one scalar per site. A shared row stores at most $m/2$ numbers, whatever $R$ is.

*Proof.* In the normal form, $\phi_i(t)$ for $t$ in the write interval equals a common public scalar times $\prod_ea\,g_i(c_e)$, independent of $t$. ∎

**Fresh rows.** Each additional independent row needs its own write.
- **Bilinear terms are useless for sections.** $c\otimes r$ is even under joint sign flip. With $c=c_0+\varepsilon(\theta)$ and $r=r_0+\eta(\theta)$, the antipodal difference is $2(\varepsilon\otimes r_0+c_0\otimes\eta)$: additive, not multiplicative.
- **So each write yields at most** $m/2+K$ dimensions, at write length $\gtrsim c\,n/\sqrt m$ (same calculation as frontier §§7–10).
- **Cost.** $D\asymp n$ needs about $R$ writes, so $mT\gtrsim Rn\sqrt m=\sqrt R\,n^{3/2}$ at $m=n/R$.

This is a scaling argument, not a theorem.

**Side issue.** Private masks make survivor local traces private: an extra private local channel, carrying the same information.

### 4.3 Rank 3 — Track-sweep spatial gate field (time → space) — **boundary only**

**Construction.**
- Donor tuples take gates that are a **private function of physical position**: the site occupying column $c$ has gate $\bar g_0+b\,\zeta(c)$, where $\zeta\in[-1,1]^{\rm columns}$ is coded continuously.
- The moving tracks sweep the columns.
- The moving-cycle parameter columns, the *nuisance* of Codex's exhaustion, become the memory medium. This is legal because private within-segment switching is outside the exhaustion scope.

**Mechanism.**
- $A(c)=\psi^TH_Ne_c=\big(\bar g_0+b\zeta(c)\big)\sum_{s:\ \text{track at }c}c\,\Lambda(s)\;+\;$ (a causal spatial filter of $\zeta$).
- Hence $D\lesssim\#\text{swept columns}\le m+N$.

**Scaling (heuristic).**
1. The donor costate satisfies $|c\Lambda|\le2/\sqrt{h_S}$.
2. For a zero-sum protected row, the costate mean arises only through captures, so $|U|\lesssim abA_0$. The per-column private amplitude is therefore $\lesssim2b^2\sqrt{2m}$.
3. Robust separation needs $(m+N)m^2\gtrsim C_\zeta n^2$.
4. With no-wrap, $N\le n/400$. So $D=\Theta(n)$ forces $N=\Theta(n)$ and $m\gtrsim c\sqrt n$, i.e. $mT=\Theta(n^{3/2})$.

**Assessment.** Not $o(n^{3/2})$. It is a potentially new boundary construction with only $m=\Theta(\sqrt n)$ driven tuples (unverified).

## 5. Hostile self-review

| Check | Finding |
|---|---|
| Hidden logarithms | Theorem F has none; Lemma F is sharp ($\lfloor1/r^2\rfloor$). Theorem B-F removes the $\log R$ and $C_{\rm CP}$ of Theorem B. |
| Energy depletion | All $\Lambda$ inputs rest on passivity: Lemma M (weak captures) and Astra (separated captures). Unproved for MTAB's long masks. |
| Ill-conditioned modes | The central MTAB risk (§4.1, item 1). |
| False independence | Lemma C: shared-row private captures collapse to rank one. Bilinear codes are even under $\theta\mapsto-\theta$. |
| Illegal queries | None introduced; all separation goes through the original checkpoint. The reader-support premise (G2 of the Theorem B archive) is inherited. For MTAB, $B$ must be the zero-sum class reader. |
| Trace corrections | Donors: inherited exact correction. Survivors: public in MTAB, **private in §4.2** (gap). |
| Fixed readout | Theorem F needs $U$ independent of $\theta$. §4.2 is the only candidate violating this, and it fails for a different reason. |
| Common-mode reading | Lemma U is proved for $B$ reading non-empty characters only. If $B$ also reads the common mode, numerics give $\|U_{\rm all}\|\le4.6$ at $R=10$, still $O(\sqrt{R})$-like. |
| Scope of Theorem B-F | One-step balanced captures, distinct characters, uniform survivors otherwise. It inherits every upstream premise of the Theorem B archive (§§1, 11 there). |

## 6. Next falsifiable theorem — TV-filter width theorem

**Conjecture TV-W.**
- **Setting.** Let $f_1,\dots,f_d:\{1..T\}\to[-1,1]$ be public, with $\mathrm{TV}(f_v)\le1$, and $\psi_v$ orthonormal.
- **Section.** Consider sections with $X(\theta)=\sum_v\psi_v\otimes\sum_tf_v(t)y_t(\theta)$, $\sup_\theta\sum_{t,j}|y_{tj}|\le\Lambda$, and $\|X\|_F\ge s$ on the equal-code set.
- **Claim.** $D\le q+C(\Lambda/s)^2(1+\log(1+d))$ for an absolute constant $C$.

**What it would decide.**
- *True:* MTAB is dead, and, with passivity for long masks, the single-channel fixed-source corridor obeys $D\lesssim(mN/n)^2\log R$.
- *Refuted* by a legal family with $D\ge\omega(\log d)(\Lambda/s)^2$: Route 7B (MTAB) is revived.

**Proof idea.**
1. Summation by parts: $\sum_tf_v(t)y_t=f_v(T)Y_T-\sum_t\Delta f_v(t)Y_t$. Each readout is the cumulative path $Y_t$ integrated against a signed measure of mass $\le2$.
2. Decompose those measures dyadically in time.
3. Apply Theorem F in the dyadic Haar basis, whose $\ell_2$-conditioning is $O(1)$ per scale, with Carl–Pajor across the $O(\log)$ scales.

## 7. Complete follow-up research prompt

> Repository soma2-stack/AI-Architecture-Research, branch main. Read `theory/claude_route_7b_20261007/RESEARCH.md` and `REVIEW_HANDOFF.md`, `theory/opus_segment_atom_width_20261007/PROOF.md`, and `theory/astra_separated_strong_capture_20261007/PROOF.md`. Do not modify CURRENT_THEORY.md or promote statuses.
>
> (1) Independently verify or break Lemma F, Theorem F, Lemma U and Theorem B-F, with special attention to the zero-set index fact (I2), the nerve construction, and the Toeplitz/orthogonality proof of $\|U_{\rm prot}\|\le2$.
>
> (2) Prove or refute Conjecture TV-W. Either construct a legal public-survivor filter bank (MTAB) whose robust section exceeds $C(\Lambda/s)^2\log(1+d)$, or prove the bound.
>
> (3) Prove a passivity (signal-mass) bound $\Lambda\le C\sqrt KN$ for arbitrary public survivor schedules (long masks), extending the arrowhead/cone arguments to a split survivor hub.
>
> (4) If (2) and (3) hold, state the resulting corridor-wide obstruction precisely, and list every remaining escape: private survivor schedules, the full parameter family with state features, and the redesigned multi-channel feedback outside the fixed $R$.
>
> Archive results under `theory/<agent>_tv_width_<date>/` with a REVIEW_HANDOFF.md, update INDEX.md as PENDING REVIEW, commit and push without force.

## 8. Files

| File | Purpose |
|---|---|
| `fan_ratio_check.py`, `.out` | Uniform-sample probe; misses Fan points by design (documented) |
| `fan_ratio_search.py`, `.out` and `fan_ratio_search_d8.py`, `.out` | Adaptive search; confirms ratio $\ge D$ at $D=5,6,8$ |
| `capture_opnorm_check.py`, `.out` | Exact finite-$R$ operator norms for Lemma U |

All are falsification probes; none is evidence for an asymptotic theorem.
