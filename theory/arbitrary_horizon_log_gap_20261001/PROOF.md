# Arbitrary-horizon log gap: lookback necessity versus credit storage

2026-10-01. Theory only. New lemmas below require independent review.
The independently verified quadratic lower bound is a premise, not reproved.
The worst-case arbitrary-horizon logarithmic gap is NOT closed by this note.

## 1. Question, quantifiers and unchanged contract

Fix c>0, epsilon=1/1000 and sufficiently large n. Put

    gamma=c/n, a=1-gamma, P=2n^2+n.

The actual predictor is always

    h_t=tanh(R h_(t-1)+W x_t+b), h0=0.

Parameters are frozen; every R/W/b entry is independently differentiated.
Inputs lie in (-1/2,1/2)^n. Assume ||R||op<=a, ||W||op<=w and
RMS(b)<=b_* with width-independent w,b_*. Define Z=S D_theta with the
accepted FROZEN group-RMS scales

    w_R=||R||F/n, w_W=||W||F/n, w_b=RMS(b).

These weights are not differentiated. The accepted late scalar head is
q=1/sqrt(n)*1, divided by beta=max(1,||R||F). At a supplied endpoint h,
an allowed continuation has effective adjoint c_q with

    ||c_q||<=kappa_Q=a/beta.

For one future step, c_q=R^T G_f q/beta. Multiple future steps contract
further. Actual answers include the direct future parameter injections;
only the history-dependent part Z^T c_q is approximated below. All histories
being compared have the same endpoint, so their future direct terms agree.
No arbitrary immediate adjoints, new loss, new units or different epsilon
are introduced.

A sufficient encoder is a continuous, finite-dimensional, counted online
state with no unaccounted history tape or discarded-history replay. Decoder
work is unrestricted. Model constants are public. Supplying exact h removes
its n coordinates from the credit count; storing it adds n. The question is
the worst case over ALL admissible dense models and ALL history lengths.
A particular model's sufficient encoder is not a worst-case class upper.

The accepted bounds are

    Omega_c(n^2) <= d_rob(n,epsilon) <= O_c(n^2 log n).

At the constructed O_c(n) horizon, counted exact state/input storage already
matches the quadratic lower. Only the arbitrary-horizon gap is open.

## 2. Exact injection and the existing window bound

Write

    G_t=diag(1-h_t^2), A_t=G_t R,
    B_t phi=G_t(w_R phi_R h_(t-1)+w_W phi_W x_t+w_b phi_b).

Disjoint parameter rows give

    B_t B_t^T=G_t^2 [w_R^2 ||h_(t-1)||^2
                    +w_W^2 ||x_t||^2+w_b^2].

Consequently ||B_t||op<=C, where

    C=sqrt(a^2+w^2/4+b_*^2).

The actual normalized sensitivity obeys Z_t=A_t Z_(t-1)+B_t, Z0=0.
Thus ||Z_t||op<=C/gamma and dropping injections older than H gives uniform
late-query error at most

    e_H=kappa_Q C a^H/gamma.

The accepted 2Hn counted recent-state/input store uses

    H=ceil_+( log(kappa_Q C/(epsilon gamma))/[-log a] ).

This proves the general upper. It does not prove a memory lower. Sections
3-5 show that a logarithmic LOOKBACK requirement is nevertheless real for
literal suffix-only summaries, even when a different quadratic summary works.

## 3. A dense family with a genuine long credit tail

Set k=floor(n/2), l=n-k, delta=1/(100n), and

    R0=diag(a I_k, delta I_l), W=I, b=(1/20)*1,
    q=(1/sqrt(n))*1, eta=1/(10^8 n^2),
    B=R0+eta q q^T, R=(a/||B||op) B.

For sufficiently large n, delta<a and eta<a/2. B is positive definite.
Every off-diagonal entry is eta/n>0, and every diagonal entry is positive.
Sherman-Morrison, with d_i=(R0)_(ii), gives

    (B^-1)_(ij)=-(eta/n)/(d_i d_j [1+(eta/n)sum_p 1/d_p]), i!=j,

and

    (B^-1)_(ii)=(1/d_i)
       [1+(eta/n)sum_(p!=i)1/d_p]/[1+(eta/n)sum_p1/d_p]>0.

