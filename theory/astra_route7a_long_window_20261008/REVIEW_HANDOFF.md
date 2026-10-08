# Hostile review: long-window Route 7A

**Repository status: PENDING REVIEW. Main target remains OPEN.**

Read [RESEARCH.md](RESEARCH.md), [EXPERIMENTS.md](EXPERIMENTS.md), and the reproducible scripts. Prior source is `1fa6b00018f7dceb72b689c4ebdbe3928ba717f9`. Do not promote CURRENT_THEORY.md from this author report.

## Claims requiring separate verdicts

1. **Exact long-window algebra:** trace-neutral compensator, centered Abel identity (1), O(epsilon G_(W+1)) fresh same-forcing bound (2). This is not a W-independent estimate.
2. **Public state certificate:** support <=N+6m, bath lower invariant, chronological first-front and subsequent front bounds in section 4. Check both autonomous and held-high cohorts, and separation from the terminal backward paths.
3. **Recent-block DONOR compression:** complete donor M rows obey the two-common-row formula plus local forcing determined by recent controls. Equal recent codes eliminate new forcing, leaving operator residual <=2N rho^h. Code size O((m+N)log R), uniform in W.
4. **Full held-high-bank corollary:** conditional D=O(n log R/R)=o(n). This does NOT cover the full autonomous-cohort response, which remains OPEN.

## Highest-risk checks

- Verify the actual complete field J_t is used throughout. Never replace it with a baseline history's field.
- In comparisons of two histories include sum K_+ Delta J and propagated incoming difference. The same-forcing identity alone omits these terms.
- Constant J cancels only with V_in=a tau J. The earlier audit's unconditional sentence is an overstatement; verify the unmatched-initial countercheck.
- Check all chronological indices in U_r, Q_r, A_i and the final reset. A_i<=.995206 must hold uniformly over tau and W.
- Verify the code pays hm coordinates for recent private controls and P coordinates for EACH shared feedback row, not one scalar.
- Moving donor rows follow public characteristics: check the old-row restriction/shift is a partial isometry and does not import unknown local source terms after codes agree.
- Confirm the complete M argument avoids invoking the old THREE-STEP local bound for W>1.
- Verify E_par is genuinely public and includes full parameter directions, not just K probes.
- The prototype's autonomous public cohorts are not piecewise parallel. The full theorem applies only to the explicitly held-high alternative. Do not merge those scopes.
- Check Walsh suffix attenuation, ordinary-row query normalization, exact bath row coding, chronological front error, dense correction, and the Borsuk–Ulam count.
- At R~log log n, h=O(log R), ell fixed: q/n=O(log R/R)->0. Constants and asymptotic onset may be enormous.
- Check cost includes W high steps, compensation, precharge, public cohort holding, source and reset. No finite cost ratio establishes little-o by itself.

## Numerical audit

`long_window.py` extends the corrected sparse state evaluator; full rank-two O and its transpose remain exact reference operations. `run_experiments.py` checks W=1 against the predecessor, dense versus sparse forward state, complete/local trace, and forward/adjoint duality. It uses difference propagation rather than subtracting two large final matrices.

The reference model uses sigma=.05 and omits explicit dense perturbation. Only selected legal future gates/horizons are searched; optimization values are FOUND scores, not suprema. H at an M-selected query is not an H optimum; separate H searches are in `diagnose_feedback.py`. Jacobian spectra are local diagnostics, not robust dimension.

## Requested verdicts

- Long-window trace/Abel algebra: VERIFIED / PARTIAL / REFUTED / OPEN.
- Public bath/front certificate: VERIFIED / PARTIAL / REFUTED / OPEN.
- Uniform-in-W recent-block donor code: VERIFIED / PARTIAL / REFUTED / OPEN.
- Conditional full held-high-bank obstruction: VERIFIED / PARTIAL / REFUTED / OPEN.

## Single next obligation

Prove a sublinear approximate code for the AUTONOMOUS public capture-cohort response at W=Theta(R), or supply a legal robust counterexample. Donor feedback alone is already covered by the new author code theorem if it survives review.
