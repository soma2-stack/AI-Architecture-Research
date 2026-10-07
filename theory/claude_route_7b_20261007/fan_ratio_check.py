"""Falsification probe (NOT proof) for the Ky Fan sparsity lemma:
every odd continuous f: S^{D-1} -> R^N \ {0} has a point with ||f||_1^2/||f||_2^2 >= D.
We build odd maps designed to stay sparse (soft-argmax over a net, random odd nets) and
search the sphere for the max ratio. The lemma predicts max ratio >= D for every map."""
import numpy as np
rng=np.random.default_rng(0)
def sphere(n,D):
    x=rng.standard_normal((n,D)); return x/np.linalg.norm(x,axis=1,keepdims=True)
def ratio(Y):
    return (np.abs(Y).sum(1)**2)/(np.square(Y).sum(1))
def sparse_net_map(D,N,temp):
    A=sphere(N,D)                       # net of directions
    def f(T):
        P=T@A.T                         # odd in T
        W=np.exp((np.abs(P)-np.abs(P).max(1,keepdims=True))/temp)  # even weights
        return np.sign(P)*W*np.abs(P)   # odd, concentrated on near-max coordinates
    return f
def random_odd_net(D,N,H):
    W1=rng.standard_normal((H,D)); W2=rng.standard_normal((N,H))
    return lambda T: np.tanh(T@W1.T*3)@W2.T
print("D  map            N     min-over-maps of max-over-sphere ratio   (lemma: >= D)")
for D in [2,3,4,5,6,8]:
    S=sphere(20000,D)
    worst=np.inf
    for trial in range(4):
        for kind in ["sparse","net"]:
            f=sparse_net_map(D,600,0.002*(trial+1)) if kind=="sparse" else random_odd_net(D,60,40)
            Y=f(S); r=ratio(Y).max(); worst=min(worst,r)
    print(f"{D:2d}  sparse/net-mix  600   {worst:10.3f}   pass={worst>=D-1e-6*D}")
