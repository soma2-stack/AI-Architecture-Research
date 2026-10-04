# Complete differentiated ledger

The full R,W,b sensitivity is equation (1)/(2) in PROOF.md. All entries are
differentiated; this table never identifies cancellation of STATE with
cancellation of DERIVATIVE. Robust lower/upper claims in this stage concern
only the frozen recurrent fixed-source-feature d_F action.

| Channel | Exact representation/status | Query and code status |
|---|---|---|
| Cycle exchange difference, two positive copies | Co-moving p mode, gate product k_i,j, zero-sum homogeneous transport | Accepted paired projected obstruction; not retried |
| Off-cycle exchange difference, two negative compensators | Stationary o mode, eligibility trace kappa_i=sum_j k_i,j | Private, survives reset; one exact scalar per row suffices for this channel |
| Cycle-versus-compensator balance | Co-moving b output mode, sum of signed cycle product rows and compensator traces | Householder term cancels exactly in this OUTPUT combination; no new finite-radius superlinear section |
| Common four-site mode | s output mode with additional 2aJ forcing; private vector V_i=a sum_j k_i,j J_(j-1) | NEW unpaired/private renewal channel; old scalar quantile proof does not cover J weights |
| Ordinary autonomous bath | State public; sensitivity has shared PRIVATE row vector Z_t | Legal queries can see it; bound uses c^T1_r<=102, not an independent query per row |
| Exceptional Householder front | Public forward gates, private row vectors F_z driven by J and B | Rows far from wrapping have coordinate upper100/sqrt(n); their right vectors remain coupled/private |
| Terminal Householder row | Direct row public, feedback equals bath Z_t | Can have order-one legal adjoint coordinate; no global ordinary-row dilution assertion |
| Node0/source for selected fixed feature | Zero reference sensitivity for E v f_s^T | Actual dense leakage included in the comparison. Fixed-feature rows outside E have public reference response |
| Reset | PUBLIC gates and forcing, but private past M is multiplied by aG_N O_* | Transmits credit; does not erase it. Direct future injections cancel only between same-endpoint histories |
| Dense perturbation | Exact comparison recurrence G_t[R Delta B+(R-R0)B_ref] | Fixed-feature pair ledger<=8e-9, uniform; not dropped. Full R/W/b has its own explicit forcing comparison |
| Full recurrent private-feature injection | delta R sum_i 2beta_i b_i(t-1) | Signed private injection, even when state sum is zero; OUTSIDE the frozen source-feature lower target |
| Full input-weight injection | delta W x_t, including odd atanh(beta)-a beta_prev, reset and dense correcting input | Private; not a new d_F result and not assumed quantile-compressible |
| Bias injection | delta b is constant but propagation G_t R is private | Private after propagation; no state-cancellation inference |
| Cross-channel paths | Exact (7) and finite insertion expansion (16); includes prefix-suffix crossover (17) and all higher insertions | Cannot add dimensions from terms or ignore their cancellations/feedback |

## Symmetry correction

The accepted paired parameter frame subtracts two POSITIVE cycle copies.
It is antisymmetric under exchanging those copies. The negative off-cycle
compensators do not supply a minus sign to fixed-source injections: those
injections are identical because the source is public and gates depend on
beta squared. Positive-versus-negative state balance uses the b mode;
the s mode remains private in sensitivity.

## Scope of the strongest partial compression

The direct cycle and compensator contributions share one local product
array. Storing its inverse-level code PLUS the m exact traces gives a
static m p-coordinate description with the local finite-error bound.
This controls the local contribution and balanced identities. It is not
a code for the full common-mode response. Nor does an OUTPUT cancellation
automatically grant arbitrary projected adjoints under the legal contract.

The only remaining fixed-feature part not covered by this local description
is the coupled J/B -> V/Z/F renewal reservoir. This is an exact ledger,
not a claim that its robust width is large.
