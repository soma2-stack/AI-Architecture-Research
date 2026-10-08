# Route 7B: the multi-timescale accumulator bank (MTAB): exact operator, a sharp no-reuse theorem, and TV-W

Author: Claude Opus 5.5 (Claude lane). Date: 2026-10-07. **Repository status: PENDING REVIEW.**

**Labels.**
- Author-local labels (PROVED, CERTIFIED, OPEN) are not repository VERIFIED status.
- The scripts in this folder are bounded experiments. A numerically found basis is a rigorous *instance* certificate, valid up to floating point, via Theorem Γ. It is never a general proof.
- `CURRENT_THEORY.md` is not modified. Route 7A and Theorem B/Lemma U are not re-audited.

**Target.** A legal construction with $D=\Omega(n)$ and $mT=o(n^{3/2})$.

**Central question.** Can several public survivor filters reuse the same feedback signal to create many robust, independent memory dimensions without paying for repeated writes?

## 0. Answer and status

**Short answer: no**, for every MTAB design that was actually proposed, and for every legal family tested. The precise claims follow.

| Claim | Status |
|---|---|
| Exact feedback-to-protected operator for MTAB, including its measure representation (§1) | PROVED (author) |
| Theorem Γ (factorisation width bound; generalises Theorem F) (§3) | PROVED (author) |
| **Theorem NC.** If the survivor profiles never cross, then $D-q\le\lfloor c_\star^2(\|B\|\Lambda/s)^2\rfloor$ with $c_\star=(2+\sqrt2)/3$, i.e. $c_\star^2\approx1.2952$. The bound is uniform in the number of classes $C$, the horizon $T$, the timescales and the gates. (§4) | PROVED (author). The Haar constant is sharp. |
| Both proposed MTAB designs (constant multi-timescale rates; staggered starts) are non-crossing, so their promised $d_{\rm eff}$-fold reuse is impossible (§4.3) | **MTAB as designed: REFUTED** |
| Crossing families with $M$ level orders: $\gamma^{2/3}$ is subadditive, giving $D-q\le c_\star^2(\sum_m\mu_m^{2/3})^3(\|B\|\Lambda/s)^2$ (§5.1) | PROVED (author); weak in practice |
| All legal and idealised crossing families tested, including the new "MTAB-X" band design and an adversarial search, certify $\gamma\le1.04$ in the tested range. Crossing *creates* independent filters but *destroys* amplitude (§5.2) | CERTIFIED per instance; general case OPEN (Conjecture MON) |
| Literal Conjecture TV-W (per-filter variation, orthonormal rows) (§6) | **REFUTED** by repeated filters (not corridor-realizable) |
| Corrected strong form TV-W* (bounded variation for every unit combination), no logarithm | Proved for non-crossing families; OPEN in general |
| Constant-rate profiles: geometric singular-value decay (my old "Laplace" claim). Staggered starts: $\sim1/k$ decay (Gemini's window point). Neither affects robust dimension (§7) | Numerical, explained |

**Strongest finding.** For non-crossing public survivor schedules, having many independent temporal filters gives no extra robust dimension. Theorem NC caps the survivor-side protected readout at $c_\star^2=1.295$ times the budget $(\Lambda/s)^2$. That is about the budget of a single orthonormal reader. It holds even though the operator norm can be $\sim\sqrt T$ (§2). Mass reuse in Route 7B's sense (lever E1) is therefore excluded for non-crossing schedules, and in every crossing family tested. Any surviving route must change $\Lambda/s$ itself.

## 1. MTAB: legal profiles and the exact operator

**Construction** (from [`../claude_route_7b_20261007/RESEARCH.md`](../claude_route_7b_20261007/RESEARCH.md) §4.1):
- $C=2^r$ equal public survivor classes;
- donor groups use private gate words;
- survivor class $c$ uses a public gate word $g_c(r)\in[g_L,g_H]$ during the write interval ($g_L=.995$, $g_H=1$ in the experiments), and $g_H$ afterwards;
- then the inherited trace correction, clear and reset.

**Explicit overlapping profiles** (all legal, gates in $[.995,1]$; generators in `mtab_width_probe.py`):
- **rates:** $g_c\equiv1-\varepsilon_c$, with $\varepsilon_c$ geometric in $[10^{-5},5\cdot10^{-3}]$;
- **staggered:** $g_L$ before $t_c$, $g_H$ after;
- **random words:** blocks of 50 steps, each block's gate $g_L$ or $g_H$ uniformly at random;
- **bands (MTAB-X, §5):** $M$ time bands; in band $m$, class $c$ is low for $\mathrm{rank}_m(c)\cdot B/C$ steps, with independent random ranks per band.

**Profiles.** Survivor sites co-move and receive feedback only through the common term (normal form, §1 of the Route 7B file). A site of class $c$ applies
$$
\phi_c(t)=\prod_{r=t+1}^{N}a\,g_c(r)\in(0,1],
$$
which is non-decreasing in $t$, with $\phi_c\equiv$ common after the write.

**Exact operator.** Take orthonormal class coordinates $b_c=\mathbf 1_{\text{class }c}/\sqrt{h_S/C}$. A survivor site in class $c$ holds $h_S^{-1/2}\sum_t\phi_c(t)y_t$. So, per parameter column,
$$
x=\mathcal U y:=C^{-1/2}P_0\,\Phi\,y,\qquad \Phi_{ct}=\phi_c(t),\qquad X=B(\mathcal U\otimes I_P)\,y . \tag{1.1}
$$
Here $P_0$ is the zero-sum (protected) projection and $B$ reads protected rows (premise G2, $\|B\|\le1$). The atoms are
$$
a_t=C^{-1/2}P_0\,\phi(t),
$$
where $t\mapsto\phi(t)$ is a coordinatewise non-decreasing path in $[0,1]^C$.

**Measure representation.** Let $G(\tau)=\sum_{t\ge\tau}y_t$ (tail sums), so $\|G\|_\infty\le\|y\|_1$ and $\mathrm{TV}(G)\le\|y\|_1$. Let $\mu_c$ be the sub-probability measure on times with CDF $\phi_c$. Then
$$
(\Phi y)_c=\int G\,d\mu_c .
$$
Each class reads the cumulative signal path through a probability-like measure. Profiles "cross" exactly when these measures are not stochastically ordered.

## 2. Three different notions (the distinction requested)

1. **Independent temporal filters.** These are the nonzero singular values of $\mathcal U$.
   - Sharp staggered steps: $\|\mathcal U\|_{\rm op}$ grows like $\sqrt T$, with about $1/k$ singular-value decay.
   - Random multi-level crossing chains have up to 127 singular values above $10\%$ of the top at $C=128$ (`mtab_wide_probe.out`).
2. **Signal reuse.** This is $D/(\Lambda/s)^2$ beyond $O(1)$, i.e. the same $\ell_1$ signal mass supporting more robust dimensions than an orthonormal reader allows.
3. **Robust readout dimensions.** This is $D$ itself: the largest sphere of legal histories whose protected readouts stay $s$-separated off a $q$-dimensional nuisance code.

**Theorem F does not decide reuse.** It bounds $D-q$ by $\|\mathcal U\|_{\rm op}^2(\Lambda/s)^2$, which is huge for staggered steps. Theorem NC shows the true constant is at most 1.2952. Many independent filters, which notion 1 counts, do not imply reuse, which notion 2 measures.

## 3. Theorem Γ (factorisation width bound)

**Theorem Γ.** Use the robust-section setting of Theorem F:
- an odd continuous $y(\theta)\in\mathbb R^N$ with $\|y\|_1\le\Lambda$;
- readout $\mathcal Ty$ with $\|\mathcal Ty\|_2\ge s$ on the zero set of an odd nuisance code $c:S^{D-1}\to\mathbb R^q$.

For every factorisation $\mathcal T=\mathcal A\mathcal W$ (with $\mathcal W$ linear into $\mathbb R^M$, or more generally odd continuous with $\|\mathcal W(y)\|_1\le\kappa\|y\|_1$),
$$
D\le q+\Big\lfloor\Big(\gamma\,\frac{\Lambda}{s}\Big)^2\Big\rfloor,\qquad \gamma=\|\mathcal A\|_{2\to2}\cdot\max_i\|\mathcal We_i\|_1\ \ (\text{resp. } \|\mathcal A\|\kappa).
$$

*Proof.*
1. $Z=\mathcal Wy$ is odd and continuous.
2. On $W_0=c^{-1}(0)$, $\|\mathcal AZ\|\ge s$. Hence $Z\neq0$ and $\|Z\|_2\ge s/\|\mathcal A\|$.
3. Also $\|Z\|_1\le\Lambda\max_i\|\mathcal We_i\|_1$.
4. $\mathrm{ind}(W_0)\ge D-1-q$ by (I2). Lemma F then gives a point where $\|Z\|_1^2\ge(D-q)\tau\|Z\|_2^2$; let $\tau\to1$. ∎

**Special cases.**
- $\mathcal W=I$ is Theorem F.
- For an orthonormal basis $Q$ of the protected space, $\gamma=\|B\|\max_t\|Qa_t\|_1$. Here $\mathcal W=Q\,\mathcal U$ and $\mathcal A=B\,Q^T$, and the bound is the same for any number $P$ of columns because $\ell_1$ adds over columns.
- **Subadditivity.** If $\mathcal T=\mathcal T_1+\mathcal T_2$, stack $Z=(\alpha_1\mathcal W_1y,\alpha_2\mathcal W_2y)$ and optimise the weights with Hölder. This gives $\gamma(\mathcal T)^{2/3}\le\gamma(\mathcal T_1)^{2/3}+\gamma(\mathcal T_2)^{2/3}$.

## 4. Theorem NC (non-crossing profiles): no mass reuse

**Definition.** A family is *non-crossing* if some order $\sigma$ of classes has $\phi_{\sigma(1)}(t)\ge\phi_{\sigma(2)}(t)\ge\dots$ for every $t$. Equivalently, the measures $\mu_c$ are stochastically ordered.

**Theorem NC.** In the setting (1.1), with $C=2^r$ equal classes and non-crossing profiles,
$$
D-q\le\Big\lfloor c_\star^2\Big(\frac{\|B\|\Lambda}{s}\Big)^2\Big\rfloor,\qquad c_\star=\frac{2+\sqrt2}{3}=\frac{1/3}{1-2^{-1/2}}\approx1.1381 .
$$
The bound does not depend on $C$, $T$, $N$, the timescales, the gate values, or $a$.

*Proof.*
1. **Basis.** Let $H$ be the orthonormal Haar basis of the zero-sum subspace of $\mathbb R^C$, in the order $\sigma$. For a level-$\ell$ block (size $2^\ell$) it has rows $h=2^{-\ell/2}(\mathbf 1_{\rm left}-\mathbf 1_{\rm right})$. Apply Theorem Γ with $Q=H$.
2. **Layer cake.** Each $\phi(t)$ is $\sigma$-nonincreasing with values in $[0,1]$, so $\phi(t)=\int_0^1\mathbf 1_{\{\text{prefix of length }k_\lambda(t)\}}d\lambda$. By convexity of $\ell_1$,
   $$
   \|Ha_t\|_1\le\sup_k\|H\,C^{-1/2}\mathbf 1_{[1,k]}\|_1 .
   $$
   The common-mode part is orthogonal to $H$.
3. **Prefix computation.** For the prefix $[1,k]$, only the block containing the cut at each level contributes, with coefficient $2^{-\ell/2}\min(j,2^\ell-j)$, where $j=k\bmod2^\ell$. With $x=k/2^r$ and $\|\cdot\|$ the distance to $\mathbb Z$,
   $$
   \|H\,C^{-1/2}\mathbf 1_{[1,k]}\|_1=\sum_{m=0}^{r-1}2^{-m/2}\,\|2^mx\|=:f_r(x),
   $$
   a truncated Takagi–Landsberg function with weight $w=2^{-1/2}$.
4. **Lemma (Takagi bound).** For $\tfrac12\le w<1$, $f_r(x)\le M:=1/(3(1-w))$ for all $r$ and $x$.

   *Proof by induction on $r$.* The cases $r=0,1$ are clear, since $\|x\|\le\frac12\le M$. By symmetry take $x\in[0,\frac12]$.
   - If $x\le\frac13$: $f_r(x)=x+wf_{r-1}(2x)\le\frac13+wM=M$.
   - If $x\in(\frac13,\frac12]$: $\|2x\|=1-2x$, so $f_r(x)=x+w(1-2x)+w^2f_{r-2}(4x)\le x(1-2w)+w+w^2M$. This is non-increasing in $x$ because $w\ge\frac12$, so it is at most $\frac{1+w}3+w^2M=M$. ∎

   With $w=2^{-1/2}$, $M=(2+\sqrt2)/3$. Taking $x\to\frac13$ (alternating bits) shows the constant is attained in the limit. `mtab_constants.out` gives $c_\star(r)=0.500,\,0.604,\dots,1.1342\ (r{=}16),\,1.1378\ (r{=}24)$; for $r\le8$ these agree with the explicit Haar basis.
5. **Conclusion.** Theorem Γ with $\gamma\le\|B\|c_\star$. ∎

### 4.1 Sharpness and meaning

The bound is a pure multiple of $(\Lambda/s)^2$. By Lemma F applied to a coordinate sphere, a single orthonormal reader already gives order $(\Lambda/s)^2$. MTAB with any number of non-crossing timescales therefore buys at most a constant factor of 1.2952. That is less than the factor 8 allowed for one-step captures by Theorem U*, and it has no $C$, $d$ or $\log$ dependence.

### 4.2 Why both MTAB designs are non-crossing

- **Constant rates.** $\phi_c(t)=(ag_c)^{N-t}$ is ordered by $g_c$ for every $t$.
- **Staggered starts.** Let $t_c<t_{c'}$. For $t\ge t_{c'}$ the two profiles are equal. For $t_c\le t<t_{c'}$, $\phi_c/\phi_{c'}=(g_H/g_L)^{t_{c'}-t}\ge1$. For $t<t_c$, the ratio is $(g_H/g_L)^{t_{c'}-t_c}\ge1$. So class $c$ stays ahead throughout.
- **Generally,** any family indexed monotonically by a single scalar parameter (rate, start time, or both moving together) is non-crossing.

### 4.3 Consequence for MTAB

The MTAB premise was $D\approx d_{\rm eff}K$ with $d=C-1$ filters reading the same mass. Theorem NC gives instead
$$
D-q\le1.2952\,(\|B\|\Lambda/s)^2 .
$$
So the $d$-fold reuse is impossible: **MTAB as designed is refuted.** Suppose a long-mask passivity bound $\Lambda\le c_\Lambda\sqrt KN$ held; it is unproved for split survivor hubs. With $s=9.5\cdot10^{-5}n/\sqrt m$ and $K\le m$, this gives $D-q\le1.2952\,c_\Lambda^2\cdot1.11\cdot10^8\,(mT/n)^2$. So $D=\Omega(n)$ still forces $mT=\Omega(n^{3/2})$: the same wall as before.

## 5. Crossing families: the improved mechanism MTAB-X and why it fails

### 5.1 A rigorous but weak bound

Partition the levels $\lambda\in(0,1)$ into sets $\Lambda_m$ (of measure $\mu_m$) on which one order $\sigma_m$ makes every level set $\{c:\phi_c(t)>\lambda\}$ a $\sigma_m$-prefix. Splitting the layer cake gives $\mathcal U=\sum_m\mathcal U_m$ with $\gamma(\mathcal U_m)\le c_\star\mu_m$. By subadditivity,
$$
D-q\le c_\star^2\Big(\sum_m\mu_m^{2/3}\Big)^3\Big(\frac{\|B\|\Lambda}{s}\Big)^2\le c_\star^2\,M\,(\|B\|\Lambda/s)^2 .
$$
This allows at most $M$-fold reuse, where $M$ counts distinct first-passage orders. It is very loose in practice; the next subsection shows why.

### 5.2 MTAB-X (invented here) and the certificates

**Idea.** Maximise crossing on purpose. Use $M$ bands, each sorting the classes in an independent random order, so that the level orders are as unrelated as possible. If reuse exists anywhere among survivor-side schedules, it should appear here.

**Result.** Each instance below is certified rigorously by Theorem Γ with an optimised orthonormal basis, checked on all atoms.
- **Legal gates** ($[.995,1]$, $N=2400$, $C\le64$; `mtab_width_probe.out`):
  - every family has $\gamma\le0.81$;
  - stable rank is only $1.0$–$1.7$, with $\|\mathcal U\|_{\rm op}$ between 2.5 and 14.8;
  - bands with $M=4$ or $16$ give $\gamma=0.28$–$0.77$, below the non-crossing staggered family (0.60–0.81).
- **Idealised arbitrary monotone profiles**, a superset of everything legal ($C\le128$; `mtab_wide_probe.out`):

  | Family | $\gamma_{\rm cert}$ |
  |---|---|
  | sharp staggered steps | 0.88–1.05 |
  | 2 levels | 0.48–1.04 |
  | 4 levels | 0.28–0.51 |
  | 16 levels | 0.09–0.15 |
  | $C$ random levels | 0.035–0.093 |
  | adversarial search over 40 level structures ($C=32$) | max 1.17, a mis-ordered non-crossing case (Theorem NC applies to it) |

**Mechanism of failure.** Crossing creates many independent filters: stable rank rises to 45 and 127 singular values exceed 10% of the top at $C=128$. But each band carries only weight $1/M$ of every profile. The crossing components therefore average out, and both the atom norms and $\gamma$ collapse. Independent temporal filters and signal reuse move in opposite directions.

**Conjecture MON (survivor-side no-reuse).** For every public survivor schedule (any co-moving profiles, crossing allowed), $\gamma\le c_\star$. Hence $D-q\le1.2952(\|B\|\Lambda/s)^2$.
- *If true:* Route 7B's lever E1 is closed for the whole single-channel public-survivor corridor.
- *Falsifier:* an instance whose best certificate exceeds $c_\star$, together with a matching section.

## 6. Conjecture TV-W

**The literal statement is refuted.** Its hypotheses were per-filter $\mathrm{TV}(f_v)\le1$, $|f_v|\le1$, and orthonormal $\psi_v$.
- **Counterexample.** Take $D$ groups of $b$ identical window filters $f=\frac12\mathbf 1_{W_i}$ (each TV 1). A coordinate section on $D$ times gives $\|x\|\ge\frac12\sqrt{b/D}\,\|\theta\|_1$, so $D\rho^2=b/4=d/(4D)$.
- This beats $C(1+\log(1+d))$ by an unbounded factor (`mtab_constants.out` (c): ratios 3.1, 8.8 and 27.5 at $d=64,512,4096$).
- **Not corridor-realizable.** The unit row $\frac1{\sqrt b}\sum\psi$ would have $|f|=\sqrt b/2>1$, contradicting Lemma TV.

**Corrected strong form TV-W\*.** Assume $\sup_{\|u\|=1}|\langle u,f(t)\rangle|\le1$ and $\sup_{\|u\|=1}\mathrm{TV}\langle u,f\rangle\le1$. Equivalently, the increments $\Delta f(t)$ generate a zonotope contained in the unit ball, and the atoms are suffix sums of its generators.

**Claim.** $D-q\le C_0(\Lambda/s)^2$, with no logarithm.

**Status.**
- Proved for MTAB-realizable non-crossing families, with $C_0=1.2952$ (Theorem NC).
- Proved with factor $M$ for $M$-order crossing families.
- Open in general, i.e. for general zonotope suffix-sum families, which include MON.

The original Haar-in-time proof idea loses $\log T$: one jump costs at every dyadic level. The class-side Haar basis of Theorem NC is what removes it.

## 7. Spectra and conditioning on donor-generated signals

From `mtab_constants.out` (b), at $C=32$, $N=2400$:

| Family | Singular values (raw) | With donor relaxation smoothing |
|---|---|---|
| Constant rates | $14.05,\,2.18,\,0.39,\,0.062,\,0.009,\,10^{-3}$: geometric decay, $\sigma_{10}/\sigma_1=1.4\cdot10^{-9}$ | $\sigma_5/\sigma_1\approx10^{-4}$ |
| Staggered starts | $13.0,\,6.0,\,3.6,\,2.4,\,1.7,\,1.2$: about $1/k$ | $\sigma_5/\sigma_1=0.03$–$0.08$ |

The smoothing models donor relaxation: $y=Ku$ with $K_{ts}=e^{-\epsilon(t-s)}$, $\epsilon\in\{10^{-3},5\cdot10^{-3}\}$.

- My earlier claim of "Laplace ill-conditioning" is correct for constant-rate filters.
- Gemini's objection is correct for staggered (window) filters, which are well conditioned.
- **But conditioning is not the obstruction.** Both families obey Theorem NC with the same constant. The obstruction is geometric: atoms of a non-crossing family are sparse in the class-ordered Haar basis. This is exactly why the "TV alone proves bad conditioning" argument was unnecessary, and also insufficient.

## 8. Cost and separation

No candidate survives Theorem NC and the certificates, so a full cost-and-separation calculation was not carried out. The budget implication is stated in §4.3.

## 9. Failed ideas (preserved)

1. **MTAB, constant rates.** Non-crossing, so killed by Theorem NC.
2. **MTAB, staggered starts.** Non-crossing, so killed by Theorem NC.
3. **MTAB-X, random-order bands** (invented here). Crossing reduces the certified $\gamma$ (§5.2).
4. **Bounding via Theorem F's $\|\mathcal U\|_{\rm op}$.** Useless: it grows like $\sqrt T$ for staggered steps.
5. **Time-Haar factorisation** (the original TV-W proof idea). Loses $\log T$; only the class-side basis works.
6. **Counting "level orders" as the reuse measure.** The heuristic count in `mtab_width_probe.py` is large while $\gamma$ is small, so the $M$-bound is loose.
7. **Relay (survivors later turned into donors to re-emit stored content).** Re-emitted signal is still counted in $\Lambda$, and its fan-out to many filters is exactly what NC caps. No gain.
8. **Private survivor profiles.** This is Rank 2 of the Route 7B file: rank-one collapse plus write-yield scaling.

## 10. Next exact obligation

1. **Prove Conjecture MON**, i.e. $\gamma\le c_\star$ for arbitrary crossing monotone profiles. A route: find an order-free sparsifying frame for monotone paths in $[0,1]^C$, or prove TV-W\* for zonotope suffix sums. Proving MON together with long-mask passivity closes lever E1 for the whole single-channel public-survivor corridor.
2. **Prove long-mask passivity** $\Lambda\le c_\Lambda\sqrt KN$ when the survivor hub is split into $C$ public classes. This requires redoing the cone and arrowhead bookkeeping. It is needed to turn §4.3 into an unconditional MTAB budget.
3. **Next mechanism.** After 1–2, Route 7B must leave survivor-side filtering. The remaining levers are E2 (signal mass above passivity; Route 7A's territory, so coordinate rather than duplicate) and E3 (history-dependent readout). The cheapest falsifiable step is an exact maximisation of $\Lambda$ under the exact recurrence for a fixed public schedule. It would show whether any legal donor schedule beats $\sqrt KN$ by more than a constant.

## 11. Files

| File | Content |
|---|---|
| `RESEARCH.md` | This file. |
| `REVIEW_HANDOFF.md` | Claims to verify. |
| `mtab_core.py` | Profiles from gates, atoms, Haar basis, certificates, basis optimiser. |
| `mtab_width_probe.py` / `.out` | Legal families: spectra, Haar and optimised certificates. |
| `mtab_wide_probe.py` / `.out` | Idealised monotone families (a superset of legal ones), MTAB-X, adversarial search. |
| `mtab_constants.py` / `.out` | Sharp $c_\star(r)$; spectra on donor-smoothed signals; the literal TV-W counterexample. |
