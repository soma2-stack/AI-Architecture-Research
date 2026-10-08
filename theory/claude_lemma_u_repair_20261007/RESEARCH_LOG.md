# Research log: Lemma U repair

Author: Claude Opus 5.5. Date: 2026-10-07. This records how the result was found, including attempts that failed. Proof-level statements are in [PROOF.md](PROOF.md). Numbers below come from scripts in this folder or from scratch probes reproduced verbatim.

## 1. Reformulation

The capture multipliers are pointwise and commute. Their product $\prod_{l\le k}((1-p)+p\chi_{\beta_l})$ has Walsh coefficients equal to the law of a lazy walk with steps $\beta_l$ and step probability $p=b/g_H$. The protected Gram matrix is therefore
$$\Gamma(j,k)=\sum_{\gamma\neq0}\pi_j(\gamma)\pi_k(\gamma)\ge0 .$$

Ordinary interval atoms are $ag_H$ times capture atoms (archived Lemma 2). Hence $\|U_{\rm prot}\|=\sqrt{1+(ag_H)^2}\,\|PA_{\rm cap}\|$ when all intervals are nonempty.

## 2. First counterexample ($b=g_H/2$)

At $p=\frac12$ the atoms are subgroup indicators. Dependent labels leave the span unchanged, so atoms repeat. A level of span dimension $j$ can repeat $2^{j-1}$ times at density $2^{-j}$. Binary counting order saturates every level.

Direct computation, $a=g_H=1$:

| $r$ | 2 | 4 | 6 | 8 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|
| $\|U_{\rm prot}\|$ | 1.0000 | 1.4192 | 1.6874 | 1.8652 | 1.9876 | **2.0346** | **2.0746** |

## 3. Smaller contrasts, counting order (`counting_scan.out`, $a=g_H=1$)

Values are $\|U_{\rm prot}\|$; the independent case uses $R=r$.

| $b$ | label set | $r=4$ | $r=6$ | $r=8$ | $r=10$ | $r=12$ |
|---|---|---|---|---|---|---|
| .4 | counting | 1.3776 | 1.6685 | 1.8548 | 1.9811 | **2.0703** |
| .4 | independent | .8003 | .8184 | .8211 | .8215 | .8216 |
| .2 | counting | 1.1721 | 1.5766 | 1.8035 | 1.9488 | **2.0485** |
| .2 | independent | .5444 | .6193 | .6554 | .6721 | .6794 |
| .05 | counting | .5393 | 1.1820 | 1.6044 | 1.8285 | 1.9685 |
| .05 | independent | .1831 | .2464 | .3009 | .3479 | .3882 |
| .0025 | counting | .0344 | .1348 | .4582 | 1.0859 | 1.5636 |
| .0025 | independent | .0101 | .0145 | .0189 | .0233 | .0276 |

Larger instances:
- `big.out`: $b=.05$ crosses 2 at $R=8191$ (2.0203) and reaches 2.0637 at $R=16383$. At $b=.0025$ the values are 1.8079 at $R=16383$ and 1.8902 at $R=32767$.
- `stream_lb*.out` lower bounds at $b=.0025$ are listed in §6.

## 4. Upper-bound attempts

1. **$p=\frac12$ via a weighted Hardy inequality (success).** The atoms are exit-time indicators, so
   $$\mathrm{Var}\,W(T)\le4\sup_s s\Pr(T\ge s)\,\|w\|^2,$$
   and $\Pr(T\ge s)\le1/(s+1)$. This gives $\le2$ for $\|PA_{\rm cap}\|$.

   The sharp value $1+2^{-1/2}$ comes from the second-moment kernel. That kernel is entrywise monotone in survival probabilities, and counting order maximizes every survival probability simultaneously.
2. **General $p$ via thinning (failed).** Bernoulli$(p)$ equals Bernoulli$(2p)$ times Bernoulli$(\frac12)$. For each fixed thinning the rows repeat about $1/(2p)$ times. Jensen then loses a factor $\sim1/p$, because the uncentered survival probability is close to 1 for $s\lesssim1/p$.
3. **General $p$ via the jump index (failed).** Write $q^{N}=\mathbb E_\nu\mathbf 1[N<\nu]$ with geometric $\nu$, and apply Minkowski over $\nu$. Each layer costs $O(\sqrt n)$, so the total loses $\sim p^{-1/2}$.
4. **Entrywise domination by the counting kernel (failed).** This would need the power-of-two anti-concentration bound $M_k\le2^{-\lceil\log_2(k+1)\rceil}$, which is false for $p<\frac12$ (`anticonc.out`, exhaustive for $r\le4$). The worst ratio is 1.4062 at $k=8$, $p=.25$. The weaker bound $(k+1)M_k\le1$ held in every case: max 1.0000, attained only at $p=\frac12$ on full subspaces.
5. **Lemma A (success).** Distinct steps make $\gamma,\gamma+\beta_1,\dots,\gamma+\beta_k$ distinct. The resulting sum identity is the differential inequality $(1-2p)F'+(k+1)F\le1$. With $F(0)=0$ this integrates to $F\le(1-(1-2p)^{(k+1)/2})/(k+1)$. Then $\Gamma(j,k)\le1/(\max(j,k)+1)$, and the discrete Hardy constant 4 gives Theorem U*.

## 5. Extremality probes (`adversarial.out`, $\|PA_{\rm cap}\|$, $a=g_H=1$)

| $r$ | search | $p=.5$ | $p=.3$ | $p=.1$ |
|---|---|---|---|---|
| 3 | exhaustive over $7!$ orders | .87232 | .74347 | .37906 |
| 4 | swap local search, 6 restarts | 1.00352 | .92460 | .60625 |
| 5 | swap local search, 6 restarts | 1.10845 | 1.05709 | .83323 |

Counting order attains every maximum found. Appending unused labels never lowers the norm, so full permutations suffice. The norm is $GL_r(\mathbb F_2)$-invariant.

## 6. $b=.0025$ (Astra's contrast)

Proposition L2 gives the limit $\ge1+2^{-1/2}$ for every $p>0$. Rigorous evidence:
- the streaming Rayleigh lower bounds ($\|U_{\rm prot}\|\ge1.9319$ at $R=2^{16}-1$ and $\ge1.9854$ at $R=2^{17}-1$, `stream_lb2.out`);
- the certified bound $>2$ at $R=2^{26}-1$ (`certify_lb.out`).

The calibration below shows that the test vector is close to optimal; $b=.0025$ throughout.

| $R$ | $i_0$ | Rayleigh bound on $\|PA_{\rm cap}\|$ | exact (Lanczos) |
|---|---|---|---|
| 16383 | 9 | 1.2537 | 1.2784 |
| 32767 | 9 | 1.3160 | 1.3366 |
