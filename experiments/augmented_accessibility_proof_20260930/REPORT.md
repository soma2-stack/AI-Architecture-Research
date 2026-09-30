# Arbitrary-width proof-development report

## Classification

**ARBITRARY-WIDTH ACCESSIBILITY PROVED**

This classification describes the mathematical argument in PROOF.md; it is not
an independently peer-reviewed or proof-assistant-certified theorem. The earlier
interval/rational numerical certificates are unchanged.

## Exact conclusion

For h'=tanh(Rh+Wx+b), with all R/W/b entries independently differentiated,
P=2n^2+n, and S'=G(RS+deltaR*h+deltaW*x+deltab), the endpoint (h,S) has dimension
d=2n^3+n^2+n. For every n>=2, invertible R/W and no zero entries in R^{-1}
suffice for a full-rank endpoint at some finite horizon. A sufficient common
horizon is T=4d. Initial h=S=0; parameters remain fixed. The explicit rational
family R=I-11^T/(n+1), W=I, b=0 works at every width.

The discrete-time forward control-pullback module reaches full tangent dimension
after three prefix pullbacks: n hidden directions, n^3 R sensitivities,
n^3 W sensitivities, and n^2 bias sensitivities. A proved rank-increment lemma
turns that module span into one actual input history. No mere hidden-state
propagation-algebra argument or snapshot-rank measurement is substituted.

## Requested proof objects

| Item | Result |
|---|---|
| Framework | Control variations/pullbacks inspired by Jakubczyk--Sontag; direct local forward-rank argument |
| Invertibility | One-step differential nonsingular; global onto-R^d diffeomorphism hypothesis fails and is not used |
| Independent controls | n continuous input directions; W is invertible |
| Full span | d=2n^3+n^2+n for every n>=2 under stated conditions |
| New width directions | 6n^2+8n+4 |
| Schur complement | Suitable fixed histories in an explicit coupling family give a non-identically-zero analytic Schur determinant |
| Leading coefficient | Exists and is nonzero at finite order; value/order not computed |
| Determinant recursion | None found; unnecessary for the direct all-width proof |
| Nonlinear invariant | No nonconstant global C^1 first integral, nor a nontrivial analytic/polynomial identity on all reachable endpoints, under theorem conditions |
| Independent control | Owner-local zeros; d_ind=n^2+3n, much smaller than cubic dense allowance |
| Shared-linear control | Bias invariant preserved; fixed-T rank<=2n, general linear rank<=2n^2 |
| Genericity | For each width at T=4d, nontrivial analytic maximal minor implies open-dense/full-measure nonzero set |
| Remaining questions | Shorter horizons, explicit pulse schedule/minor formula, conditioning, query observability and precision-dependent memory bounds |

## Checks and resources

47 exact symbolic checks passed at n=2 and n=3, including direct augmented
differential identities, gate coefficient independence, bias Laurent expansion,
R covector spanning, the parameter family, width-extension algebra, and the
linear first integral. No new numerical endpoint sweep or wider example was
run. Raw check names, versions, config hash and resource measurements are in
checks_result.json. Equations and analytical implications are in PROOF.md;
the hostile review is in AUDIT.md.

Measured check process: 1.28125 CPU seconds (0.0213542 CPU-minutes), wall
1.3234503 seconds, peak working set 75,362,304 bytes (~71.871 MiB).
A separate conservative 20-second administrative CPU charge is recorded; this
is an estimate, not a measured total. Research/thinking wall time is not claimed
to be metered by the symbolic script. Both measured compute and conservative
charge are far below the 45 CPU-minute budget. No GPU/CUDA, ML framework,
model server, GAS-0, Stage C, AMS v10 or training was used.

Setup/config freeze commit: f614fd0. Results commit is the commit containing this
report (reported to the owner separately, avoiding a self-referential hash).

## Stop / recommendation

STOP. Obtain an independent mathematical verification of the proof, especially
the coefficient-extraction and rank-increment steps. No observability, learning,
Stage C or AMS v10 is authorized by this result. The proved cubic independent
coordinate count is not a finite-precision memory lower bound or an architecture
discovery.
