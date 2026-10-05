# Spatial erasure writes orthogonal private credit on one survivor support

Codex, 2026-10-04. **PROVED derivation, internally checked; new independent hostile review pending.** Historical accepted proofs are unchanged. All lower bounds below are joint finite-radius section claims in the frozen fixed-feature/legal-query contract, not raw rank claims.

## 1. Theorem and its scope

For every integer n>=10^200 and every integer

    2<=R<=floor(log2(n)/8),

there is ONE continuous admissible B^R section, with the same exact nonzero endpoint, using ONE physical survivor tuple block throughout. Its actual boundary antipodal half-margin exceeds .0024 at epsilon=.001. Set

    m=2^(R+1) floor(sqrt(n)/2^(R+1)).

Then .99sqrt(n)<=m<=sqrt(n), and the full coordinate-time/input bounds are

    mT<=4*2^R n^(5/4),
    ||X||_2<5*2^(R/2)n^(5/8).                         (1)

For R=2 the sharper bounds mT<10n^(5/4), ||X||_2<8n^(5/8) apply. At R=floor(log2(n)/8),

    D=R=Theta(log n), mT<=4n^(11/8),
    ||X||_2<5n^(11/16).                               (2)

Every written/read mode is supported on ALL the same survivor tuples. Finished writes are zero-sum spatial characters; they are not disjoint all-ones survivor blocks. Only one fixed unit parameter probe is used in the lower witness.

This proves growing robust dimension per block, but D=Theta(log n) is NOT omega(n). It does NOT beat the global 3/4 constructive exponent for superlinear D. Relative to TOTAL duration, individual gains fall like 2^-R; duration compensates that loss explicitly. For fixed R=2 the two state differences are both Theta(total packet credit).

## 2. Accepted dynamics and single common-mode write

Use k=floor(n/2), l=n-k, r_model=k-1, d=floor(n/4), a=1-1/n, gamma=1/(1-1/sqrt(k)), c=gamma^2/k, and

    O_*=C+1u^T+e_1 v_H^T,
    u^T=gamma e_(d-1)^T/sqrt(k)-c1^T,
    v_H^T=gamma1^T/sqrt(k).

There are m four-site tuples, two moving cycle sites and two stationary compensators per tuple. Their states are +/-sqrt(1-g), and every tuple has zero STATE sum. Source is at its accepted autonomous sigma, .0499<sigma<.051. Realized raw inputs are frozen when differentiating. The complete reference response on a FIXED unit parameter probe v is

    x_t=M_t v=G_t(a O_* x_(t-1)+v), M_0=0.            (3)

Donors are the first m/2 tuples and survivors the remaining m/2. Define v=+1/sqrt(2m) on the m donor compensators, -1/sqrt(2m) on the m survivor compensators, and zero elsewhere. The same v is used for EVERY stage and every query witness. It is zero-sum and O_*v=v.

Let S_t be ALL 2m physical sites of the survivor tuples. The co-moving zero-sum subspace

    H_t={z:support z subset S_t, sum z=0}

is mapped isometrically by O_* to H_(t+1). When all survivor gates equal g_H=1-n^-2, G multiplies it by g_H, independently of every donor gate. Its orthogonal complement is invariant. The accepted two-step complement norm bound, with donors at g_L=.995 and public bath/front gates <=.9992, is

    1-m/(8000n),

and a unit forcing has complementary response <=16000n/m. This keeps ALL Householder renewals.

For a common-mode write of length t_e, start (3) from zero, use donor g_theta=g_L+(theta+1)(g_H-g_L)/2 until the final L_d=ceil(1000log n) low-tail steps, keep survivors high throughout, then apply the legal final scalar trace correction. At theta=+1 the early response is kappa_e v; at theta=-1 it is kappa_e p+e, where p is the zero-sum projection onto H, ||p||=1/2 and ||e||<=16000n/m. Here

    kappa_e=g_H sum_(j=0)^(t_e-L_d-1)(ag_H)^j
             >=.998 t_e.                             (4)

The accepted carry estimate through the common low tail gives, BEFORE any reset, matched-minus-low difference y with

    |w^T y|>.497 kappa_e, ||y||<1.001 kappa_e,
    w=1_(S_t)/sqrt(2m).                              (5)

Equation (5) uses only the two-step complement estimate, short tail drift and a near-g_L last gate; it does not need a monotonicity claim about intermediate theta. It remains valid for t_e>=3n^(3/4) and the rounding/ranges below. All conservative errors are smaller than .001kappa_e at n>=10^200. A nonzero incoming state contributes a homogeneous term; its H component cancels exactly between the two donor endpoints, and its complementary norm will be charged explicitly.

