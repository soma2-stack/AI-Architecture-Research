"""Dyadic rational intervals; all certificate arithmetic is exact integer arithmetic."""
from fractions import Fraction

class I:
    bits=256
    scale=1<<256
    def __init__(self,lo,hi=None,raw=False):
        if raw:self.lo,self.hi=int(lo),int(hi)
        else:
            q=Fraction(lo)*self.scale;self.lo=q.numerator//q.denominator;self.hi=-((-q.numerator)//q.denominator)
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
        assert not self.lo<=0<=self.hi,'Interval division by zero'
        k=self.scale*self.scale
        return I(k//self.hi,-((-k)//self.lo),True)
    def __truediv__(self,x):return self*self.cast(x).reciprocal()
    def __rtruediv__(self,x):return self.cast(x)*self.reciprocal()
    def abs_bound(self):return max(abs(self.lo),abs(self.hi))
    @classmethod
    def exp_positive(cls,endpoint):
        assert 0<=endpoint<=4*cls.scale
        x=I(endpoint,endpoint,True);term=I(1);total=I(1);order=cls.bits+32
        for k in range(1,order+1):term=term*x/k;total+=term
        nxt=term*x/(order+1)
        bound=nxt/(1-x/(order+2))
        return I(total.lo,total.hi+bound.hi,True)
    @classmethod
    def exp_point(cls,v):return cls.exp_positive(v) if v>=0 else cls.exp_positive(-v).reciprocal()
    def exp(self):
        a=self.exp_point(self.lo);b=self.exp_point(self.hi);return I(a.lo,b.hi,True)
    def tanh(self):
        e=(2*self).exp();return (e-1)/(e+1)
    def contains(self,q):
        q=Fraction(q)*self.scale;return self.lo<=q<=self.hi

def certify(J,preconditioner):
    """Exact outward bounds for I-MJ, with M integer / 2**bits."""
    size=len(J);scale=I.scale;maxrow=0;residual=[]
    for i in range(size):
        row=[];bound=0
        for j in range(size):
            lo=hi=0
            for k in range(size):
                a=int(preconditioner[i][k]);v=J[k][j]
                lo+=a*(v.lo if a>=0 else v.hi);hi+=a*(v.hi if a>=0 else v.lo)
            lo=lo//scale;hi=-((-hi)//scale)
            unit=scale if i==j else 0
            value=I(unit-hi,unit-lo,True);row.append([str(value.lo),str(value.hi)]);bound+=value.abs_bound()
        maxrow=max(maxrow,bound);residual.append(row)
    return {'verified':maxrow<scale,'residual_infinity_numerator':str(maxrow),'denominator_power2':I.bits,
            'residual_intervals':residual,'criterion':'||I-MJ||_infinity < 1 implies J nonsingular'}
