# Fixed K=3 comparison: exact Gram, illegal matched survivor word

Sol/Codex, 2026-10-06. THEORY ONLY. Author counterexample; independent
hostile review required. STATUS=REFUTED applies ONLY to the specified
Gemini matched K=3 history, not to the Gram or to all possible K=3 banks.
No K=4, growing-K, alpha, beta optimization or architecture work is done.

## 1. Precise result

Let r_1,r_2,r_3 be the Paley Walsh words with quarter-interval signs

    r_1=(+,+,-,-), r_2=(+,-,+,-), r_3=(+,-,-,+).

Put F_j(u)=integral_0^u s r_j(s) ds, G_ij=integral_0^1 F_i(u)F_j(u) du,
H=G^(-1/2), and use the explicitly matched bank psi(u)=H F(u).
Use Gemini's specified orthonormal survivor-read matrix

    Q_S=(1/2)[ 1,-1, 1,-1;
                1, 1,-1,-1;
                1,-1,-1, 1 ],
    lambda_S(u)=eta[1_4+(1/2) Q_S^T psi(u)], eta=10^-6.       (1)

THEOREM A. The exact temporal Gram is

    G=(1/7680)[64,5,10; 5,14,-10; 10,-10,74].                (2)

It is positive definite and

    .03876 < sigma_min(G^(1/2)) < .03878.                    (3)

Independent numerical evaluation gives .03876699625524...; this decimal
is evidence, whereas (2)--(3) are rigorous rational certificates.

THEOREM B. For the matched bank (1), its FIRST survivor rate satisfies

    lambda_S,1(u) < -eta/200, 15/16 <= u <= 1,
    lambda_S,1(1) < -eta/3.                                 (4)

Therefore the prescribed discrete word g_S,1,t=1-lambda_S,1(t/W)/W
requires

    g_S,1,t > 1+eta/(200W) > 1
              whenever ceil(15W/16) <= t <= W.              (5)

Every such gate is impossible in the frozen tanh family. This is already
true at theta=0 and is independent of all three donor controls. There is
no legal center history, hence no actual discrete B^3 section corresponding
to this candidate, no actual protected transfer matrix to compare to its
continuum matrix, and no robust-memory conclusion from this bank.

This does not refute existence of a DIFFERENT, correctly normalized K=3
bank. Changing the common waveform normalization, rho, spatial orientation
or public base rates changes the candidate; it must be stated and analyzed
explicitly rather than silently substituted into its purported proof.

## 2. Candidate recovered from the sources

The source is ../gemini_time_varying_nearcritical_filter_bank_20261006/:
PROOF.md sections 3 and 5 define the matched psi=G^(-1/2)F, rho=1/2,
eta=10^-6, delta=10^-30. The only explicit K=3 spatial basis in that
folder is Q3 in checks.py; (1) transcribes that DEFINITION, not any test
output or numerical assertion. No original script is run or trusted.

Its proposed donor words and geometry are

    lambda_D,j(u,theta)=(j+1)eta+delta theta_j r_j(u), j=1,2,3,
    theta in B^3, g_D,j,t=1-lambda_D,j(t/W,theta)/W,
    W=ceil(10^60 n^(3/4)), L=ceil(1000 log n), T=W+L, N=T+1,
    p=2floor(sqrt(n)/10), m=7p/2, h=2p.

There are seven equal cohorts D1,D2,D3,S1,S2,S3,S4, each p/2 four-site
tuples. The source feature is f_s=1_l/sqrt(l). Fixed probes are
v_j=(d_j-s_j)/sqrt(2), with d_j,s_j unit compensator indicators; their
recurrent actions (Ev_j)f_s^T are Frobenius-orthonormal. The unit witness
is v=(v_1+v_2+v_3)/sqrt(3). Its mean forcing is
f=(1,1,1,-1,-1,-1,0)/(2sqrt(3)).

The leading continuum protected transfer asserted by the source is

    J_lead = -[rho eta/(14sqrt(3))] G^(1/2).                  (6)

Thus its leading minimum .5*10^-6*.03876699.../(14sqrt(3)) is indeed
about 7.99e-10. This arithmetic and the Fubini/Gram identity do not enforce
pointwise survivor-rate legality.

