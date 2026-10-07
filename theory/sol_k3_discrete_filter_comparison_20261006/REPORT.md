# Fixed K=3 discrete comparison — report

Sol/Codex, 2026-10-06. THEORY ONLY. **Author verdict: REFUTED for the
specified matched Gemini K=3 bank. Independent hostile review pending.**

## Plain-English finding

The K=3 continuum Gram number is correct. The actual survivor waveform
normalization is not. Symmetric whitening makes three functions orthonormal
in integrated squared magnitude; it does not keep their values below one.
Using those actual functions with Gemini's rho=1/2 and its specified spatial
read basis makes one survivor rate negative. That would require a tanh
derivative gate larger than one. There is no legal center history, before
we reach trace correction, reset or finite-error query separation.

This kills THIS proposed continuum-to-discrete implication. It does not
prove that a correctly renormalized K=3 temporal bank is impossible.

## Strongest exact statements

The four-panel exact Gram is

    G=(1/7680)[64,5,10; 5,14,-10; 10,-10,74].

Exact spectral certificates give

    .03876 < sigma_min(G^(1/2)) < .03878.

Independent small numerical evaluation: .03876699625524..., agreeing with
the surviving ~.03877 checkpoint. No original checks.py was run.

For psi=G^(-1/2)F and the stated Walsh survivor basis:

    lambda_S,1(u)<-eta/200 for 15/16<=u<=1,
    lambda_S,1(1)<-eta/3, eta=10^-6.

Therefore final primary gates require

    g_S,1,t>1+eta/(200W)>1,

independently of all three controls. The endpoint gate has the stronger
excess eta/(3W). This is a strict exact sign failure at every admitted width,
not a floating-rounding issue, one bad sampled query, or a poor Jacobian.

The certificate in PROOF.md supplies an explicit rational approximation to
the inverse square root, exact residual/minor checks, an integral Sylvester
bound and a uniform final-interval inequality. Floating eigenvectors do not
establish the sign theorem.

## Answers to the thirteen questions

1. **Is the continuum Gram value correct?** Yes: ~.0387669963, with the
   rigorous .03876--.03878 bracket.
2. **One genuine discrete continuous B^3 section?** No, for this specified
   candidate. Its public survivor word is illegal even at theta=0.
3. **Whole B^3 boundary controlled?** No robust boundary theorem is obtained.
   The legality failure instead covers the entire ball, including its center.
4. **Discrete minimum protected gain?** Undefined for actual legal histories;
   it would be misleading to report zero or the formal continuum gain.
5. **Complete continuum-to-discrete error?** No such actual comparison exists
   for this word. The first failure precedes an E(n) estimate.
6. **All three traces match exactly?** The inherited formula is not refuted,
   but there are no legal primary histories here to which it can be applied.
7. **Signal survives reset?** Not established for this candidate; its primary
   history cannot be realized. The inherited reducing-space lemma is intact.
8. **Actual legal-query antipodal margin?** None proved/defined for this bank.
9. **Margin >.002?** No such conclusion is justified.
10. **mT=o(n^(3/2))?** The FORMAL intended schedule has that scaling, but it
    is not a realized low-energy theorem. No actual energy is claimed.
11. **Robust D=3 now proved?** No new D=3 temporal-filter theorem is proved.
    This does not deny D>=3 already implied by the verified multicolumn
    construction in its own scope.
12. **Change beta=3/16?** No. It remains a verified construction lower bound,
    not a ceiling. No beta optimization was attempted.
13. **Exact next lemma?** For this fixed K=3 bank, explicitly repair the
    pointwise rate normalization and certify a positive continuum protected
    gain for THAT legal word. Then prove its uniform complete seven-cohort
    discrete comparison and finite-boundary margin. Neither is silently
    assumed here; no new normalization is substituted in this task.

## What the independent reviewer should attack

Check the candidate identification: symmetric whitening psi=G^(-1/2)F,
rho=1/2, and the specified Q3 basis. Then audit (2), the explicit rational
inverse-square-root certificate, the strict final-interval rate inequality,
and the elementary tanh gate obstruction. Verify that the scope is the
specified matched word, not every possible normalized K=3 bank.

No K=4, growing-K, universal dilution, architecture or frontier analysis
was done. No accepted result was reopened. Historical research, the joint
audit, AGENTS.md, CURRENT_THEORY.md and main were not modified.