Thus R and R^-1 have no zero entries. W is invertible. All entries are still
independently differentiated; the base-value formula does not tie parameters.
The actual operator norm is EXACTLY a. Since a<=||B||op<=a+eta,

    e_R=||R-R0||op<=2eta<=4/(10^8 n^2).                 (1)

Both beta values equal their Frobenius norms once n is large enough. In
particular w_R/beta=1/n EXACTLY. The model is dense in the accepted sense,
but is close to diagonal; no typical-model claim is made.

## 4. Two histories with identical last H steps

Let sigma=2/5, J=ceil(1/gamma), and H be any nonnegative integer. Prescribe
two trajectories with sign s in {-1,+1}:

    h_t^s=(0_k,s sigma 1_l), t=1,...,J;
    h_t^s=0, t=J+1,...,J+1+H; h0=0.

For the actual fixed R realize each trajectory using

    x_t^s=atanh(h_t^s)-R h_(t-1)^s-b.                 (2)

Inputs are held FIXED for sensitivity differentiation, not differentiated
through this compensator. At R0 the source input bound is
atanh(2/5)+delta(2/5)+1/20<0.477. The perturbation changes any input coordinate
by at most e_R sigma sqrt(l)<0.001 for sufficiently large n. The trajectories
therefore remain inside the original input cube jointly.

The reset input at t=J+1 may differ between signs. It is OUTSIDE the last H
transitions. At T=J+1+H the supplied h_T=0 is common, and EVERY retained item

    h_(T-H),...,h_(T-1), x_(T-H+1),...,x_T

is identical: states are zero, inputs are -b. This explicitly avoids leaking
the old sign through the first retained reset transition. The argument also
works at H=0, when there is no retained suffix.

Use the allowed future input v=(9/20)*1. Its preactivation is (1/2)*1 at
h_T=0 for both models, so G_f=kappa I with kappa=sech^2(1/2)>3/4.
The direct future R injection is zero. The other direct terms cancel.

At R0, memory gates are exactly one and source coordinates do not feed the
reference memory dynamics. The ACTUAL R memory-row/source-column injection
is deltaR_ms h_source. Its normalized queried gradient is

    g_ms^s=(s kappa sigma/n)
          a^(H+1)(1-a^J)/gamma * q_m 1_l^T,
    q_m=(1/sqrt(n))*1_k.

This follows by summing the J injections at transitions t+1. The exponent
including the one-step future query is J+H+1-t; summing t=1,...,J gives
a^(H+1)(1-a^J)/gamma. No parameter columns are independently controlled.
Since J>=1/gamma, 1-a^J>=1-exp(-1)>1/2. Also sqrt(k l)/n>=1/3 for n>=2.
The reference boundary half-separation is therefore

    m_ref(H)=(kappa sigma/n) sqrt(k/n) sqrt(l)
                a^(H+1)(1-a^J)/gamma
            >= sqrt(n)/(20c) * a^(H+1).                (3)

The exact gates and prescribed states in (2) agree between R0 and R even
though their realizing inputs differ. Only the R block is used in (3), so
input differences do not enter its injection. For either model its full
normalized R-gradient is

    g_R=(kappa/n)sum_(t=1)^T
           [G_t A_(t+1)^T ... A_T^T R^T q] h_(t-1)^T.

Every recurrent factor has norm at most a, every gate at most one. A product
of p recurrent factors changes by at most p a^(p-1)e_R. The nonzero past
states have norm sigma sqrt(l). Bounding their ages by the full geometric
derivative series yields, independently of J,H,T,

    ||g_R(R;s)-g_R(R0;s)||F
       <=(kappa sigma sqrt(l)/n) e_R sum_(p>=1)p a^(p-1)
       <=E_n:=4 sigma/(10^8 c^2 sqrt(n)).              (4)

Equation (4) retains the future R factor and all source gates. Projecting
to the selected block and comparing both histories proves

    m_dense(H)>=sqrt(n)/(20c) a^(H+1)-E_n.             (5)

## 5. Theorem: logarithmic lookback is necessary for suffix-only summaries

A suffix-only summary is ANY function of the supplied current h and the
last H state/input transitions above, together with fixed model/horizon
constants. It does not carry a history-dependent accumulator from before
the retained suffix. Its dimension and decoder are otherwise unrestricted;
this theorem does not even need continuity.