The joint audit at theory/grok_codex_gemini_joint_audit_20261006/ correctly
preserves the Gram and rejects the claimed robust completion. Its positive
rate envelope assumes |psi_j|<=1. That bound is not true for the specified
matched whitening. The present certificate checks the ACTUAL matched
waveforms, not a hypothetical bounded substitute. No audit file is edited.

## 3. Independent exact integration

For u in successive quarters, the complete vector F is

    [0,1/4]:   (u^2/2, u^2/2, u^2/2),
    [1/4,1/2]: (u^2/2, 1/16-u^2/2, 1/16-u^2/2),
    [1/2,3/4]: (1/4-u^2/2, u^2/2-3/16, 1/16-u^2/2),
    [3/4,1]:   (1/4-u^2/2, 3/8-u^2/2, -1/2+u^2/2).         (7)

Values agree at boundaries. Walsh conventions at isolated jump points do
not change these integrals or the continuous survivor words.

Integrating products of these quadratic polynomials gives (2). The leading
principal minors of 7680G are 64,871,55654, all positive. For the lower
spectral bound, direct rational arithmetic gives all three leading minors
of G-(969/25000)^2 I positive. For the upper bound,

    det[G-(1939/50000)^2 I] < 0.

The latter matrix has a negative eigenvalue, so the minimum eigenvalue of
G is smaller than (1939/50000)^2. This proves (3). No quadrature mesh,
sampled trajectory or floating eigensolver is part of this argument.

H G=G^(1/2) gives M_ij=integral psi_i F_j=(G^(1/2))_ij, exactly. It also
gives integral psi_i psi_j=delta_ij. L2 orthonormality does NOT imply
pointwise |psi_i|<=1. Indeed a continuous L2-unit function bounded by one
would have absolute value identically one; these matched functions are
continuous, start at zero and are not such functions.

## 4. Rational certificate for H, without trusting an eigensolver

Define the following explicit symmetric rational matrix:

    B=(1/10^6)[11190504,-1715279,-997092;
              -1715279,25098676,2619403;
              -997092,2619403,10598990].                    (8)

We will prove ||B-H||_op<1/1400 by exact matrix arithmetic. This treats B
as a CERTIFICATE; the way its entries were discovered is not a premise.

The leading minors of B-8I are

    398813/125000,
    51611212124863/10^12,
    52103308044604078489/(5*10^17),

so B>8I. Also tr(G)=19/960<1/40, hence H>sqrt(40)I>6I. The inverse is

    G^(-1)=(3840/27827)[936,-470,-190;
                      -470,4636,690;
                      -190,690,871].                        (9)

For R=B^2-G^(-1), a common denominator is 27827*10^12. Its exact integer
numerator matrix is

    [-209697161533, 492364924208,  71643230105;
      492364924208,-479294032098,-314840249418;
       71643230105,-314840249418, -71781420329].

Every numerator has absolute value <=492364924208 <27827*10^9. Thus
|R_ij|<1/1000 and ||R||_op<=||R||_F<3/1000<1/100.

For E=B-H, BE+EH=B^2-H^2=R. The exact Sylvester solution is

    E=integral_0^infinity exp(-Bs) R exp(-Hs) ds.

This follows by differentiating the integrand and using positive spectra;
no commutativity of B,H is assumed. Its norm is strictly less than

    (1/100)/(8+6)=1/1400.                                 (10)

This certifies closeness to the UNIQUE positive symmetric inverse square
root and justifies every following inequality without floating error.

## 5. Negative rate on a whole final interval

The first column of Q_S is (1/2,1/2,1/2). Consequently

    lambda_S,1(u)/eta=1+(1/4)1_3^T H F(u).                 (11)

On [3/4,1], write F(u)=b+c u^2, where
b=(1/4,3/8,-1/2), c=(-1/2,-1/2,1/2). Exact arithmetic gives

    1_3^T B c=-1391227/125000=-11.129816.

By (10),

    |1_3^T(H-B)c| < sqrt(3)*(1/1400)*(sqrt(3)/2)=3/2800.

