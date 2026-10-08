# Lemma U repair: dependent Walsh characters, the true operator norm, and Theorem B-F

Author: Claude Opus 5.5 (Claude lane). Date: 2026-10-07. **Repository status: PENDING REVIEW.**

This is an author derivation, not an independently reviewed result. Author-local words such as *proved* are not repository VERIFIED status. The scripts in this folder are falsification probes and finite witnesses, not proofs. `CURRENT_THEORY.md` is not modified.

Targets:
- Lemma U and Theorem B-F of [`../claude_route_7b_20261007/RESEARCH.md`](../claude_route_7b_20261007/RESEARCH.md) §3.4;
- the Lemma U repair in [`../gemini_route7b_audit_20261007/PROOF.md`](../gemini_route7b_audit_20261007/PROOF.md) §4.

Theorem F (§3.3 of the Route 7B file) is used only as a black box, with whatever value of $\|U\|$ is valid. Nothing here assumes Lemma U.

## 0. Verdicts

| Item | Verdict |
|---|---|
| Lemma U as stated ($\|U_{\rm prot}\|\le2$ for all distinct Walsh characters, uniformly in $R$) | **REFUTED.** For every legal contrast ratio $b/g_H\in(0,\frac12]$, at $ag_H=1$, $\sup_R\|U_{\rm prot}\|\ge1+\sqrt2\approx2.414$. Each finite witness persists for $ag_H$ close enough to 1, by continuity. Explicit legal witnesses are in §7.3. |
| Original proof step 2 (orthogonality) | False for dependent labels, as Gemini found. It is correct exactly when the labels are linearly independent (§6). |
| Gemini's repair (cross terms $\le2b(a\bar g)^{\vert e-f\vert-1}$, Gershgorin $\le 1+2b/(1-a\bar g)\le2$, hence $\|U_{\rm prot}\|\le2$) | **REFUTED.** The cross-term bound fails by factors up to $10^{96}$. The Gram row sums grow like $\log R$. The Gershgorin arithmetic gives 3, not 2, at $ag_H=1$. The final $\le2$ is false (§3.3). |
| Corrected Lemma U* (§5) | **Proved here.** $\|U_{\rm prot}\|\le2\sqrt{1+(ag_H)^2}\le2\sqrt2$ for all distinct nonzero labels, all $R$, all legal $a,g_H,b$, inter-capture gaps and resets. Refinement: $\|U_{\rm prot}\|^2\le(1+(ag_H)^2)\min\{4,(b/g_H)R\}$. |
| Linearly independent labels (§6) | $\|U_{\rm prot}\|\le\sqrt{1+(ag_H)^2}\;ab/(1-a\bar g)\le\sqrt2$. |
| Sharp constant | **Uniform constant** (supremum over $R$, labels and legal $a,g_H$): it lies in $[1+\sqrt2,\ 2\sqrt2]$. **At $b=g_H/2$:** exactly $1+\sqrt2$, approached as $ag_H\to1$, $R\to\infty$ and never attained; for each fixed $ag_H$, $\|U_{\rm prot}\|<\sqrt{1+(ag_H)^2}(1+2^{-1/2})$. **For $0<b<g_H/2$:** $1+\sqrt2$ is conjectured exact (Conjecture S). |
| Theorem B-F (§8) | **Survives with constant 8.** $D-q\le\lfloor8(\Lambda/s)^2\rfloor$, replacing 4. The operator-norm route cannot do better than $(1+\sqrt2)^2(\Lambda/s)^2\approx5.83(\Lambda/s)^2$. For independent labels, $D-q\le\lfloor2(\Lambda/s)^2\rfloor$. |
| Log-free Route-6 corollary | Survives: $D-q\le1.42\cdot10^{10}\,KN^2m/n^2=o(n)$. It remains conditional on the same upstream inputs (§8). |
| Theorem F | Untouched (§9). |

## 1. Setting and the exact atom map

**Scope.** This is the one-step-capture scope of [`../opus_segment_atom_width_20261007/PROOF.md`](../opus_segment_atom_width_20261007/PROOF.md) §1:
- fixed source, no wrap, public survivor gates;
- every survivor site at $g_H$, except $R$ one-step balanced captures and the final common reset.

