"""Small independent algebra checks; no robust-dimension inference from samples."""
import os
POOLS = (
    "OMP_NUM_THREADS", "OMP_THREAD_LIMIT", "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS", "TBB_NUM_THREADS"
)
for name in POOLS:
    os.environ[name] = "1"
os.environ["OMP_DYNAMIC"] = "FALSE"
os.environ["MKL_DYNAMIC"] = "FALSE"
os.environ["OMP_MAX_ACTIVE_LEVELS"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["NVIDIA_VISIBLE_DEVICES"] = "void"

from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib
import json
import time
import psutil

HERE = Path(__file__).resolve().parent
PROC = psutil.Process()
CPU0 = sum(PROC.cpu_times()[:2])
WALL0 = time.perf_counter()
CHECKS = []
PEAK_THREADS = 0
PEAK_RAM = 0

def guard():
    global PEAK_THREADS, PEAK_RAM
    PEAK_THREADS = max(PEAK_THREADS, PROC.num_threads())
    PEAK_RAM = max(PEAK_RAM, PROC.memory_info().rss)
    if PEAK_THREADS > 8 or PEAK_RAM > 100 * 1024**2 or PROC.children():
        raise RuntimeError("Resource stop; no retry with more resources")

def check(name, condition, **data):
    guard()
    CHECKS.append(dict(name=name, passed=bool(condition), data=data))
    if not condition:
        raise AssertionError(name)

def dot(x, y):
    return sum((a*b for a,b in zip(x,y)), F(0))

def cone_checks(K):
    gamma = F(10001, 10000)
    donor_w = F(1,500*K)
    weights = [donor_w]*K + [F(1,500), gamma-F(1,250)]
    survivor = K
    nonS = [i for i in range(K+2) if i != survivor]
    forcing = [F(0)]*(K+2)
    forcing[0] = F(K)
    forcing[survivor] = F(-1)
    check(f"K{K} weighted forcing balance", dot(weights,forcing)==0)
    state = [F(0)]*(K+2)
    deriv = [F(0)]*(K+2)
    idle = 1
    # Exact rational, genuinely changing bath; no floating-point sign test.
    for t in range(32):
        gates = [F(199,200)] + [
            F(199,200)+F((t+3*i)%11,2200)
            for i in range(1,K)
        ] + [F(1), F(9989+(t%3),10000)]
        B = sum(weights[i]*(1-gates[i]) for i in nonS)
        check(f"K{K} positive coefficients step{t}", B-(gamma-1)>F(6,10000))
        S = dot(weights,state)
        stepS = (
            (1-dot(weights,gates))*S
            +sum(weights[i]*(gates[i]-1)*state[i] for i in nonS)
            +F(1,500)*(gates[0]-1)
        )
        newstate = [gates[i]*(state[i]-S+forcing[i]) for i in range(K+2)]
        check(f"K{K} forced mass identity step{t}", dot(weights,newstate)==stepS)
        check(f"K{K} invariant forcing cone step{t}",
              stepS<=0 and all(newstate[i]>=0 for i in nonS))
        # Each idle impulse uses the exact same chronological gate matrix.
        impulse = [F(0)]*(K+2)
        impulse[idle] = F(1)
        SI = dot(weights,impulse)
        U = -impulse[survivor]
        r = [impulse[i]+U for i in nonS]
        P = U+SI
        for j in range(7):
            gj = [F(199,200)] + [
                F(199,200)+F((t+j+3*i)%11,2200)
                for i in range(1,K)
            ] + [F(1), F(9989+((t+j)%3),10000)]
            B = sum(weights[i]*(1-gj[i]) for i in nonS)
            SI = dot(weights,impulse)
            expected = [gj[i]*(impulse[i]-SI) for i in range(K+2)]
            rn = [gj[i]*r[q]+(1-gj[i])*P for q,i in enumerate(nonS)]
            Pn = sum(weights[i]*gj[i]*r[q] for q,i in enumerate(nonS))+(B-(gamma-1))*P
            Un = P
            from_positive = [F(0)]*(K+2)
            from_positive[survivor] = -Un
            for q,i in enumerate(nonS):
                from_positive[i] = rn[q]-Un
            check(f"K{K} chronological cone identity t{t} j{j}",
                  expected==from_positive and expected[survivor]<=0
                  and min(rn)>=0 and Pn>=0)
            impulse, r, P, U = expected, rn, Pn, Un
        state = newstate

def probe_checks():
    for K in range(1,33):
        P = [[F(1,K) for j in range(K)] for i in range(K)]
        G = [[F(i==j)+P[i][j] for j in range(K)] for i in range(K)]
        inverse = [[F(i==j)-P[i][j]/2 for j in range(K)] for i in range(K)]
        product = [[sum(G[i][s]*inverse[s][j] for s in range(K))
                    for j in range(K)] for i in range(K)]
        check(f"K{K} exact Gram inverse",product==[
            [F(i==j) for j in range(K)] for i in range(K)])
        b = [F(i==0)+F(1,K) for i in range(K)]
        bnorm = sum(b[i]*inverse[i][j]*b[j] for i in range(K) for j in range(K))
        # Set m=1 algebraically; formula is homogeneous in physical support.
        prefactor_sq = F(2,K)/(F(2)+F(2,K))**2
        check(f"K{K} exact joint axis dilution",
              prefactor_sq*bnorm==F(1,2*(K+1)))
        gap_sq = F(K*K,2*(K+1)*(2*K-1)**2)
        check(f"K{K} exact worst-idle lower coefficient",gap_sq>=F(1,8*K))

def mask_checks():
    R=4
    labels = range(2**R)
    def character(bits):
        return [F((-1)**sum((j>>(e-1))&1 for e in bits)) for j in labels]
    lo=F(199,200); hi=F(99999,100000)
    for e in range(2,R+1):
        for f in range(1,e):
            char=character({f})
            mask=character({e})
            image=[(hi if mask[i]==1 else lo)**5 * char[i] for i in labels]
            A=(hi**5+lo**5)/2
            B=(hi**5-lo**5)/2
            expected=[A*x+B*y for x,y in zip(character({f}),character({f,e}))]
            check(f"Walsh fresh mask f{f} e{e}",
                  image==expected and sum(image)==0
                  and dot(image,character({e}))==0)
    same=character({1})
    broken=[(hi if same[i]==1 else lo)*same[i] for i in labels]
    check("reused bit fails zero-sum protection",sum(broken)!=0)

def full_front_bank_check():
    # Exact rational structural test, not an admitted large-n history.
    # Deliberately use a pre-existing front, to catch false fresh-stage resets.
    n=800; k=400; r=k-1; d=200; m=8; K=2; N=32
    a=F(n-1,n); c=F(1,361); hv=F(1,19)
    def sites(global_time):
        return [[50+i+global_time,110+i+global_time,d+2*i+2,d+2*i+3]
                for i in range(m)]
    def rotate(x):
        out=x.copy()
        out[0]=F(0)
        out[1:d-1]=x[:d-2]
        J=hv*x[d-2]-c*sum(x)
        B=hv*sum(x)
        out=[v+J for v in out]
        out[0]+=B
        return out
    groups=[range(0,2),range(2,4),range(4,8)]
    sizes=[8,8,16]
    weights=[c*h for h in sizes]+[F(20,19)-4*m*c]
    probe=[F(0)]*r
    for i,ss in enumerate(sites(10)):
        for z in ss[2:]:
            probe[z-1]=F(1) if i<2 else (F(-1,2) if i>=4 else F(0))
    forcing=[F(1,2),F(0),F(-1,4),F(0)]
    x=[F(0)]*r
    observed=[F(0)]*4
    truncated_failed=False
    for fresh in range(1,9):
        global_time=10+fresh
        q=F(9988+2*(fresh%2),10000)
        group_g=[F(199,200),F(997,1000),F(1999,2000),q]
        Jprev=hv*x[d-2]-c*sum(x)
        Zprev=x[d-2]
        rho=-c*sum(x[z-1]-Zprev for z in range(1,N+1))
        check(f"full-front group J identity fresh{fresh}",
              Jprev==-dot(weights,observed)+rho)
        rho_bad=-c*sum(x[z-1]-Zprev for z in range(1,fresh))
        if rho_bad!=rho:
            truncated_failed=True
        expected=[group_g[i]*(a*(observed[i]+Jprev)+forcing[i])
                  for i in range(4)]
        G=[q]*r
        for z in range(1,global_time+1):
            G[z-1]=F(1,100) if z==1 else q-F(1,1000*(z+1))
        for g,rows in zip(group_g[:3],groups):
            for i in rows:
                for z in sites(global_time)[i]:
                    G[z-1]=g
        ox=rotate(x)
        x=[G[i]*(a*ox[i]+probe[i]) for i in range(r)]
        observed=[
            sum(x[z-1] for i in rows for z in sites(global_time)[i])/h
            for rows,h in zip(groups,sizes)
        ]+[x[d-2]]
        check(f"full-front exact group recurrence fresh{fresh}",observed==expected)
    check("fresh-time front truncation genuinely fails",truncated_failed)

def envelope_checks():
    # Scalar evaluation supplements the analytic every-width proof.
    with localcontext() as ctx:
        ctx.prec=80
        n=Decimal(10)**1000
        L=n.ln()
        vals = {
            "front": Decimal("4e13")*n**(-Decimal(1)/16),
            "complement": Decimal(6000)*n**(-Decimal(1)/4),
            "tail": Decimal(25000)*L*n**(-Decimal(5)/32),
            "mask": Decimal(50000)*L*n**(-Decimal(5)/32),
            "erased": Decimal(3)*n**(-9)+Decimal(1300)*n**(-Decimal(5)/32),
            "trace": Decimal(100)*n**(-Decimal(63)/16),
            "geometry": Decimal(401)*(n**(-Decimal(1)/2)+Decimal(11)*n**(-Decimal(3)/32)+4/n),
            "quantile": Decimal(16000)*Decimal(11).sqrt()*n**(-Decimal(3)/64),
            "high_gate_loss": Decimal(22)*n**(-Decimal(3)/32),
        }
        for key in ("front","complement","tail","mask","erased","trace"):
            check(f"threshold scalar envelope {key}",vals[key]<Decimal("1e-6"),
                  value=str(vals[key]))
        check("threshold geometry envelope",vals["geometry"]<1,value=str(vals["geometry"]))
        check("threshold p=1 envelope",vals["quantile"]<1,value=str(vals["quantile"]))
        check("threshold high-gate envelope",vals["high_gate_loss"]<Decimal(".001"),
              value=str(vals["high_gate_loss"]))
        signal=Decimal(".0499")*Decimal(".99")*Decimal(".17")*Decimal(".16")*Decimal(".998")*10*Decimal(".994")
        check("exact conservative pair signal",signal==Decimal(".013329736668864")
              and signal-Decimal("9e-9")>Decimal(".012"),value=str(signal))

guard()
check("one thread numerical pools / no GPU",all(os.environ[k]=="1" for k in POOLS)
      and os.environ["CUDA_VISIBLE_DEVICES"]=="")
probe_checks()
full_front_bank_check()
for K in (2,3,5):
    cone_checks(K)
mask_checks()
envelope_checks()
guard()
result = dict(
    status="PASS", checks=CHECKS,
    exact_rational_algebra=True,
    scalar_values_are_checks_not_proof=True,
    cpu_seconds=sum(PROC.cpu_times()[:2])-CPU0,
    wall_seconds=time.perf_counter()-WALL0,
    peak_observed_process_threads=PEAK_THREADS,
    peak_observed_rss_bytes=PEAK_RAM,
    gpu_cuda_calls=0, workers=0, pools={k:os.environ[k] for k in POOLS},
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
)
(HERE/"checks_result.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in result.items() if k!="checks"},indent=2))
print(f"{len(CHECKS)} independent algebra checks passed")
