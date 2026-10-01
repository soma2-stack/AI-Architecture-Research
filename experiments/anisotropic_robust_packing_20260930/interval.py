"""Outward dyadic arithmetic; elementary transcendental bounds use Taylor tails."""
from fractions import Fraction as Q
from math import isqrt

class I:
    bits=192
    scale=1<<192
    def __init__(self,lo,hi=None,raw=False):
        if raw:self.lo,self.hi=int(lo),int(hi)
        else:
            x=Q(lo)*self.scale
            self.lo=x.numerator//x.denominator
            self.hi=-((-x.numerator)//x.denominator)
        assert self.lo<=self.hi
    @classmethod
    def precision(cls,bits):cls.bits=bits;cls.scale=1<<bits
    @classmethod
    def cast(cls,x):return x if isinstance(x,cls) else cls(x)
    def __add__(self,x):
        x=self.cast(x);return I(self.lo+x.lo,self.hi+x.hi,True)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo,True)
    def __sub__(self,x):return self+-self.cast(x)
    def __rsub__(self,x):return self.cast(x)+-self
    def __mul__(self,x):
        x=self.cast(x);p=[self.lo*x.lo,self.lo*x.hi,self.hi*x.lo,self.hi*x.hi]
        return I(min(p)//self.scale,-((-max(p))//self.scale),True)
    __rmul__=__mul__
    def reciprocal(self):
        assert not self.lo<=0<=self.hi
        k=self.scale*self.scale
        return I(k//self.hi,-((-k)//self.lo),True)
    def __truediv__(self,x):return self*self.cast(x).reciprocal()
    def __rtruediv__(self,x):return self.cast(x)*self.reciprocal()
    def absq(self):return Q(max(abs(self.lo),abs(self.hi)),self.scale)
    def midq(self):return Q(self.lo+self.hi,2*self.scale)
    def sqrt(self):
        assert self.lo>=0
        lo=isqrt(self.lo*self.scale);hi=isqrt(self.hi*self.scale)
        if hi*hi<self.hi*self.scale:hi+=1
        return I(lo,hi,True)
    def square(self):
        if self.lo<=0<=self.hi:
            k=max(self.lo*self.lo,self.hi*self.hi)
            return I(0,-((-k)//self.scale),True)
        return self*self
    @classmethod
    def exp_positive(cls,v):
        assert 0<=v<=4*cls.scale
        x=I(v,v,True);term=I(1);total=I(1);order=cls.bits+32
        for k in range(1,order+1):
            term=term*x/k;total+=term
            if k>8 and term.hi<=2:break
        nxt=term*x/(k+1)
        tail=nxt/(1-x/(k+2))
        return I(total.lo,total.hi+tail.hi,True)
    @classmethod
    def exp_point(cls,v):
        if v<0:return cls.exp_point(-v).reciprocal()
        if v<=4*cls.scale:return cls.exp_positive(v)
        half=I(v,v,True)/2
        return half.exp().square()
    def exp(self):
        a=self.exp_point(self.lo);b=self.exp_point(self.hi)
        return I(a.lo,b.hi,True)
    def tanh(self):
        # tanh is monotone. Evaluate endpoints separately: using the SAME
        # wide exp interval in numerator and denominator loses correlation
        # and can falsely enclose values outside [-1,1].
        a=(I(2*self.lo,2*self.lo,True)).exp()
        b=(I(2*self.hi,2*self.hi,True)).exp()
        low=(a-1)/(a+1);high=(b-1)/(b+1)
        return I(max(-self.scale,low.lo),min(self.scale,high.hi),True)

def matmul(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),I(0))
             for j in range(len(B[0]))] for i in range(len(A))]

def inverse(A):
    """Small exact-rational or interval Gauss-Jordan, with nonzero pivots."""
    n=len(A);is_interval=isinstance(A[0][0],I)
    zero=I(0) if is_interval else Q(0)
    one=I(1) if is_interval else Q(1)
    rows=[list(row)+[one if i==j else zero for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        pivot=max(range(j,n),key=lambda i:float(rows[i][j].absq()) if is_interval else abs(rows[i][j]))
        rows[j],rows[pivot]=rows[pivot],rows[j]
        denom=rows[j][j]
        rows[j]=[x/denom for x in rows[j]]
        for i in range(n):
            if i==j:continue
            v=rows[i][j]
            rows[i]=[x-v*y for x,y in zip(rows[i],rows[j])]
    return [row[n:] for row in rows]