The two histories in section 4 give exactly the same summary. Uniform query
error <=epsilon forces their exact query separation <=2epsilon. By (5),
such a summary can succeed only if

    a^(H+1)<=20c(epsilon+E_n)/sqrt(n).

For n large enough that the right side is below one, necessarily

    H >= log(sqrt(n)/[20c(epsilon+E_n)])/[-log(1-c/n)] - 1
      >= (n/(2c)) log n - O_(c,epsilon)(n).            (6)

Therefore the log n is NOT solely an artifact of the old scalar geometric
majorant: a real normalized gradient tail requires that lookback depth on
an admissible fully dense model.

CRITICAL LIMITATION: (6) is a lower bound on LOOKBACK LENGTH, NOT on the
number of continuous coordinates of an arbitrary encoder. Even an encoder
of a long suffix might compress it. An accumulator can retain old credit
without retaining old inputs. The literal 2Hn uncompressed buffer pays
O(n^2 log n), but (6) does NOT establish Omega(n^2 log n) credit dimension.
The particular separating tail above is highly coherent, not a joint
n^2 log n-dimensional robust section.

## 6. General perturbation-to-structured-propagation lemma

Consider any actual permitted model and any public reference R_bar with
||R_bar||op<=a. Use the ACTUAL forward states, gates, inputs and normalized
injections, but propagate surrogate sensitivity by

    Z_bar_t=G_t R_bar Z_bar_(t-1)+B_t, Z_bar0=0.        (7)

This does not change the forward predictor or parameter definitions.
Z_bar is an approximation, not claimed to be its exact parameter derivative.
If e=||R-R_bar||op, then

    ||Z_bar_t||op<=C/gamma,
    Delta_t=A_t Delta_(t-1)+G_t(R-R_bar)Z_bar_(t-1),
    ||Z_t-Z_bar_t||op<=e C/gamma^2                     (8)

for EVERY horizon and EVERY allowed history. The final step sums
e C/gamma times sum_(j>=0)a^j. Thus answering with the surrogate VJP has
uniform late-query error at most

    kappa_Q e C/gamma^2.                              (9)

All actual future direct injections are computed from actual h and the
permitted continuation. They are not replaced by reference-model injections.
For multi-step continuations the same bound applies because ||c_q||<=kappa_Q.
The lemma only needs a compact realization of (7); closeness alone is not
an encoder until ALL derivative buffers in that realization are counted.

## 7. Arbitrary-horizon quadratic encoder for the family in section 3

Take R_bar=R0, which is diagonal. Because both G_t and R0 are diagonal,
Z_bar has support only on the parameters in the corresponding state row.
For each i store

    E_i^R in R^n, E_i^W in R^n, E_i^b in R.

With d_i=(R0)_(ii), actual g_i,t=1-h_i,t^2, update

    E_i^R <- g_i,t (d_i E_i^R+w_R h_(t-1)),
    E_i^W <- g_i,t (d_i E_i^W+w_W x_t),
    E_i^b <- g_i,t (d_i E_i^b+w_b).

Initialize these arrays at zero. Place each array in the corresponding
parameter-row columns of row i of Z_bar. This realizes (7) EXACTLY with

    n(2n+1)=P=2n^2+n

persistent credit coordinates. It is continuous and streams all inputs;
there is no history tape, recent buffer, replay or uncounted factor. Store
n actual forward coordinates too when h is not supplied. At query time the
decoder uses the ACTUAL future adjoint c_q and actual future direct terms.

This encoder works for ALL allowed histories of the dense family in section
3, not only its special zero-memory trajectories. All actual dense parameters
remain independently differentiated; omitted cross-state derivative terms
are covered by (8), rather than incorrectly claimed to be zero.

Here C<6/5. Also beta>=a sqrt(k)/2 once n is sufficiently large, since

    ||R||F>=||R0||F-sqrt(n)e_R>=a sqrt(k)-sqrt(n)e_R.

Hence kappa_Q<=2/sqrt(k). Combining (1), (9) and gamma=c/n gives

    query error <=48/[5*10^8 c^2 sqrt(k)],             (10)

