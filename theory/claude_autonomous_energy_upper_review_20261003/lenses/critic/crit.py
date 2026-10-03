from mpmath import mp, mpf, log, sqrt, ceil, atanh, tanh
mp.dps=80
def L(n): return int(ceil(log(100*sqrt(n))/log(mpf(10001)/10000)))
def BR(R): return int(ceil(10000*(1+10000*mpf(R))**2))
def HR(R): return BR(R)+10000
def d0(n,R):
    l=n-n//2
    return sqrt(l)*(L(n)+HR(R))/n
eps=mpf('0.001')
# kappa^L sqrt n <= m/2
for n in [10**6,10**30,10**80]:
    print(n==10**6 and 'n=1e6' or n, L(n), (mpf(10000)/10001)**L(n)*sqrt(n) <= mpf(1)/100)
print('BR(1),HR(1)',BR(1),HR(1))
# integer bisection for smallest n with d0<=eps/2 (R=1), check neighbors
lo,hi=10**29,10**31
while hi-lo>1:
    mid=(lo+hi)//2
    if d0(mid,1)<=eps/2: hi=mid
    else: lo=mid
print('n* approx',hi, mp.nstr(mpf(hi),10), d0(hi,1)<=eps/2, d0(hi-1,1)<=eps/2)
print('d0(1e80,1)=',mp.nstr(d0(10**80,1),12),' coarse', mp.nstr((L(10**80)+HR(1))/sqrt(10**80),12))
# (38) terms
print('(40008/eps)^(20/9)=',mp.nstr((40008/eps)**(mpf(20)/9),6),' (4H/eps)^2=',mp.nstr((4*HR(1)/eps)**2,6))
# (39) coefficient
for e in [40,80,200]:
    n=mpf(10)**e
    Rreq=(sqrt((eps*sqrt(n)-10002*log(n)-10001)/10000)-1)/10000
    print('1e%d'%e,'Rreq',mp.nstr(Rreq,8),'Rreq/n^.25',mp.nstr(Rreq/n**mpf(0.25),12),'sqrt(eps)/1e6',mp.nstr(sqrt(eps)/10**6,12))
# Lemma 2 tightness at z=-p/2
for p in [mpf(1)/50, mpf('0.5'), mpf('0.99')]:
    z=-p/2
    print('p',p,'secant/(1+p^2/4)', mp.nstr((atanh(z)-atanh(p))/(z-p)/(1+p**2/4),15))
# B* limit
b0=mpf(1)/20
print('b0-tanh b0',mp.nstr(b0-tanh(b0),10))
# L_n <= 10002 log n threshold
print('log n threshold',mp.nstr((10001*log(100)+1)/mpf('5001.5'),8))
# kappa constants
k=mpf(10000)/10001
print('m/(2sqrt(1-k^2))',mp.nstr(mpf(1)/100/sqrt(1-k**2),10),'k/(1-k)',k/(1-k),'k/sqrt(1-k^2)',mp.nstr(k/sqrt(1-k**2),10))
# Theorem 1 constants
m0=mpf(1)/40
n=10**6
Bm=atanh(m0)-(1-mpf(1)/n)*m0
print('B_m',mp.nstr(Bm,10),'(1-m0)/m0^2',(1-m0)/m0**2)
print('Phi bound',mp.nstr(mpf(1)/100000-b0+mpf(201)/200*(m0+mpf(1600)/500000),10))
