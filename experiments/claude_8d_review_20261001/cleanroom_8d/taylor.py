"""Symmetric Taylor coefficient ring, independently derived via convolution."""
import itertools, math
import numpy as np
from arithmetic import ZERO, ONE, Up, usum

class Ring:
    def __init__(self,q,order=3):
        self.q=q
        self.indices=[()]+[t for d in range(1,order+1) for t in itertools.combinations_with_replacement(range(q),d)]
        self.lookup={a:i for i,a in enumerate(self.indices)}
        self.pairs=[]
        for a in self.indices:
            counts=[a.count(i) for i in range(q)]
            terms=[]
            for bcounts in itertools.product(*(range(c+1) for c in counts)):
                b=tuple(i for i,c in enumerate(bcounts) for _ in range(c))
                c=tuple(i for i,n in enumerate(counts) for _ in range(n-bcounts[i]))
                terms.append((self.lookup[b],self.lookup[c]))
            self.pairs.append(terms)
    def empty(self): return [ZERO]*len(self.indices)
    def mul(self,a,b):
        return [usum(a[i]*b[j] for i,j in pairs) for pairs in self.pairs]
    def tensors(self,jets,d):
        out=np.empty((len(jets),)+(self.q,)*d,dtype=object)
        for ix in itertools.product(range(self.q),repeat=d):
            a=tuple(sorted(ix)); factor=math.prod(math.factorial(a.count(i)) for i in set(a))
            k=self.lookup[a]
            for row,j in enumerate(jets): out[(row,)+ix]=j[k]*factor
        return out

def hidden_compose(ring,A,g):
    A2=ring.mul(A,A); A3=ring.mul(A2,A)
    H=[g[0]*a+g[1]*b/2+g[2]*c/6 for a,b,c in zip(A,A2,A3)]
    F=[g[1]*a+g[2]*b/2+g[3]*c/6 for a,b,c in zip(A,A2,A3)]
    F[0]=g[0]
    return H,F