## 3. A nonuniform public mask produces a Theta(kappa) orthogonal mode

Label survivor tuples so a balanced character chi takes values +/-1. All four sites of a tuple have the same label. The normalized spatial mode

    xi_t=chi/sqrt(2m) on S_t, zero elsewhere

is orthogonal to w. Each sign has m physical sites. Apply the SAME public mask to both histories: g_H where chi=+1, g_L where chi=-1, for

    L_mask=ceil(2000 log n).

Before the mask, y is constant on survivor sites for the one-coordinate donor comparison: the same survivor gates, fixed forcing and zero initial DIFFERENCE make each co-moving survivor row obey the same recurrence. Zero-sum incoming survivor components evolve identically and cancel. Thus each sign-group common projection initially has magnitude >.497kappa/sqrt(2).

For the retained high half, the accepted exact Householder compression is 1-cm and outside coupling <=sqrt(10m/n). Over L_mask steps, norm contraction and the common-mode drift estimate cost <=3L_mask sqrt(10m/n)*1.002kappa<.001kappa. Its common projection remains >.35kappa. The erased half obeys

    beta_-next=a g_L(beta_-+sqrt(m)u^T y),
    |u^T y|<=3||y||/sqrt(n).

Consequently

    |beta_-|<=1.002kappa n^-10
                    +603kappa sqrt(m/n)<.001kappa.    (6)

It follows that

    |xi^T y_mask|>(.35-.001)kappa/sqrt(2)>.24kappa.   (7)

This is finite amplitude, not tangent rank. The mask creates a spatial step in the private broadcast response. It is not a different Householder eigenvector being spontaneously amplified. Incoming complementary state with norm B contributes at most 2B to the comparison; below 2B<.001kappa, so the conservative .24 in (7) still holds.

After restoring ALL survivors high, the xi component is an EXACT co-moving zero-sum mode. It sees no J or B feedback and decays only by ag_H. Complement damping can erase the common/bath part without erasing xi.

## 4. Walsh geometry protects earlier writes during new nonuniform masks

Let survivor tuple j have a PUBLIC label b(j) in {0,1}^R; every label occurs m/2^(R+1) times. Put chi_e(j)=(-1)^(b_e(j)). For K subset {1,...,R}, chi_K=product_(e in K)chi_e. The nonempty characters are orthogonal and zero-sum on S. Their unit vectors are xi_K=chi_K/sqrt(2m).

At stage e use the mask chi_e. For any K containing an EARLIER bit f<e,

    sum chi_K=0, sum chi_K chi_e=0.

Hence the mask preserves zero sum at EVERY intermediate step. Both Householder feedback terms vanish exactly for this stored component. No state leaks off S. During L_mask mask steps it transforms exactly as

    xi_K -> A xi_K+B xi_(K symmetric_difference {e}),
    A=[(ag_H)^L_mask+(ag_L)^L_mask]/2,
    B=[(ag_H)^L_mask-(ag_L)^L_mask]/2.               (8)

Both resulting characters still contain f. After the mask, restoring uniform high gates again preserves this space. Thus an older write never becomes the sole character of a later bit.

For a write made with bit f, subsequent masks produce only characters containing f and later bits. Its FINAL coefficient on xi_{f} is the product of the A's and the uniform-high decay factors, bounded below by

    (ag_H)^T 2^(-(R-f)).                             (9)

No write f!=e has a nonzero xi_e readout. This is the exact triangular READ structure. It is not a list of separately successful histories and does not follow from a raw matrix rank. The masks act on the SAME full survivor support; the protected spatial patterns overlap everywhere.

## 5. Whole joint protocol and exact trace independence

For e=1,...,R set

    t_e=ceil(3*2^(R-e)n^(3/4)),
    L_d=ceil(1000log n),
    L_mask=ceil(2000log n),
    L_clear=100000ceil(n/m)ceil(log n).

Each stage consists of:

1. A length t_e common-mode write controlled ONLY by theta_e. Survivors ALL high; donors g_theta_e until the final L_d-1 common low steps and the last trace correction.
2. The public chi_e mask for L_mask, donors low.
3. Restore ALL survivors high, donors low, for L_clear. No sensitivity reset is performed.

Only after ALL stages is the accepted public hidden-state reset applied. Initial preparation and the source are the accepted ones.

At a stage start the donor local trace k_0 is PUBLIC and identical for every section point. Define the target by running g_L throughout t_e from k_0. At the last donor step set

    g_last(theta_e)=k_target/(1+a k_prev(theta_e)).    (10)

