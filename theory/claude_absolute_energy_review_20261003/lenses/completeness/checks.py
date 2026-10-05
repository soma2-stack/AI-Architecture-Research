from fractions import Fraction as Fr
import mpmath as mp, hashlib
mp.mp.dps=50
b0=mp.mpf(1)/20
# constants
c=Fr(1,20)-Fr(1,20000)-Fr(8,10**8*200**2)
print("coef",c, c>Fr(499,10000), c-Fr(499,10000))
print("sq/2",Fr(499,10000)**2/2, "thr",mp.mpf(200000000)/249001)
def parts(n):
    n=mp.mpf(n); k=mp.floor(n/2); l=n-k; a=1-1/n; lam=1/(100*n); en=4/(mp.mpf(10)**8*n**2)
    cst=mp.sqrt(k)-1/(mp.sqrt(k)-1)
    mem=max(mp.mpf(0),b0*cst-a)
    L=(b0-lam)*mp.sqrt(l)-en*mp.sqrt(n)
    S=mp.sqrt(l*(b0-lam)**2+mem**2)-en*mp.sqrt(n)
    two=b0*mp.sqrt(l)-mp.sqrt(2)*en*mp.sqrt(n)
    return L,S,two,mem
# onset of memory term
on=[n for n in range(790,820) if parts(n)[3]>0][0]; print("memory onset n",on, parts(on-1)[3], parts(on)[3], b0*(mp.sqrt(401)-1/(mp.sqrt(401)-1))-(1-mp.mpf(1)/803))
# min margin of S vs b0 sqrt n - c for c=0.709, 0.71
worst={}
import math
for cc in ['0.709','0.7075','0.71','0.721']:
    cc=mp.mpf(cc); m=mp.inf; arg=None
    ns=list(range(200,20001))+[int(10**e) for e in [4.5,5,5.5,6,7,8,9,10,12,15,20,30]]
    for n in ns:
        L,S,two,mem=parts(n); v=max(S,two)-(b0*mp.sqrt(n)-cc)
        if v<m: m=v;arg=n
    print("c",cc,"min margin",mp.nstr(m,8),"at",arg)
# ratio L/(0.0499 sqrt(n/2)) min
m=min((parts(n)[0]/(mp.mpf('0.0499')*mp.sqrt(mp.mpf(n)/2)),n) for n in range(200,5000)); print("min ratio",m)
# thresholds per R
for R in [0.5,1,2,5,10,100]:
    R=mp.mpf(R)
    claimed=mp.mpf(200000000)/249001*R**2
    # first n>=200 from which S>R for all larger n (S increasing?) 
    lo=200
    n=200
    while max(parts(n)[1],parts(n)[2])<=R: n+=1 if n<5000 else max(1,int(n*0.001))
    print("R",R,"claimed",mp.nstr(claimed,10),"first n with S>R ~",n,"nonempty up to",mp.nstr(400*R**2,8),"400(R+.709)^2",mp.nstr(400*(R+mp.mpf('0.709'))**2,8))
C=mp.sqrt(2*(b0**2+(mp.atanh(mp.mpf(2)/5)-b0)**2)); print("C_abs",C)
# B_n sign
def B(n):
    n=mp.mpf(n);k=mp.floor(n/2);r=k-1;a=1-1/n;Lat=1/(1-1/(4*n));Cn=mp.sqrt(r/(4*n));en=4/(mp.mpf(10)**8*n**2)
    return b0*mp.sqrt(r)-(Lat+a)*Cn-en*mp.sqrt(n)
print("B399",B(399),"B400",B(400))
d=open('/home/user/AI-Architecture-Research/theory/codex_absolute_history_energy_20261003/ARITHMETIC.json','rb').read()
print("ARITH LF",hashlib.sha256(d).hexdigest()[:12],"CRLF",hashlib.sha256(d.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')).hexdigest()[:12])
