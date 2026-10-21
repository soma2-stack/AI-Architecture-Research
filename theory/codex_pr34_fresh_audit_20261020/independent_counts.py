"""Independent combined-listing polynomial and exact integer geometry checks."""
from fractions import Fraction as F
from pathlib import Path
import math,json
HERE=Path(__file__).resolve().parent

def upper_exp(x):
    assert 0<=x<=2
    term=total=F(1)
    for j in range(1,61):term*=x/j;total+=term
    return total+term*x/61/(1-x/62)

def main():
    kap=F(15,100000);lam=450000
    assert upper_exp(F('.6931'))<2
    assert upper_exp(F('.0309'))<1+F(1,32)+F(1,6144)
    assert upper_exp(F('2.302585')/4)**4<10
    # W' <= w0+w1*u, p <= p0+p1*u; L/n<=1/4.
    w0=(8-F('.6931')/2)/kap+1;w1=1/(4*kap)
    p0=7*(w0+lam+1);p1=7*w1
    a0=7*(4*(w0+126667)+lam+4)+F(232000,16)*p0*p0+2*p0+13000000*(1+F('.01')/F('.0618'))
    a1=28*w1+F(232000,8)*p0*p1+2*p1+F(13000000,2)/F('.0618')
    a2=F(232000,16)*p1*p1
    assert a0<F('1.784e17') and a1<F('1.187e15') and a2<F('1.974e12')
    results=[]
    for c0,c1,c2,decade in [(10**12,10**12,10**12,80),(10**18,10**18,10**18,100),
                            (10**30,10**30,10**30,150),(10**200,0,0,826)]:
        u=decade*F('2.302585');term=total=F(1)
        for j in range(1,501):term*=u/(4*j);total+=term
        A=a0+3*c0+F(9,4)*c1;B=a1;C=a2+c2
        margin=[total/161-A-B*u-C*u*u,total/644-B-2*C*u,total/2576-2*C]
        assert all(v>0 for v in margin)
        results.append({'C0':str(c0),'C1':str(c1),'C2':str(c2),'n_threshold':'10^'+str(decade),
                        'positive_g_gprime_gsecond':[v>0 for v in margin]})
    geom=[]
    for n in [31622**4,10**18,1000000000000000280,1000000000000000284,10**80,10**166,10**168,10**180,10**1000]:
        v=40**4*n**3;h=math.isqrt(math.isqrt(v));h+=int(h**4<v)
        D=(n//4-41)//(h+1)
        assert (h-1)**4<v<=h**4 and (161*D)**4>=n
        assert 2*D+1<n//4 and n//4+39+D*(h+1)<=n//2-2
        geom.append({'n':str(n),'H':str(h),'D':str(D),'exact_checks_pass':True})
    result={'polynomial_coefficients':[float(v) for v in [a0,a1,a2]],'count_certificates':results,'integer_geometry':geom}
    (HERE/'independent_counts_result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
