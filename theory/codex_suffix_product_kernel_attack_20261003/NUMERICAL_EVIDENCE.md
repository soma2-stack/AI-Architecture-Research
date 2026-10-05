# Numerical evidence: formula checks only

Fixed seed20261003. No history search, scaling fit, training or GPU.

Six small(m,T) cases: (1,1),(3,5),(5,8),(6,17),(2,31),(6,4).
Gate patterns: random in[.9901,.9999], constant.995, sparse .9902 deficits
on .9999 baseline. Quantile resolution p=1,2,4,9,17.
For each case we explicitly enumerate up to64 legal sign vertices to
compute the exact worst-sign norm numerically, and compare with the analytic
finite-radius cap sqrt(mT min(m,T))/p. This is cheap identity validation,
not a brute-force witness search or robust-dimension lower estimate.

Cumulative spectra are checked at T=1,2,4,16,32; exact rational Haar
cumulative squares at half-length1,2,4,8,16. Large scalar dimension-count
examples allocate no large matrices or histories.

At192 and256 bits:

    q_f=sech^2(.25)=.940014848806377956277210780084...
    100sqrt(2)*.051=7.2124891681027847488886...<8.

An eight-gate row pair with opposite .0007 log perturbations in its first
and last gates has the SAME total product and same p=2 quantile code, while
other row entries differ by about.001393. Its inverse-level discrepancy
is3.19e-58 /8.64e-78 at192/256 bits, consistent with zero mathematically.
This illustrates finite-error coordinate collapse, not exact noninjectivity
of the product map (which is proved injective).

All204 recorded checks pass. These are ordinary high-precision numerical
calculations, without outward error control; the rigorous theorem rests
on written exact formulas and inequalities, not numerical agreement.
