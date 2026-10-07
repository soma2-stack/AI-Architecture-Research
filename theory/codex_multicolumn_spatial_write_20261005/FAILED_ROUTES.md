# Failed routes and exact scope limits

| Route | First failed identity or inequality | Outcome |
|---|---|---|
| Add orthogonal stationary donor contrasts while retaining one donor gate | M_t d=tau_D,t d for sum(d)=0; matched final tau makes Delta M_N d=0 | FAILED, exact |
| Add orthogonal source features on the autonomous source | delta forcing is sigma(1_l^T f); all source-orthogonal directions have zero forcing | FAILED, exact for this source |
| Multiply R by K without changing the history family | The old family has only R controls; adding gradient probes does not add history dimensions | FAILED, topological |
| Treat per-group donor and shared-survivor probes as orthogonal | W^T W=I+P, not I | Repaired by V=W[I-(1-1/sqrt(2))P] |
| Ignore the shared donor-group gain cost | Axis common row norm is kappa/sqrt(2(K+1)), not Theta(kappa) | FAILED for no-cost multiplication in this family |
| Keep old duration while K diverges | Selected-probe all-query axis margin is O(1/sqrt(K))+negligible error, below .002 eventually | FAILED, scoped; not a universal obstruction |
| Prove only individually good axes | Boundary may have many simultaneous idle controls and old writes | Repaired by multi-idle chronological comparison and stage telescope |
| Replace actual q chronology by a frozen spectral matrix | Gate matrices do not commute | NOT USED; common cone at every chronological step |
| Drop the pre-existing front at each fresh write | rho includes GLOBAL front slots with z>fresh age | FAILED exact truncation; whole bank retained |
| Regard the reduced group recurrence as exact without rho | It omits exceptional-front feedback | NOT USED; rho retained then bounded |
| Claim a diagonal cross-probe response | The row r_e contains all probe coordinates and depends nonlinearly on controls | NOT USED; a unit witness in probe space suffices |
| Count Kn ceiling as achieved dimension | A topological ceiling is not a minimum-gain theorem | FAILED inference |
| Infer superlinear energy improvement from exponent 43/64 | D=Theta(n^(3/16)) is sublinear, so it does not improve the superlinear threshold | FAILED inference |

Open, not refuted: another donor code or moving-cycle parameter-probe
family may avoid the 1/sqrt(K) loss. The new construction does not prove
that dilution is universally necessary. It supplies an explicit
finite-error joint theorem that compensates it with shared duration.