The survivor sites, which are co-moving, are split into $2^r$ equal classes labelled by $x\in\mathbb F_2^r$. Capture $e$ (in time order $e=1,\dots,R$) has label $\alpha_e\in\mathbb F_2^r\setminus\{0\}$, with all labels **distinct**. Its gate is
$$
\bar g+b\chi_e(x),\qquad \chi_e(x)=(-1)^{\alpha_e\cdot x},\qquad \bar g=g_H-b .
$$
So the gate is $g_H$ on one half and $g_H-2b$ on the other. Legality requires $0<b\le g_H/2$ and $0<a,g_H\le1$.

**Inner product.** Survivor content is a function on survivor sites, with $\langle f,g\rangle=\mathbb E_x[fg]$ (site average). The common mode $\mathbf 1$ then has norm 1, matching the archived $\mathbf 1_S/\sqrt{h_S}$. The projection $P$ removes the site mean ("protected part").

**Atoms (archived Lemma 2).** Injections are grouped into segments.
- The capture-step injection at capture $e$ has direction
  $$
  \mathrm{cap}_e=a(\bar g+b\chi_e)\cdot\prod_{e'>e}\big[\sigma_{e'}\,a(\bar g+b\chi_{e'})\big]\cdot\sigma_{\rm tail}.
  $$
  Here each $\sigma\in(0,1]$ is a scalar collecting $(ag_H)^{\Delta}$ over ordinary steps, and $aq_N$ at the reset.
- The interval ending just before capture $e$, if nonempty, has direction $ag_H\,\mathrm{cap}_e$, with weights $\lambda_t\le1$ absorbed into the coefficients $Z$.
- The interval after the last capture is a multiple of $\mathbf 1$, so its protected part is 0.

Hence, with $A_{\rm cap}=[\mathrm{cap}_1,\dots,\mathrm{cap}_R]$,
$$
U_{\rm prot}=P\,[\,A_{\rm cap}\mid A_{\rm cap}D\,],\qquad D=\mathrm{diag}\big(ag_H\,\mathbf 1[\text{interval before }e\neq\emptyset]\big),
$$
$$
\|U_{\rm prot}\|^2=\|PA_{\rm cap}(I+D^2)A_{\rm cap}^TP\|\le\big(1+(ag_H)^2\big)\,\|PA_{\rm cap}\|^2 . \tag{1.1}
$$
Equality holds when every interval is nonempty.

**Walk normalization.** Write
$$
a(\bar g+b\chi)=ag_H\big((1-p)+p\chi\big),\qquad p:=b/g_H\in(0,\tfrac12].
$$
Reverse time by setting $\beta_l:=\alpha_{R-l+1}$, and define
$$
u_k:=\prod_{l\le k}\big((1-p)+p\chi_{\beta_l}\big),\qquad k=1,\dots,R .
$$
Then $\mathrm{cap}_e=c_e\,u_{R-e+1}$ with $c_e\in(0,1]$ a product of $ag_H$ factors and the $\sigma$'s. So $A_{\rm cap}=A_{\rm walk}\,\mathrm{diag}(c)$, and
$$
\|PA_{\rm cap}\|\le\|PA_{\rm walk}\|,\qquad A_{\rm walk}=[u_1,\dots,u_R]. \tag{1.2}
$$

*Convention robustness.* Suppose the input at a capture step is gated without the factor $a$, i.e. by $G_t(aO_*M_{t-1}+I)$. Then $c_e$ becomes $g_H(ag_H)^{R-e}\cdot(\sigma\text{'s})\le1$. (1.1)–(1.2) are unchanged.

## 2. Random-walk representation (Lemma W)

**Lemma W.** Let $\varepsilon_l$ be i.i.d. Bernoulli$(p)$ and $X_k=\sum_{l\le k}\varepsilon_l\beta_l\in\mathbb F_2^r$, with law $\pi_k$. Then:
1. $u_k=\sum_\gamma\pi_k(\gamma)\chi_\gamma$, i.e. $\hat u_k=\pi_k$.
2. $\langle f,g\rangle=\sum_\gamma\hat f(\gamma)\hat g(\gamma)$, and $\widehat{Pf}=\hat f\,\mathbf 1_{\gamma\neq0}$.
3. In site form, $u_k(x)=q^{N_k(x)}$, where $q=1-2p$ and $N_k(x)=\#\{l\le k:\beta_l\cdot x=1\}$.

*Proof.*
1. $\mathbb E\,\chi_{X_k}(x)=\prod_l\mathbb E\,\chi_{\varepsilon_l\beta_l}(x)=\prod_l\big(1-p+p\chi_{\beta_l}(x)\big)=u_k(x)$, and $\mathbb E\,\chi_{X_k}=\sum_\gamma\pi_k(\gamma)\chi_\gamma$.
2. This is Parseval for the orthonormal characters.
3. Each factor equals 1 or $q$. ∎

Consequently, the protected Gram matrix of the walk atoms is
$$
\Gamma(j,k):=\langle Pu_j,Pu_k\rangle=\sum_{\gamma\neq0}\pi_j(\gamma)\pi_k(\gamma)\ \ge0,\qquad \|PA_{\rm walk}\|^2=\|\Gamma\|. \tag{2.1}
$$

## 3. Cross terms for arbitrary distinct labels (item 1)

### 3.1 Protected atoms (the correct object)

For $j\le k$, write $X_k=X_j+\Delta_{jk}$ with independent increment. Let $X'$ be an independent copy and $Y_j=X_j+X'_j$. $Y_j$ is the lazy walk with step probability $2p(1-p)$. Then
$$
\Gamma(j,k)=\Pr\big(Y_j+\Delta_{jk}=0\big)-\pi_j(0)\pi_k(0)\ \ge0 .
$$
The usable bound comes from Lemma A (§4):
$$
\boxed{\;0\le\Gamma(j,k)\le\min\{M_j,M_k\}\le\frac{1}{\max(j,k)+1},\qquad M_k:=\max_{\gamma\neq0}\pi_k(\gamma)\;} \tag{3.1}
$$
This holds because $\sum_{\gamma\neq0}\pi_j(\gamma)\le1$, and symmetrically. It also gives $\Gamma(j,k)\le p$ (§5). Numerically, $\max\Gamma(j,k)(\max(j,k)+1)=0.996$ over 200 random orders (checks S4).

### 3.2 Gemini's columns $\mathcal V_e\xi_e$

The columns are $v_e=\chi_e\prod_{e'>e}[\sigma_{e'}a(\bar g+b\chi_{e'})]\,\sigma_{\rm tail}$. Write $n_e=R-e$, and let $X^{(>e)}$ be the walk over the later labels $\alpha_{e+1},\dots,\alpha_R$. Then $\hat v_e$ is $c'_e$ times the law of $\alpha_e+X^{(>e)}$, so
$$
G_V(e,f)=\langle v_e,v_f\rangle=c'_ec'_f\,\Pr\big(\alpha_e+X^{(>e)}=\alpha_f+X'^{(>f)}\big)\ \ge0 .
$$
For $e<f$, substitute $\delta=X^{(>e)}$:
- the $\delta=0$ term is at most $\Pr(X^{(>f)}=\alpha_e+\alpha_f)\le1/(n_f+1)$, because $\alpha_e+\alpha_f\neq0$ and Lemma A applies;
- the $\delta\neq0$ terms total at most $M^{(>e)}\le1/(n_e+1)$.

Hence
$$
0\le G_V(e,f)\le\frac1{n_e+1}+\frac1{n_f+1}\quad(e\neq f),\qquad G_V(e,e)\le1 . \tag{3.2}
$$
This is the correct general cross-term bound. **It does not decay in $|e-f|$, and this is sharp.**

At $b=g_H/2$, $ag_H=1$, all labels of $\mathbb F_2^r$ in binary counting order (§7), the columns inside one "level" coincide: $v_e=\mathbf 1_H$ with $|H|=2^{-j}$. So $G_V(e,f)=2^{-j}$ for every pair in the level, with $|e-f|$ up to $2^{j-1}$.

### 3.3 Where Gemini's repair fails

1. **The cross-term claim $|G_V(e,f)|\le2b(a\bar g)^{|e-f|-1}$ is false.** In the counting family the maximal ratio of $G_V$ to this bound (checks S2) is:

   | $(r,b)$ | max ratio |
   |---|---|
   | $(4,.5)$ | $5.1\cdot10^2$ |
   | $(6,.5)$ | $3.6\cdot10^{16}$ |
   | $(8,.4)$ | $6.6\cdot10^{53}$ |
   | $(10,.2)$ | $2.2\cdot10^{96}$ |

   Gemini's own $R=3$ instance ($\langle\mathcal V_1\xi_1,\mathcal V_2\xi_2\rangle=2a^3\bar g^2b=0.088095$) is reproduced exactly (S1). It is consistent with the bound only because $R$ is tiny.
2. **Gershgorin cannot give a uniform constant.** The maximal off-diagonal row sum of $G_V$ is $1.31,\,2.27,\,3.22,\,3.91$ at $r=4,6,8,10$. It grows like $\log R$, as (3.2) allows.
3. **The arithmetic is off even granting the cross terms.** $1-a\bar g\ge b$ gives $1+2b/(1-a\bar g)\le3$, with equality at $ag_H=1$, not $\le2$.
4. **The final $\|U_{\rm prot}\|\le2$ is false** (§7.3). It was supported numerically only at $R\le31$. For $R\le31$ every tested norm is below 1.6; the excess over 2 appears from $R\approx2^{11}$ at $b=g_H/2$.

## 4. Lemma A (anti-concentration of lazy walks with distinct steps)

**Lemma A.** Let $\beta_1,\dots,\beta_k\in\mathbb F_2^r\setminus\{0\}$ be distinct, $0\le p\le\frac12$, and $X_k=\sum_{l\le k}\varepsilon_l\beta_l$ with $\varepsilon_l$ i.i.d. Bernoulli$(p)$. Then for every $\gamma\neq0$,
$$
\Pr(X_k=\gamma)\ \le\ \frac{1-(1-2p)^{(k+1)/2}}{k+1}\ \le\ \min\Big\{p,\ \frac1{k+1}\Big\}.
$$

*Proof.*
1. **Setup.** Fix $\gamma\neq0$ and put $F(p)=\Pr_p(X_k=\gamma)$. This is a polynomial with $F(0)=0$. By Lemma W, with $q=1-2p$ and $n(x)=N_k(x)$,
   $$
   F(p)=\mathbb E_x\big[\chi_\gamma(x)\,q^{n(x)}\big].
   $$
2. **Distinct points.** The $k+1$ points $\gamma,\gamma+\beta_1,\dots,\gamma+\beta_k$ are distinct, because the $\beta_l$ are distinct and nonzero. So their probabilities sum to at most 1:
   $$
   S(p):=\Pr(X_k=\gamma)+\sum_l\Pr(X_k=\gamma+\beta_l)\le1 .
   $$
3. **Identity for $S$.** Since $\chi_{\gamma+\beta_l}=\chi_\gamma\chi_{\beta_l}$ and $\sum_l\chi_{\beta_l}(x)=k-2n(x)$,
   $$
   S=\mathbb E_x\big[\chi_\gamma q^{n}(k+1-2n)\big].
   $$
4. **Derivative.** Differentiating step 1 gives $(1-2p)F'(p)=-2\,\mathbb E_x[\chi_\gamma\,n\,q^n]$. Hence
   $$
   (1-2p)F'(p)+(k+1)F(p)=S(p)\le1 .
   $$
5. **Integration.** It follows that
   $$
   \frac{d}{dp}\Big[(1-2p)^{-(k+1)/2}F\Big]=(1-2p)^{-(k+3)/2}\big[(1-2p)F'+(k+1)F\big]\le(1-2p)^{-(k+3)/2}.
   $$
   Integrating from 0 to $p<\frac12$, with $F(0)=0$,
   $$
   (1-2p)^{-(k+1)/2}F(p)\le\frac{(1-2p)^{-(k+1)/2}-1}{k+1}.
   $$
   The case $p=\frac12$ follows by continuity.
6. **Last inequality.** It uses $1-(1-2p)^{m}\le2pm$ with $m=(k+1)/2$. ∎

**Equality case.** At $p=\frac12$, $X_k$ is uniform on the span of the $\beta_l$. If the $\beta_l$ are all nonzero vectors of a $j$-dimensional subspace ($k=2^j-1$), then $\Pr(X_k=\gamma)=2^{-j}=1/(k+1)$.

**Numerical check (S3).** The ratio of the left side to the right side has maximum exactly $1.000000$. This covers an exhaustive search over all step sets for $r\le4$ at six values of $p$, and 1500 random sets for $r=5..9$ (all prefixes). The power-of-two strengthening $\Pr\le2^{-\lceil\log_2(k+1)\rceil}$ is **false** for $p<\frac12$; for example, the ratio is 1.41 at $k=8,\ p=.25$ (`anticonc.out`).

## 5. Theorem U* (uniform bound for all distinct labels)

**Theorem U*.** In the scope of §1, for all $R$, all distinct nonzero labels (dependent or not), all $0<a,g_H\le1$, $0<b\le g_H/2$, and all inter-capture gaps and resets:
$$
\|PA_{\rm cap}\|\le2,\qquad \|U_{\rm prot}\|\le2\sqrt{1+(ag_H)^2}\le2\sqrt2 .
$$
Moreover,
$$
\|U_{\rm prot}\|^2\le\big(1+(ag_H)^2\big)\min\{4,\ pR\},\qquad p=b/g_H .
$$

*Proof.*
1. **Hardy kernel bound.** By (1.1), (1.2), (2.1) and (3.1), $0\le\Gamma\le K$ entrywise, with $K(j,k)=1/(\max(j,k)+1)$. For nonnegative symmetric matrices, entrywise domination gives domination of the operator norm: $|\langle v,\Gamma w\rangle|\le\langle|v|,K|w|\rangle$.
2. **Comparison with the Hardy operator.** Since $1/m^2\ge\int_m^{m+1}x^{-2}dx$,
   $$
   K(j,k)\le\sum_{m>\max(j,k)}m^{-2}=(H^TH)(j,k),\qquad (Hw)_m=\frac1m\sum_{j<m}w_j .
   $$
   The discrete Hardy inequality (Hardy 1920, constant $(\frac{p}{p-1})^p=4$ at $p=2$) gives $\|H\|\le2$. So $\|\Gamma\|\le\|K\|\le4$ and $\|PA_{\rm cap}\|\le2$.
3. **Refinement.** Lemma A gives $\Gamma(j,k)\le\min\{M_j,M_k\}\le p$. A Schur row-sum bound then gives $\|\Gamma\|\le pR$. Insert both bounds into (1.1). ∎

Numerically, $\|K_R\|=1.51,\,2.37,\,2.88,\,3.05$ at $R=10,10^2,10^3,3\cdot10^3$, increasing slowly toward 4 (S4). Over 400 random legal full-model configurations, $\|U_{\rm prot}\|/[2\sqrt{1+(ag_H)^2}]\le0.27$ (S7). These configurations include dependent labels, $a,g_H<1$, empty and nonempty gaps, and tails.

## 6. Linearly independent labels: the original proof is correct there

Suppose the labels are linearly independent. Then:
- $\hat v_e$ is supported on $\alpha_e+\mathrm{span}\{\alpha_{e'}:e'>e\}$;
- for $f>e$, $\hat v_f$ is supported in $\mathrm{span}\{\alpha_{e'}:e'>e\}$;
- these two sets are disjoint iff $\alpha_e\notin\mathrm{span}\{\alpha_{e'}:e'>e\}$, which is exactly linear independence of the sequence.

So the $v_e$ are orthogonal, with $|v_e|\le1$ pointwise, and $\|V\|\le1$.

**Exact factorization (any labels).** Unrolling $\mathcal M_e\mathbf 1=a\bar g\mathbf 1+ab\chi_e$ gives
$$
\mathrm{cap}_e=\sum_{f\ge e}T(f,e)\,v_f+(\cdots)\mathbf 1,\qquad 0\le T(f,e)\le ab(a\bar g)^{f-e}.
$$
So $PA_{\rm cap}=PVT$, with $\|T\|\le ab/(1-a\bar g)\le1$ by Young's inequality, since $a(\bar g+b)=ag_H\le1$. With (1.1):
$$
\|U_{\rm prot}\|\le\sqrt{1+(ag_H)^2}\;\frac{ab}{1-a\bar g}\le\sqrt2\qquad\text{(independent labels)} .
$$
The original "$\le2$" summed the two triangular blocks. The Gram combination (1.1) gives $\sqrt{1+(ag_H)^2}$ instead.

**Diagnosis of the dependent case.** The factorization $PVT$ remains exact, but $\|V\|$ is no longer $\le1$. It is not uniformly bounded by Gershgorin (§3.3). The repair therefore bypasses $V$ and works with $\Gamma$ directly.

## 7. Lower bounds and legal counterexamples

**Counting family.** Take all $2^r-1$ nonzero labels, ordered in walk order $\beta_l=l$ (binary counting), i.e. time order $\alpha_e=2^r-e$. Walk index $k$ lies in level $j$ iff $2^{j-1}\le k\le2^j-1$. That gives $L_j=2^{j-1}$ indices per level, and $\mathrm{span}(\beta_1..\beta_k)=\mathbb F_2^j\times0$ throughout level $j$.

### 7.1 Proposition L1 (exact supremum at $b=g_H/2$)

At $p=\frac12$, for every $R$ and every sequence of distinct labels, $\|PA_{\rm walk}\|<1+2^{-1/2}$. The counting family attains this as $r\to\infty$. Hence:
- $\|U_{\rm prot}\|<\sqrt{1+(ag_H)^2}\,(1+2^{-1/2})$ always;
- at $ag_H=1$, $\sup_R\|U_{\rm prot}\|=1+\sqrt2$.

For fixed $ag_H<1$ the factors $c_e\le(ag_H)^{R-e+1}$ damp the high levels, so the supremum over $R$ is smaller.

*Proof.*
1. **Exit-time form.** At $p=\frac12$, $u_k=\mathbf 1[T(x)\ge k]$, where $T(x)$ is the first $l$ with $\chi_{\beta_l}(x)=-1$, minus 1. So
   $$
   \sum_kw_ku_k(x)=W(T(x)),\qquad W(t)=\sum_{k\le t}w_k .
   $$
2. **Survival probabilities.** $\Pr_x(T\ge s)=2^{-\mathrm{rank}(\beta_1..\beta_s)}\le d_s:=2^{-\lceil\log_2(s+1)\rceil}$, because $s$ distinct nonzero vectors span at least $s+1$ points.
3. **Second-moment kernel.** Hence
   $$
   \mathrm{Var}\,W(T)\le\mathbb E\,W(T)^2=\sum_{j,k}w_jw_k\Pr(T\ge\max(j,k))\le\langle|w|,K^{\rm cnt}|w|\rangle,\qquad K^{\rm cnt}(j,k)=d_{\max(j,k)} .
   $$
4. **Level grouping.** $K^{\rm cnt}$ is constant on level blocks. Its nonzero spectrum is that of
   $$
   M'(i,i')=\sqrt{L_iL_{i'}}\,2^{-\max(i,i')}=\tfrac12\,2^{-|i-i'|/2},
   $$
   where a partial last block only lowers the entries. This is a finite section of a nonnegative Toeplitz matrix, so its norm is strictly below the symbol maximum
   $$
   \tfrac12\sum_{n\in\mathbb Z}2^{-|n|/2}=(1+2^{-1/2})^2 .
   $$
5. **Lower bound.** For the counting family the protected Gram matrix is exactly
   $$
   \Gamma(j,k)=2^{-i'}(1-2^{-i})\quad(\text{levels }i\le i').
   $$
   Its level-grouped matrix is $M(i,i')=\tfrac12\,2^{-|i-i'|/2}(1-2^{-\min(i,i')})$. Restricting to levels $\ge i_0$ and letting $r\to\infty$, then $i_0\to\infty$, gives $\|M\|\to(1+2^{-1/2})^2$. Finally use equality in (1.1). ∎

Exact values of $\|PA_{\rm cap}\|$ from the level matrix, which agree with the direct site computation for $r\le12$ (S5–S6):

| $r$ | 4 | 8 | 11 | 12 | 20 | 200 | 1000 |
|---|---|---|---|---|---|---|---|
| $\|PA_{\rm cap}\|$ | 1.0035 | 1.3189 | 1.4387 | 1.4670 | 1.5920 | 1.7054 | 1.7070 |

### 7.2 Proposition L2 (every contrast)

For every fixed $p\in(0,\frac12)$,
$$
\liminf_{r\to\infty}\|PA^{(p)}_{\rm walk,\,count}\|\ge1+2^{-1/2}.
$$
Hence, at $ag_H=1$, $\sup_R\|U_{\rm prot}\|\ge1+\sqrt2$ for **every** legal $b$. Each finite witness persists for $ag_H$ close enough to 1.

*Proof.*
1. **Atom decomposition.** For walk index $k$ in level $j\ge2$, put $t=k-2^{j-1}+1\in[1,2^{j-1}]$. Write $x_i=e_i\cdot x$. Then
   $$
   u_k=\mathbf 1_{Z_j}+q^t\mathbf 1_{Y_j}+E_k ,
   $$
   where:
   - $Z_j=\{x_1=\dots=x_j=0\}$ and $Y_j=\{x_1=\dots=x_{j-1}=0,\ x_j=1\}$, each of density $2^{-j}$;
   - $0\le E_k\le q^{2^{j-2}}$, supported on $\{(x_1..x_{j-1})\neq0\}$.

   The reason: at the end of level $j-1$, every $x$ with nonzero low bits has $N=2^{j-2}$. During level $j$, the steps are $e_j+v$ with $v$ running over $\mathbb F_2^{j-1}$.
2. **Comparison with $p=\frac12$.** $\mathbf 1_{Z_j}$ is exactly the $p=\frac12$ atom. For $w$ supported on levels $[i_0,r]$, Cauchy–Schwarz gives
   $$
   \|PA^{(p)}w\|\ \ge\ \|M_{[i_0,r]}\|^{1/2}\|w\|-\eta\|w\|,\qquad \eta^2=2\sum_{j=i_0}^{r}\Big[\frac{2^{-j}q^2}{1-q^2}+2^{j-1}q^{2^{j-1}}\Big].
   $$
   Here $w$ is the Perron vector of $M_{[i_0,r]}$, spread evenly in each level.
3. **Limit.** $\eta\to0$ as $i_0\to\infty$, for fixed $q<1$. Apply 7.1. ∎

**Certified instances** (`certify_lb.py`, $a=g_H=1$): $\|U_{\rm prot}\|\ge\sqrt2\,(\|M_{[i_0,r]}\|^{1/2}-\eta)>2$ at:

| $b$ | $r$ | $i_0$ | bound |
|---|---|---|---|
| .2 | 19 | 9 | 2.020 |
| .05 | 22 | 12 | 2.023 |
| .0025 | 26 | 16 | 2.004 |

These are rigorous given the proof; the estimate is crude.

### 7.3 Legal witnesses

All witnesses use the counting family with $a=g_H=1$ and at least one ordinary step between captures.

**Exact $\|U_{\rm prot}\|$, full model with both atom types (S5, `counting_scan.out`, `big.out`):**

| $b$ | $R=2^{11}-1$ | $2^{12}-1$ | $2^{13}-1$ | $2^{14}-1$ | $2^{15}-1$ |
|---|---|---|---|---|---|
| .5 | **2.0346** | **2.0746** | | | |
| .4 | | **2.0703** | | | |
| .2 | | **2.0485** | | | |
| .05 | | 1.9685 | **2.0203** | **2.0637** | |
| .0025 | | 1.5636 | | 1.8079 | 1.8902 |

- Setting $a=1-10^{-9}$ leaves the $b=.2$, $R=4095$ value at 2.0485 to four decimals.
- **Streaming lower bounds** at $b=.0025$ (`stream_lb.py`, `stream_lb2.out`; any test vector gives a valid lower bound): $\|U_{\rm prot}\|\ge1.9319$ at $R=2^{16}-1$ and $\ge1.9854$ at $R=2^{17}-1$. These are still increasing; the numerical crossing of 2 is expected near $R\approx2^{18}$.
- **Certified** (§7.2): $>2$ at $R=2^{26}-1$.

**Legality.**
- Labels are distinct nonzero Walsh characters on $2^r$ equal survivor classes, which needs $h_S\ge2^r$. Nothing in the Theorem B scope or in Astra's assumptions forbids linear dependence.
- Gates are $g_H=1$ and $1-2b\in[0,1)$. Interior gates are used for $b<\frac12$.
- $ag_H$ can be taken $=1$ or $\to1$. Astra's family requires only $1-ag_H\le10^{-4}p_S$ and $a,g_H\ge.99999$, so the decays $(ag_H)^\Delta$ over its $\ge100/p_S$ spacing can be made $\to1$ at fixed $R$.
- The only "cost" is a large $R$. Lemma U claimed uniformity in $R$, and Route 6 has $R\to\infty$.
- In the realistic Route-6 range ($R=O(\log\log n)$ and $b\approx.0025$), the refinement $\|U_{\rm prot}\|^2\le2pR$ of Theorem U* is far below 1.

### 7.4 Is counting order extremal?

Adversarial search finds nothing better than counting order (S8, `adversarial.out`):
- exhaustive over all $7!$ orders at $r=3$;
- swap local search with restarts at $r=4,5$;
- each for $p\in\{.5,.3,.1\}$.

**Conjecture S.** $\sup\|PA_{\rm cap}\|=1+2^{-1/2}$ for every $p\in(0,\frac12]$, with the supremum over $R$, labels and $ag_H\le1$. Equivalently, the sharp uniform Lemma U constant is $1+\sqrt2$ at every contrast.

## 8. Theorem B-F after repair (item 4)

Apply Theorem F with $U=B\,U_{\rm prot}$, keeping the archived normalization $\|B\|_{\rm op}\le1$ and the reader-support premise G2. Then:
$$
\boxed{\;D-q\le\Big\lfloor\big(1+(ag_H)^2\big)\min\{4,(b/g_H)R\}\Big(\frac{\Lambda}{s}\Big)^2\Big\rfloor\le\Big\lfloor8\Big(\frac{\Lambda}{s}\Big)^2\Big\rfloor\;}
$$
For linearly independent labels the bound is $D-q\le\lfloor2(\Lambda/s)^2\rfloor$.

- **Limit of the method.** By §7, no bound of the form $D-q\le c\,(\Lambda/s)^2$ obtained through $\|U_{\rm prot}\|$ can have $c<(1+\sqrt2)^2\approx5.83$. This applies uniformly over general labels with $ag_H$ allowed arbitrarily close to 1.
- **Route-6 corollary.** Take $\Lambda\le4\sqrt KN$ (Astra, PENDING REVIEW, scope: separated captures) and $s=9.5\cdot10^{-5}n/\sqrt m$. Then $(\Lambda/s)^2=1.773\cdot10^9KN^2m/n^2$ and
  $$
  D-q\le1.42\cdot10^{10}\,\frac{KN^2m}{n^2}=O\Big(C_T^2\frac nR\Big)=o(n),
  $$
  replacing $7.1\cdot10^9$. The conclusion is unchanged: linear $D$ still forces $C_T\gtrsim\sqrt R$, i.e. $mT\gtrsim n^{3/2}$.
- **Conditions.** The corollary is conditional, exactly as before, on:
  - Astra's mass bound, with matching scope;
  - the checkpoints ($7.213$, $\eta<.001$, $q_{\rm stat}$);
  - moving-cycle exhaustion ($q_{\rm cyc}$);
  - G2 and $\|B\|\le1$.

## 9. Theorem F is preserved (item 5)

Theorem F ($D\le q+\lfloor(\|U\|_{2\to2}\Lambda/s)^2\rfloor$ for any fixed linear $U$) and its ingredients do not use Lemma U. Gemini's audit marks them VERIFIED. The ingredients are:
- Lemma F;
- the zero-set index fact (I2);
- the inequality $\|Z\|_2^2\le\|Z\|_1\|Z\|_\infty$.

This repair changes only the numerical value of $\|U\|$ fed into Theorem F.

## 10. Remaining obligations

1. **Independent review** of:
   - Lemma A (new, load-bearing): the $k+1$ distinct points and the derivative identity;
   - the Hardy domination step;
   - Lemma W;
   - the atom map (1.1)–(1.2), including the $a$-convention at capture steps.
2. **Sharp constant for $0<b<g_H/2$** (Conjecture S). If true, Theorem B-F holds with $(1+\sqrt2)^2$ in place of 8.
3. **Inherited premises:**
   - $\|B\|_{\rm op}\le1$ and reader support G2;
   - one-step captures only (multi-step masks are not covered);
   - the upstream $\Lambda$, $s$, $q$ inputs and the scope match between Astra's separated family and the one-step-capture scope.
4. **Cross-reference.** The Route 7B file carries a pointer note to this repair. Its §3.4 text is otherwise preserved as originally written.

## 11. Files

| File | Content |
|---|---|
| `PROOF.md` | This derivation. |
| `REVIEW_HANDOFF.md` | Claims to verify, in order of risk. |
| `RESEARCH_LOG.md` | Exploration record, including failed attempts and the power-of-two counterexample. |
| `lemma_u_repair_checks.py` / `.out` | Sections S1–S8. About 8 minutes on CPU. |
| `big.py` / `big.out` | Exact Lanczos norms for $R$ up to $2^{15}-1$ (cached float32 atoms). |
| `stream_lb.py` / `stream_lb.out` / `stream_lb2.out` | Streaming Rayleigh lower bounds at $b=.0025$ ($R$ up to $2^{17}-1$). |
| `certify_lb.py` / `.out` | Certified instances from Proposition L2. |
| `core.py`, `counting_scan.py` / `.out` | Counting order vs independent labels for $b\in\{.4,.2,.05,.0025\}$ and $r\le12$. |
| `anticonc.py` / `.out` | Exhaustive test ($r\le4$) of the power-of-two anti-concentration bound (false) against $1/(k+1)$ (holds). |
| `adversarial.py` / `.out` | Ordering search; counting order is never beaten (§7.4). |
| `stream_lb_calib.out` | Calibration of the streaming test vector against exact values. |
