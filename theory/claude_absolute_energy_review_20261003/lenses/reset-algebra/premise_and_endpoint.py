# Standalone (does not import adversary main loop). Output saved in premise_out.txt.
import os
os.environ["OPENBLAS_NUM_THREADS"]="2"
import numpy as np
exec(open("adversary.py").read().split("out = []")[0])
for n in (200, 256, 400, 1000):
    M = build(n); R, R0 = M["R"], M["R0"]
    eps = 1/(1e8*n**2); a = 1-1/n
    print(f"n={n}: ||R-R0||_op(float)={np.linalg.norm(R-R0,2):.3e}  analytic<=2a*eps/(a-eps)={2*a*eps/(a-eps):.3e}  e_n={4/(1e8*n*n):.3e}")
for n in (200, 400):
    M = build(n); R = M["R"]; b = 0.05*np.ones(n)
    h = np.zeros(n)
    for t in range(60*n): h = np.tanh(R@h + b)
    z = h
    print(f"n={n}: ||z*||={np.linalg.norm(z):.4f}, fixed-pt residual={np.linalg.norm(np.tanh(R@z+b)-z):.1e}")
    for T in (n, 5*n, 20*n):
        g = np.zeros(n)
        for t in range(T-1): g = np.tanh(R@g + b)
        print(f"   T={T}: ||X|| to land exactly on z* = {np.linalg.norm(np.arctanh(z) - R@g - b):.3e}")