This sets the trace EXACTLY. Since the preceding L_d-1 steps are common low, |g_last-g_L|<=2N n^-5, where N=T+1 bounds all prior traces. Thus .994<g_last<.996. All gate words are admissible and continuously depend on theta_e. This is an analytically specified correction, not post-result tuning.

Every survivor gate schedule is PUBLIC, including all Walsh masks, so survivor local traces are independent of every theta. Donor trace matching in (10) makes the next stage's donor trace public too. By induction all future gate words after a coordinate's stage are INDEPENDENT of that earlier coordinate. This exact property is essential to (8)-(9). At the final old quantile p=1, so the entire section has equal final local codes: traces are public and there are no quantile positions.

For this stationary-compensator probe, C never moves an injected parameter column onto a cycle row. Local compensator responses are precisely those scalar traces. Hence L_N v is the SAME over the whole section, and every final comparison on v is in the PRIVATE H_N=M_N-L_N channel. The new modes are not changing direct survivor traces in disguise.

The accepted inverse lift realizes every gate word in the whole cube [-1,1]^R. Each tuple remains zero-sum in STATE; bath/front/source evolution is public. The final PUBLIC reset gives the identical exact nonzero endpoint to EVERY history. All raw inputs, including source preparation, interior drives, masks, clearing, trace corrections, dense lift and reset, count in (1).

## 6. Uniform joint antipodal proof; no intermediate monotonicity assumption

Let P_H be the orthogonal projection onto the survivor zero-sum space. At the end of every clear segment,

    ||(I-P_H)x||<=B_0:=16000n/m+N n^-6.             (11)

The initial complementary state contracts by <=n^-6 because L_clear/2 times m/(8000n) is >6log n. The forced complement uses the accepted unit-forcing bound. This is an ABSOLUTE bound on the mathematical credit state, not free input energy or an implemented reset. For stage1 its incoming state is zero. Later B_0/kappa_min<.0001, kappa_min>=.998*3n^(3/4).

Compare two cube points differing in ONE coordinate f, with every other coordinate fixed. During stage f the identical incoming P_H state propagates independently of the donor gate and cancels. Its complement contributes <=2B_0. The matched-versus-low endpoint comparison consequently has the mask gain (7). For ARBITRARY values of coordinate f, its survivor difference at the write end is constant on S, hence after its mask it lies in span{1,xi_f}. Its clear segment leaves

    Delta x=alpha_f xi_f+error,
    ||error||<=2N n^-6.                             (12)

Equation (12) also holds for arbitrary differing amplitudes, with no asserted gain. The final amplitude/read for endpoint +1 versus -1, including all later masks/high intervals and public reset, satisfies

    |xi_f,future^T O_* Delta x_N|
       >.23 kappa_f 2^(-(R-f))                     (13)

apart from the same small error. The ag_H total factor is >.999; final reset multiplies by public a q_N>.98; future O_* maps each protected zero-sum character exactly to its next support. These losses leave .23 from .24.

Now compare ANY boundary antipodes theta,-theta of the CUBE. Some |theta_e|=1. Telescope by flipping the R coordinates one at a time. The e-flip has (13), uniformly in all earlier controls, because its incoming complement is bounded by (11). Every OTHER flip has zero ideal xi_e readout by (8)-(9); its error is <=2N n^-6. Total cross-control remainder is <=2R N n^-6. No cancellation of the e signal by other finite-amplitude parameters is possible beyond this explicit charge. This establishes a WHOLE-boundary, finite-radius, joint statement.

Map the Euclidean ball to the cube by the odd radial homeomorphism

    theta(y)=||y||_2 y/||y||_infinity, y!=0;
    theta(0)=0.

Its inverse is ||theta||_infinity theta/||theta||_2. Boundary antipodes become cube antipodes. Every coordinate changes a nonempty early donor gate interval, so the gate and raw-input section is continuous and injective. No affine assumption about alpha_f(theta_f) or local Jacobian is used.

If a continuous encoder used fewer than R counted persistent coordinates, Borsuk-Ulam on this boundary would produce equal encoder states at antipodes. Their current hidden endpoint and public time are the same. One legal query would then require the common decoder output to approximate two gradients separated by >2epsilon, which is impossible. Thus the joint section gives the claimed causal credit-coordinate lower bound; no finite-state or bit-counting argument is involved.

## 7. Actual legal queries and full error ledger

