"""E4: scalar hole recovery x_{t+1}=tanh(a x_t + B*) from x=0, with B* and H
measured at the actual h* (n=1e4,1e5,1e6) and the n->infinity limit
(H=tanh(.05), B*=atanh(H)-H).  Reports steps the coordinate stays 'bad'
(|x-H|>m/2=0.01) and nearly critical (x<0.01), and the energy of the creating
pulse (|atanh H| ~ H).  Shows the duration is O(1/H^2), n-independent."""
import numpy as np

m = 1 / 50
rows = []
for n in (10**4, 10**5, 10**6, None):
    if n is None:
        a = 1.0
        H = np.tanh(0.05)
        tag = "n->inf"
    else:
        h = np.load(f"hstar_{n}.npy")
        k, d = n // 2, n // 4
        H = np.median(h[d:k])
        a = 1 - 1 / n
        tag = f"n={n}"
    B = np.arctanh(H) - a * H
    x = 0.0
    t = 0
    bad = 0
    crit = 0
    l2 = 0.0
    while abs(x - H) > 1e-6 and t < 10**7:
        x = np.tanh(a * x + B)
        t += 1
        if abs(x - H) > m / 2:
            bad += 1
        if abs(x) < 0.01:
            crit += 1
        l2 += (x - H) ** 2
    pulse = np.arctanh(H)   # preactivation shift to put coordinate at 0 from h*
    print(f"{tag:9s} H={H:.6f} B*={B:.4e} H^3/3={H**3/3:.4e} bad steps(|u|>.01)={bad} "
          f"near-crit steps(|x|<.01)={crit} pulse energy={pulse**2:.4e} "
          f"sum_t u^2={l2:.4f}  ratio sum u^2/pulse^2={l2/pulse**2:.1f}  1/H^2={1/H**2:.1f}")
