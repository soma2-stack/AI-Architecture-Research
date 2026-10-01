# Section-specific entropy, not a global upper dimension bound

This is a post-primary analytic consequence of the frozen lower/upper
Lipschitz inequalities. No certificate constants, histories or epsilon change.

On the retained cube, D_C(s(z),s(z'))>=max_i b_i|z_i-z'_i| and
D_C<=M||z-z'||2. For strict separation >delta, the exact integer choice
N_i=max(1,ceil(2b_i/delta)) fits uniformly across [-1,1]: when N_i>1,
step2/(N_i-1)>delta/b_i. Thus a Cartesian grid has at least prod_i N_i
separated states. At delta=2epsilon this gives ceil(b_i/epsilon), possibly
stronger than the historically fixed17/8 conservative spacing rule.
In particular all2^r retained cube corners are separated when b_i>epsilon.
This does not infer continuous dimension FROM a count: both statements follow
independently from the whole-section coordinate inequality.

For a cover, divide each coordinate into ceil(2M sqrt(r)/delta) cells.
Every cell has query diameter<=delta; a strictly separated set has at most
the product of the cell counts. These are exact lower/upper entropy bounds
ON THIS CHOSEN r-SECTION. As delta->0 their exponents are both r. The constants
can be poor and this asymptotic statement need not describe slopes near epsilon.
The ambient reachable family includes other directions and other sections;
this cover is NOT an upper bound on its true robust dimension. No useful
ambient epsilon-specific upper dimension bound follows.