For a selected character e choose two legal one-step future patterns with high gate sech^2(.25) on its positive sites and low gate sech^2(.75) on its negative sites, and vice versa. They agree off S. Each preactivation is in [.25,.75]; the SAME chosen query is applied to both histories. Let s_gate=(g_hi-g_lo)/2>.17. Head is 1/sqrt(n), recurrent group factor 1/n, source feature normalization unchanged. Triangle inequality over the two actual query outputs gives

    nu(Delta M_N)>=sigma sqrt(l)a s_gate sqrt(2m)/(n sqrt(n))
                                |xi_e^T O_* Delta M_N v|.   (14)

Other parameter coordinates are unrestricted; projection onto unit v is only a valid LOWER on gradient norm. This is not RMS visibility, an arbitrary adjoint, or the old paired 8/n upper coefficient.

Using (4), (13), m>=.99sqrt(n), and sigma>.0499, the main pair signal is greater than

    .0499*.99*.17*.23*.998*3*sqrt(.99)>.005.          (15)

The ledger is:

- Complement injection/damping: <=16000n/m and incoming homogeneous difference <=2B_0, charged before the .24 write constant.
- Mask's common-mode drift: <=3L_mask sqrt(10m/n)*1.002kappa<.001kappa.
- Erased group: <=1.002kappa n^-10+603kappa sqrt(m/n)<.001kappa.
- Tail/trace corrections: <=4N^2 n^-5, absorbed in the .497 write constant; all trace equalities themselves are exact.
- Temporal transport and future masks: multiplicative (ag_H)^T>.999 and factor 2^(-(R-e)); compensated by t_e.
- Public reset: a q_N>.98; character transport by future O_* is exact in the reference.
- Cross-coordinate residual: <=2R N n^-6 in state norm, permitted-query charge <1e-9.
- Dense pair comparison: <=8e-9, uniformly over the WHOLE section.

Therefore ACTUAL pair distance >.005-9e-9, and half-margin >.0024. These are finite-error bounds at epsilon=.001. The correction to the old printed dense display is preserved: do not reuse it; a correct finite-N ledger is e_R sigma sqrt(l)[q_f N(N-1)/n+14N/n], e_R<=4/(10^8n^2), q_f<.941.

## 8. Energy, floors, and proved growth

Let T=sum_e t_e+R(L_mask+L_clear). The stage lengths sum to <=3(2^R-1)n^(3/4)+R. For n>=10^200 and R<=floor(log2(n)/8),

    R(L_mask+L_clear)+R+2<2^R n^(3/4),
    T+2<4*2^R n^(3/4), S=m+T+4<=floor(n/4)/100.      (16)

The largest rounding loss m relative to sqrt(n) is <2^(R+1)/sqrt(n)<=2n^-3/8. The high-gate loss across the WHOLE experiment is <=2T/n<=8n^-1/8, vastly below .001 at the threshold. The clear factor is <=n^-6 for every n in range. These elementary bounds improve with n and bound all errors uniformly, not just at sampled widths.

The accepted FULL norm estimate gives

    ||X||<=2sqrt(m(T+2)+1)<5*2^(R/2)n^(5/8).

For R=2, stage sum is 9n^(3/4)+rounding, overhead <n^(3/4), giving norm<8n^(5/8). At maximal R, 2^R<=n^(1/8), establishing (2). R grows logarithmically, not faster than n.

## 9. Strong exact negative statements and limits

For ANY legal nonuniform tuple gates, every within-tuple zero-sum combination of the private H=M-L rows cancels EXACTLY: all four private rows equal V_i, and its sum-zero row functionals annihilate them. Householder feedback is broadcast and cannot excite those three internal tuple modes. The new modes are BETWEEN tuple means, not within a single four-site pair structure.

For the present Walsh protocol each new bit needs 2^R equally represented labels and each later erasure halves an older character's coefficient. Thus our constructive cost grows as 2^R; it is not an O(R)-cost multiplication of cheap signals. Reusing a bit fails the identity sum chi_K chi_new=0 and can create an all-ones component; fresh bits are essential. The current theorem does not prove a maximum for arbitrary nonuniform gates.

Any section whose entire separation is witnessed through ONE fixed parameter probe factors through its n-dimensional actual state response mathcal M_N v. Borsuk-Ulam gives D<=n for that scoped notion. This is NOT an upper on complete fixed-feature sensitivity, which has multiple parameter columns. Our growing-single-probe route therefore cannot alone yield D=omega(n), regardless of the number of masks.

The full corridor remains open. A useful next lemma is whether the protected spatial-write/read construction can be replicated across genuinely independent parameter-column probes in ONE jointly admissible ball, with its worst-query gain and shared energy controlled. Separate columns, separate successful runs or a rank count are insufficient. Global threshold [1/4,3/4], accepted Omega(n log n) construction and full-model gap remain unchanged.
