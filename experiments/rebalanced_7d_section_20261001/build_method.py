"""Mechanical pre-freeze generation of two auditable affine-bound replacements."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent; EXPS=ROOT.parent
old=EXPS/'third_order_antipodal_20261001/kernel.py'
assert hashlib.sha256(old.read_bytes()).hexdigest()=='c2483d3585dccb36b7dfba945c1a0cb2964a59f440161a7663c594bd4d928578'
src=old.read_text()
a="        pre=[sum((RI[i][j]*hh[j]+WI[i][j]*xx[j] for j in range(n)),b[i]) for i in range(n)]"
b="""        # Exact signed affine input combination, before interval absolute values.
        affine=[[sum((WI[i][j]*base['BI'][t*n+j][k] for j in range(n)),I(0)) for k in range(s)] for i in range(n)]
        inputcenter=[sum((WI[i][j]*base['X'][t][j] for j in range(n)),I(0)) for i in range(n)]
        inputrad=[sum((v.absq()*amps[k] for k,v in enumerate(row)),Q(0)) for row in affine]
        pre=[sum((RI[i][j]*hh[j] for j in range(n)),b[i])+inputcenter[i]+I(-inputrad[i],inputrad[i]) for i in range(n)]"""
# I accepts exact endpoints via its raw-integer constructor, not two Fractions.
b=b.replace('I(-inputrad[i],inputrad[i])',"I(-I(inputrad[i]).hi,I(inputrad[i]).hi,True)")
c='        ax=upadd(left(R,hx),left(W,u)); ax2=left(R,h2); ax3=left(R,h3)'
d='        ax=upadd(left(R,hx),np.array([[uq(v.absq()) for v in row] for row in affine])); ax2=left(R,h2); ax3=left(R,h3)'
assert src.count(a)==1 and src.count(c)==1
assert not (ROOT/'kernel.py').exists()
(ROOT/'kernel.py').write_text(src.replace(a,b).replace(c,d),encoding='utf-8',newline='\n')
p=EXPS/'antipodal_robust_dimension_20261001/stage2_proxy/screen_proxy3.py'
srcp=p.read_text(); ap='ax = Ra @ hx + Wa @ u;'
bp='ax = Ra @ hx + np.abs(ep.W @ Bs[t*n:(t+1)*n]);'
cp='nl = np.tanh(Rp @ hl + Rm @ hh + Wp @ lo[t] + Wm @ hi[t] + ep.b); nh = np.tanh(Rp @ hh + Rm @ hl + Wp @ hi[t] + Wm @ lo[t] + ep.b)'
dp='inputrad = (np.abs(ep.W @ Bs[t*n:(t+1)*n])*amps[None,:]).sum(1); center=ep.W @ ep.X[t]; nl = np.tanh(Rp @ hl + Rm @ hh + center-inputrad + ep.b); nh = np.tanh(Rp @ hh + Rm @ hl + center+inputrad + ep.b)'
assert srcp.count(ap)==1 and srcp.count(cp)==1
(ROOT/'screen_proxy3.py').write_text(srcp.replace(ap,bp).replace(cp,dp),encoding='utf-8',newline='\n')
(ROOT/'SOURCE_TRANSFORM.json').write_text(json.dumps({'accepted_kernel_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),
    'kernel_replacements':[[a,b],[c,d]],'proxy_source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
    'proxy_replacements':[[ap,bp],[cp,dp]],'proof':'PROOF_AFFINE.md'},indent=2),encoding='utf-8',newline='\n')
print('Generated exactly two nominal-affine replacements in each local source')
