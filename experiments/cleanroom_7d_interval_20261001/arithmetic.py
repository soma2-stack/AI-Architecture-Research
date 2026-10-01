"""Separate directed arbitrary-precision backend; no project engine imports."""
from fractions import Fraction
from mpmath import iv
from mpmath.libmp import (mpf_add, mpf_mul, mpf_div, mpf_sqrt, mpf_cmp,
                         from_int, from_rational, to_float, round_ceiling)

PREC = 192
def set_precision(bits):
    global PREC
    PREC = bits
    iv.prec = bits

def fraction_tuple(t):
    sign, man, exp, bits = t
    return Fraction((-1 if sign else 1)*man) * Fraction(2)**exp

def interval(x):
    if isinstance(x, Up):
        return iv.make_mpf((x.t, x.t))
    if hasattr(x, '_mpi_'):
        return x
    f = Fraction(x)
    return iv.mpf(f.numerator)/iv.mpf(f.denominator)

class Up:
    __slots__ = ('t',)
    def __init__(self, x=0, raw=False):
        if raw:
            self.t = x
        elif isinstance(x, Up):
            self.t = x.t
        else:
            f = Fraction(x)
            if f < 0:
                raise ValueError('negative majorant')
            self.t = from_rational(f.numerator, f.denominator, PREC, round_ceiling)
    def __add__(self, other):
        other = Up(other)
        if not self.t[1]: return other
        if not other.t[1]: return self
        return Up(mpf_add(self.t,other.t,PREC,round_ceiling),True)
    __radd__ = __add__
    def __mul__(self, other):
        other = Up(other)
        if not self.t[1] or not other.t[1]: return ZERO
        return Up(mpf_mul(self.t,other.t,PREC,round_ceiling),True)
    __rmul__ = __mul__
    def __truediv__(self, other):
        other = Up(other)
        return Up(mpf_div(self.t,other.t,PREC,round_ceiling),True)
    def sqrt(self):
        return Up(mpf_sqrt(self.t,PREC,round_ceiling),True)
    def frac(self): return fraction_tuple(self.t)
    def float_up(self): return to_float(self.t,rnd=round_ceiling)
    def __float__(self): return to_float(self.t)
    def __lt__(self,other): return mpf_cmp(self.t,Up(other).t)<0
    def __le__(self,other): return mpf_cmp(self.t,Up(other).t)<=0
    def __repr__(self): return str(float(self))

ZERO=Up(0)
ONE=Up(1)
def upper(x):
    lo,hi=interval(x)._mpi_
    return Up(hi,True)
def lower_fraction(x): return fraction_tuple(interval(x)._mpi_[0])
def upper_fraction(x): return fraction_tuple(interval(x)._mpi_[1])
def abs_upper(x):
    return upper(abs(interval(x)))
def hull(lo,hi): return iv.make_mpf((interval(lo)._mpi_[0],interval(hi)._mpi_[1]))
def radius_interval(r): return hull(-r.frac(),r.frac())
def isum(values): return sum(values,interval(0))
def usum(values): return sum(values,ZERO)
def tanh_box(x):
    x=interval(x)
    vals=[]
    for endpoint in x._mpi_:
        z=iv.make_mpf((endpoint,endpoint))
        e=iv.exp(2*z)
        vals.append((e-1)/(e+1))
    return iv.make_mpf((vals[0]._mpi_[0],vals[1]._mpi_[1]))
def gates(H):
    square=H**2
    g=1-square
    return [abs_upper(g),abs_upper(-2*H*g),
            abs_upper(-2*g*(1-3*square)),abs_upper(8*H*g*(2-3*square))]

def matrix_inverse(M):
    """Interval Gauss-Jordan for a narrow, signed center matrix."""
    n=len(M); C=[[interval(x) for x in row]+[interval(int(i==j)) for j in range(n)] for i,row in enumerate(M)]
    for k in range(n):
        candidates=[i for i in range(k,n) if not(lower_fraction(C[i][k])<=0<=upper_fraction(C[i][k]))]
        if not candidates: raise ArithmeticError('zero-containing pivot')
        p=max(candidates,key=lambda i:float(abs_upper(C[i][k])))
        C[k],C[p]=C[p],C[k]
        pivot=C[k][k]
        C[k]=[x/pivot for x in C[k]]
        for i in range(n):
            if i!=k:
                c=C[i][k]
                C[i]=[C[i][j]-c*C[k][j] for j in range(2*n)]
    return [row[n:] for row in C]

def rational_inverse(M):
    n=len(M); C=[[Fraction(x) for x in row]+[Fraction(i==j) for j in range(n)] for i,row in enumerate(M)]
    for k in range(n):
        p=next((i for i in range(k,n) if C[i][k]),None)
        if p is None: raise ArithmeticError('singular rational matrix')
        C[k],C[p]=C[p],C[k]
        q=C[k][k]; C[k]=[x/q for x in C[k]]
        for i in range(n):
            if i!=k:
                q=C[i][k]; C[i]=[C[i][j]-q*C[k][j] for j in range(2*n)]
    return [row[n:] for row in C]
