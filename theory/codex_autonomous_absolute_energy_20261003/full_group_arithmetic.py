"""Full-gradient normalization consistency; does not replay earlier outputs."""
from pathlib import Path
from fractions import Fraction as Q
import json
import time
import mpmath as mp

HERE=Path(__file__).resolve().parent
cpu,wall=time.process_time(),time.perf_counter()
checks=[]
def check(name,ok,detail):
    if not ok:
        raise ArithmeticError(name)
    checks.append({"name":name,"pass":True,"detail":detail})

e=Q(4,10**8*200**2)
check("beta_loss lower",3*(Q(1,2)+e)**2<Q(199,200)**2,"beta_loss>sqrt(n)/2, n>=200")
check("full-gradient epsilon allocation",Q(21,10)*Q(1,6)<Q(1,2),"2.1epsilon/6<epsilon/2")
check("full-gradient onset coefficient",12*10002==120024,"two epsilon/12 allocations")
check("W relative term condition",Q(2)**2*2==8,"n>=8R_abs^2 suffices")

def values(precision):
    with mp.workdps(precision):
        n=mp.mpf(10)**80; r=mp.mpf(1)
        L=int(mp.ceil(mp.log(100*mp.sqrt(n))/mp.log(mp.mpf(10001)/10000)))
        H=10000*(1+10000)**2+10000
        total=mp.mpf("1.1")*(L+H)/mp.sqrt(n)+2*r*(mp.sqrt(L)+mp.sqrt(H))/n
        return mp.nstr(total,45)
lo,hi=values(80),values(120)
check("80/120 decimal full-gradient agreement",lo==hi,hi)
with mp.workdps(80):
    check("full-gradient epsilon gate",mp.mpf(hi)<mp.mpf(1)/2000,hi)
result={"checks":checks,"count":len(checks),"n":"10^80","R_abs":1,
        "full_normalized_query_error_upper":hi,"CPU_seconds":time.process_time()-cpu,
        "wall_seconds":time.perf_counter()-wall,"GPU_seconds":0,"CUDA_used":False,
        "scope":"same frozen bounded-energy family only; full-model worst-case gap unchanged"}
path=HERE/"FULL_GROUP_ARITHMETIC.json"
if path.exists():
    raise FileExistsError("Preserve previous output")
path.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,indent=2))