which is <epsilon for every fixed c and sufficiently large n. This proves
an arbitrary-horizon O(n^2) continuous sufficient encoder for THIS dense
family, including the histories that force logarithmic lookback in (6).
No change of epsilon or normalized query contract is made.

More generally, for a near-diagonal actual model the same P-coordinate
encoder succeeds whenever

    ||R-R_bar||op<=epsilon gamma^2/(kappa_Q C).

When beta=Theta(sqrt(n)) and gamma=c/n this allows an O_(c,epsilon)(n^-3/2)
norm neighborhood. This is a sufficient neighborhood, not a characterization
of every model admitting quadratic compression. Reference values are public;
all history-dependent derivative arrays are counted. These are ordinary
eligibility traces, not an invented architecture.

## 8. Why this does not close the requested worst-case gap

The new results distinguish two propositions that the window proof conflates:

1. Uniform last-H-only truncation needs H=Omega_c(n log n) on some dense
   models under the exact accepted normalization. This is now derived.
2. Those same models can need only O(n^2) counted continuous state when old
   credit is AGGREGATED, rather than forgotten. This is also now derived.

Neither establishes an arbitrary-horizon O(n^2) encoder for ALL dense R.
An arbitrary dense R need not be within the neighborhood required by (9).
With e=Theta(1), gamma=c/n and beta=Theta(sqrt(n)), its bound is of order
n^(3/2), far above epsilon. Dropping the cross-state sensitivities would
therefore be unjustified.

Nor does (6) prove Omega(n^2 log n): two distinguishable histories do not
produce a high-dimensional jointly robust section. In the accepted rotating
quadratic construction, repeated constant-gate orbit periods aggregate into
the same O(n^2) block, so assigning independent coordinates to each age band
would be incorrect. One fixed query returns only P numbers; to establish a
larger robust lower one must use the full query family correctly, jointly.

A fixed R obeys Cayley-Hamilton, but the actual propagation uses products

    G_T R G_(T-1) R ... G_s.

Arbitrary history-dependent diagonal gates need not commute with R or each
other after conjugation. A basis for powers of R alone does not compress
these products. Conversely, showing that their algebra spans all n by n
matrices does not prove robust sensitivity dimension: trajectory-dependent
injections, late-query normalization and joint finite margins still matter.

The worst-case bounds after this task remain

    Omega_c(n^2) <= d_rob <= O_c(n^2 log n).

At a prescribed T=O_c(n), the existing counted exact 2Tn encoding and the
accepted section give the already-established Theta_c(n^2) horizon-specific
result. No extension from that horizon to all horizons is asserted.

## 9. Precisely what would settle the remaining gap

The upper direction needs a uniform, continuous online aggregation theorem
for the actual gated dense sensitivity recursion: O_(c,epsilon)(n^2)
counted coordinates must give late-query error <=epsilon for every bounded
history and every admissible R, without the near-diagonal hypothesis in (9).
A terminal low-rank factorization alone is insufficient: its factors, online
update buffers and continuity must all be counted and justified.

The lower direction needs an explicit r=Omega_c(n^2 log n) continuous
fixed-h history section with boundary query half-margin >epsilon uniformly
in n. Merely requiring history length n log n, an exact full-rank endpoint,
or a large coherent old tail will not supply that theorem.

Single recommended next step: attack a uniform structured-tail aggregation
lemma for noncommuting G_t R products under the same normalized query norm.
The near-diagonal theorem above is its resolved boundary case, not a proof
that the general lemma is true. Do not move to another contraction regime.

## 10. Status, checks and resources

These are author-derived mathematical lemmas, not independently reviewed or
machine-verified. Derivation checks explicitly include: exact inverse and
gap, the reset transition being excluded from the common suffix, the extra
future R factor in the age exponent, frozen w_R/beta cancellation, the
uniform geometric DERIVATIVE series in (4), the surrogate support count,
and actual future direct injections in (9).

No new numerical experiment, training, witness search, automated test,
GPU/CUDA workload or architecture work was run. The task's uncertainty is
mathematical, so no compute was spent repeating certificates. Experiment
CPU/GPU usage is zero; document/shell overhead and process RAM were not
profiled. Old evidence, AGENTS.md, GAS-0 and other notebooks are untouched.
No finite-bit, practical VRAM, runtime, learning or novelty claim follows.