Thus 1_3^T H c<0, and 1_3^T H F(u) decreases with u on that quarter.
At u_0=15/16,

    1_3^T B F(u_0)=-128708227/32000000.

For every u, |F_j(u)|<=integral_0^u s ds<=1/2, so
|1_3^T(H-B)F(u_0)|<3/2800. The exact strict arithmetic gap is

    -201/50 - [-128708227/32000000+3/2800]
       =237589/224000000 >0.

Hence 1_3^T H F(u)<-201/50 on [15/16,1], proving
lambda_S,1(u)/eta<1-201/200=-1/200. At u=1,

    F(1)=(-1/4,-1/8,0),
    1_3^T B F(1)=-21479533/4000000,
    -21479533/4000000+3/2800 < -16/3.

Equation (11) then proves the stronger endpoint bound lambda_S,1(1)<-eta/3.

## 6. Why there is no actual discrete comparison

In the actual frozen tanh model, each diagonal gate is

    g_i=sech^2(preactivation_i)=1-h_i^2 <=1.               (12)

The inherited inverse lift prescribes beta_i=sqrt(1-g_i). For the first
survivor word on the final interval, (5) instead requires

    beta_i^2=lambda_S,1(t/W)/W <0.

No real beta, hidden state, preactivation or inverse-lift raw input exists.
The failure applies to the WHOLE control ball because survivor schedules
are public and independent of theta. It is not a tangent or axis argument.

For every n>=10^1000, W is an integer >=16 and the prescribed final sample
t=W uses u=1. At least floor(W/16)+1 final primary samples lie in the bad
interval. Changing only the endpoint convention cannot repair the word;
the rate is strictly negative on an interval of positive length.

For clarity, the complete reference recurrence that a LEGAL candidate would
need to satisfy is

    M_0=0, M_t=G_t(aO_*M_(t-1)+I),
    O_*=C+1u^T+e_1 v_H^T,
    J_t=u^T M_t, B_t=v_H^T M_t,
    L_t=G_t(aCL_(t-1)+I), H_t=M_t-L_t,
    H_t=sum_(s=1)^t Phi_C(t,s) aG_s[1J_(s-1)+e_1B_(s-1)],
    Phi_C(t,s)=(aG_t C)...(aG_(s+1) C).

This retains all chronological rank-two feedback, bath, front, global-time
front bank and terminal paths. Inputs must be realized and then frozen under
differentiation. The accepted actual dense lift and common reset do not
allow gates above one, so neither can fix (12). Computing the same formal
matrix recurrence with g>1 would be a SHADOW linear system, not an actual
tanh history. No all-query or energy inference from that system is valid.

In particular A_discrete(theta) for the requested legal section is undefined;
there is no mathematical error E(n) between that nonexistent actual matrix
and A_cont. It would be incorrect to report E(n)=0, a vanished singular
value, or an asymptotic error exceeding a margin: legality fails BEFORE
those comparisons become meaningful.

## 7. Downstream disposition and narrow scope

For this specified bank, the following claimed completions are not available:
three legal jointly lifted histories, trace corrections of such histories,
a protected actual reset signal, an actual legal-query pair margin, an
actual full-history norm, or a new robust D=3 theorem. The continuum Gram
and its arithmetic leading signal survive. Exact trace matching and the
verified K=2 theorem are not contradicted or reopened.

The formal proposed geometry would have m=7floor(sqrt(n)/10), not
m<=.5sqrt(n) as printed. This arithmetic typo is secondary and is NOT the
refutation: the rate counterexample (4) already kills realizability.
No upper bound on physical robust dimension, no dilution barrier and no
claim about all redesigned corridor histories is derived here.

The user's verified multicolumn D>=n^(3/16)/3 is a CONSTRUCTION LOWER
BOUND, not a ceiling. It remains unchanged. No K=4 or growing-K calculation
is performed. Main, AGENTS.md, CURRENT_THEORY.md and historical reports stay
untouched. The next fixed-K=3 dependency, if the owner chooses to repair the
candidate, is an explicitly pointwise-legal normalized survivor word with
a certified protected continuum gain, followed by a COMPLETE seven-cohort
finite-ball discrete comparison. This proof does not substitute a new word.
