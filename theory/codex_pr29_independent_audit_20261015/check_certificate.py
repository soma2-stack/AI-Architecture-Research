"""Independent PR29 certificate; no author imports. CPU, Python standard library.

Majorant algebra uses exact Fractions. Transcendentals use Decimal at 100 digits;
the independent front-chain bound is deliberately relaxed to z_20000 < 1e-23
and a geometric tail. A second precision run checks numerical stability.
"""
from fractions import Fraction as Q
from decimal import Decimal as D, localcontext
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent


def elimination(A, b):
    a = [list(row) + [v] for row, v in zip(A, b)]
    for j in range(len(b)):
        pivot = next(i for i in range(j, len(b)) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        p = a[j][j]
        a[j] = [v / p for v in a[j]]
        for i in range(len(b)):
            if i != j:
                p = a[i][j]
                a[i] = [u - p*v for u, v in zip(a[i], a[j])]
    return [row[-1] for row in a]


def exact_majorant():
    # Rounded upward, certified by squaring: no floating point in the certificate.
    q = Q(1154700538379252, 10**24)
    assert q*q >= Q(1, 750000000000000000)
    gamma = 1/(1-q)
    rs = Q('0.707106781186548')
    assert rs*rs >= Q(1,2) + 194*q*q
    s2, oh, od = Q('.0024959'), Q('346.70'), Q('258.79')
    sigma = dbar = Q(314)
    lam, mu, mud, w = Q(120401), Q('1.424'), Q('1.246'), Q('.50347')
    front_over_q = Q(1,10**230)
    # Evaluate the *unscaled* six recurrences, then conjugate by the scaling.
    def envelope(x):
        z, b, s, zm, bm, sm = (q*x[0], x[1], x[2]/q, q*x[3], x[4], x[5]/q)
        arrival, am = od+z, oh+zm
        leak = b+sigma*z+Q('1.41')*od+mu*(oh+zm)+w
        leakm = bm+sigma*(oh+zm)
        out = [
            q*front_over_q*b + gamma*q*(dbar+gamma*sigma*lam*q*q)*arrival
            + gamma*q*(mud+gamma*mu*lam*q*q)*am
            + gamma*lam*q*q*(leak+s2*s) + mud*zm,
            arrival+q*(leak-w+s2*s)+gamma*q*q*(sigma*arrival+mu*am)+q*w,
            z+(gamma*q*(s2+gamma*sigma*q*q)*arrival
               +gamma*gamma*mu*q**3*am+gamma*q*q*leak)/(2*q*q),
            q*front_over_q*bm+gamma*q*(dbar+gamma*sigma*lam*q*q)*am
            +gamma*lam*q*q*(leakm+s2*sm)+gamma*lam*q,
            am+q*(leakm+s2*sm)+gamma*q*q*sigma*am+1,
            rs/q+zm+(gamma*q*(s2+gamma*sigma*q*q)*am
                     +gamma*q*q*leakm+gamma*q)/(2*q*q),
        ]
        return [out[0]/q,out[1],q*out[2],out[3]/q,out[4],q*out[5]]
    zero = [Q(0)]*6
    b = envelope(zero)
    cols = []
    for j in range(6):
        e = zero.copy(); e[j] = 1
        cols.append([v-u for v,u in zip(envelope(e),b)])
    M = [list(row) for row in zip(*cols)]
    assert all(v >= 0 for row in M for v in row)
    identity_minus_M = [[Q(i==j)-M[i][j] for j in range(6)] for i in range(6)]
    x = elimination(identity_minus_M, [v+Q(1,10**7) for v in b])
    residual = [u-v for u,v in zip(x,envelope(x))]
    assert min(residual) == max(residual) == Q(1,10**7)
    assert min(x) > 0
    claimed = list(map(Q,['368090','258.80','.32296','229780','347.71','1.6399']))
    assert all(v <= u for v,u in zip(x,claimed))
    # Exact weighted-infinity-norm proof of rho(M)<1; no numerical eigenvalues needed.
    contraction = max(sum(M[i][j]*x[j] for j in range(6))/x[i] for i in range(6))
    assert contraction < 1
    zh,B,Sh,zmh,Bm,Smh = claimed
    EY = q*zh + gamma/2*(s2+gamma*sigma*q*q)*zh
    EY += gamma*gamma*mu*q/2*(oh+q*zmh)
    EY += gamma/2*(B+sigma*q*zh+Q('1.41')*od+mu*(oh+q*zmh)+w)
    assert EY < 1019
    # Proposition 0.2 adds one scalar. Even at the smallest D=36000,
    # the inherited strict coefficient margins absorb the factor 1-2/D.
    retention=1-Q(2,36000)
    assert Q('.001')/Q(18*1171000)*retention>Q('4.7e-11')
    assert Q('.001')/Q(12*1511000)*retention>Q('5.5e-11')
    assert Q('5.6e-10')**2 < retention/(Q(1511000)**2*6*232000)
    return {
        'q_upper_exact': str(q), 'supersolution': [float(v) for v in x],
        'six_exact_slacks': [str(v) for v in residual],
        'weighted_matrix_norm_upper': float(contraction), 'EY_upper': float(EY),
        'M': [[float(v) for v in row] for row in M],
        'b': [float(v) for v in b],
    }


def decimal_constants(precision):
    with localcontext() as ctx:
        ctx.prec = precision
        def tanh(t):
            e = (2*t).exp()
            return (e-1)/(e+1)
        n = D(1500000000000000000); k=n/2; q=1/k.sqrt(); gamma=1/(1-q)
        t05=tanh(D('.05')); slo=t05-D('1.5e-9'); shi=t05+D('1.5e-9')
        gate=1-slo*slo
        z=D(1); sumz=z; sumdelta=D(0)
        for _ in range(19999):
            z=gate*tanh(z); sumz+=z; sumdelta+=z*(z+2*shi)
        tail=z*gate/(1-gate)
        sumz+=tail; sumdelta+=tail*(z+2*shi)
        assert sumz<D('51.7') and sumdelta<D('11.82') and z<D('1e-22')
        mass=sumz+D('.0501')*120009
        # Derive epsilon from beta exactly, not assuming the displayed 1.2q.
        # |h(d-1)|<=1, |s|<=shi, |M|<=6350.
        eps_bound=shi/n+gamma*q*(1+2*shi)+gamma*gamma*q*q*6350
        assert eps_bound<D('1.2')*q<D('1.4e-9')
        assert eps_bound+shi/n<D('1.5e-9')
        beta_lo=D('.05')-shi-D('1.4e-9'); beta_hi=D('.05')-slo+D('1.4e-9')
        assert beta_lo>D('4.1622e-5') and beta_hi<D('4.1628e-5')
        # Front preactivation: beta + a*gamma*((k-1)*s+M)/sqrt(k).
        front=beta_lo+(1-1/n)*gamma*((k-1)*slo-6350)/k.sqrt()
        assert front>D('.0498')*k.sqrt()
        assert D(4).ln()+k.sqrt().ln()-D('.0996')*k.sqrt() < -230*D(10).ln()
        wake=D(1)
        for _ in range(5): wake=tanh(wake+beta_hi)
        spike_input=wake+beta_hi
        hi=1-tanh(D('.25'))**2
        mod=1-(1-tanh(D('.45'))**2)**7
        s2lo=D('.0024958'); s2hi=D('.0024959')
        sig=1+sumdelta+120001*s2hi+8*D('.1756')
        dbar=1+sumdelta+119993*s2hi+7*D('.1756')
        own=(D(120000)+(1-s2lo)**2/(1-(1-s2lo)**2)).sqrt()
        assert sig<314 and dbar<314 and own<D('346.70') and mod*own<D('258.79')
        W=int(((30+n.ln())/D('.00015')).to_integral_value(rounding='ROUND_CEILING'))
        T=int(n/4)+120000+W+32
        count=int(n/4)-W-24; count-=count%2
        # log(1-1/n)>=-1/(n-1) supplies a rigorous, directly evaluated lower bound.
        apower=(-D(T+120002)/(n-1)).exp()
        rho=1-gamma*s2hi*D(T)/k
        coefficient=hi*mod*rho*apower*(s2lo-gamma*314/k)*(1-D('1e-12'))*D(count)/n
        main=coefficient*D(119990).sqrt()
        err=hi*1019/(2*n).sqrt()
        tau_upper=D('.002')*D(2).sqrt()/t05
        margin=D('.11791')-D('5.6e-7')
        ratio=margin/tau_upper
        assert main>D('.11791') and err<D('5.6e-7')
        assert D(120001)*T/n < 30012
        assert D(120001)*T < D('.000025')*n*n.sqrt()
        assert margin/tau_upper>D('2.0826')
        # The rounded .11790/.05662 alone does NOT imply 2.0826.
        vals=dict(front_sum=sumz,front_gate_sum=sumdelta,mass_bound=mass,eps_bound=eps_bound,
                  spike_start_input=spike_input,own_norm=own,own_difference_norm=mod*own,
                  Sigma=sig,Dbar=dbar,main_coefficient=main,error_over_n=err,tau_over_n_upper=tau_upper,
                  final_ratio_lower=ratio,coarse_ratio=D('.11790')/D('.05662'),
                  budget_over_n=D(120001)*T/n,Wtail=D(W),T=D(T),arrivals=D(count))
        return {key:str(value) for key,value in vals.items()}


if __name__=='__main__':
    certificate=exact_majorant()
    low=decimal_constants(70); high=decimal_constants(100)
    for key in low:
        assert abs(D(low[key])-D(high[key])) < max(D(1),abs(D(high[key])))*D('1e-55'),key
    result={'exact_majorant':certificate,'decimal_constants_100_digits':high,
            'precision_crosscheck':'70 vs 100 digits, agreement < 1e-55 relative/absolute',
            'status':'Exact rational majorant certified; transcendental constants independently reproduced.'}
    (OUT/'certificate_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
