"""Independent precision replay of frozen selected certificate constants."""
import json,sys,hashlib
from fractions import Fraction as Q
import mpmath as mp
import engine as e

def load(n,case,bits,meter):
    e.I.precision(bits);mp.mp.dps=e.CFG['svd_digits']
    saved=json.loads((e.ROOT/f'basis_{case}_n{n}.json').read_text())
    data=json.loads((e.REPO/e.prior.CFG['dense_certificates'][str(n)]).read_text())
    model=e.prior.model_at(data,n,case=='independent');X=[[Q(x) for x in row] for row in data['X']]
    if case=='dense':
        JI=[[e.I((int(lo)*e.I.scale)//(1<<data['bits']),-((-int(hi)*e.I.scale)//(1<<data['bits'])),True)
             for lo,hi in row] for row in data['J_intervals']]
    else:
        _,J,_=e.prior.archived.jets(model,X,'interval');JI=J.tolist()
    B=[[Q(x) for x in row] for row in saved['B']];U=[[Q(x) for x in row] for row in saved['U']]
    scaleI={name:e.I(sum(Q(model.params[p])**2 for p,(_,_,g,_) in enumerate(model.meta) if g==name)/
                    sum(g==name for _,_,g,_ in model.meta)).sqrt() for name in ('R','W','b')}
    sd=e.I(Q(3,32)).sqrt();BI=[[e.I(x)*sd for x in row] for row in B]
    reduced=e.matmul(JI,BI)
    for j,(_,p) in enumerate(model.support):reduced[n+j]=[x*scaleI[model.meta[p][2]] for x in reduced[n+j]]
    return {'model':model,'X':X,'n':n,'D':saved['D'],'U':U,'B':B,'BI':BI,'JI':JI,'reduced':reduced,
            'scaleI':scaleI,'sigma':[e.dyadic(mp.mpf(x)) for x in saved['singular_values']],'spectra':saved}

def verify_one(cert,meter):
    n=cert['n'];r=cert['r'];case=cert['case']
    base=load(n,case,e.CFG['second_interval_bits'],meter)
    L=[[Q(x) for x in row] for row in cert['selected_projection']]
    Kh=[[Q(x) for x in row] for row in cert['K_hidden']];K=[[Q(x) for x in row] for row in cert['K_selected']]
    J=[row[:n+r] for row in base['reduced']];H0=[row[:n] for row in J[:n]];Ht=[row[n:] for row in J[:n]]
    Jp=e.matmul([[e.I(x) for x in row] for row in L],J[n:]);cross=e.matmul([row[:n] for row in Jp],e.matmul(e.inverse(H0),Ht))
    C0=[[Jp[i][n+j]-cross[i][j] for j in range(r)] for i in range(r)]
    mu,_=e.query_margins(base,L)
    key=(e.I.bits,r,tuple(tuple(row) for row in L))
    base['_center_cache']={key:(Kh,e.abs_array(Kh),e.residual(Kh,H0),K,e.residual(K,C0),mu)}
    out=e.certify(base,r,Q(cert['a0']),cert['profile'],Q(cert['hidden_factor']),L,True)
    assert out['valid'],out
    rho=list(map(Q,cert['rho_i']));oldmu=list(map(Q,cert['mu_i']));aa=list(map(Q,cert['a_i']))
    assert all(sum(abs(K[j][i])*rho[i] for i in range(r))<=(1-Q(out['eta_sensitivity']))*aa[j] for j in range(r))
    assert all(x<=y for x,y in zip(oldmu,mu))
    counts=[int(2*x*y//(Q(e.CFG['strict_spacing_epsilon_multiplier'])*Q(e.CFG['epsilon_primary'])))+1 for x,y in zip(rho,oldmu)]
    assert counts==cert['N_i']
    return {'case':case,'n':n,'r':r,'verified':True,'interval_bits':e.I.bits,'fixed_preconditioners_replayed':True,
            'original_product_verified':True,'original_query_margins_verified':True,
            'eta_higher_precision':out['eta_sensitivity'],'eta_hidden_higher_precision':out['eta_hidden'],
            'N_i':counts,'center_inverse_residual_inf':float(max(e.upsum(e.residual(K,C0),axis=1))),
            'certificate_sha256':hashlib.sha256(json.dumps(cert,sort_keys=True).encode()).hexdigest()}

def main(mode):
    meter=e.Meter('selected '+mode+' certificates 256-bit independent replay');e.prior.archived.ACTIVE_METER=meter
    try:
        certificates=json.loads((e.ROOT/f'results_{mode}.json').read_text());rows=[]
        for cert in certificates:
            meter.check();row=verify_one(cert,meter);rows.append(row);print(row,flush=True)
        (e.ROOT/f'verification_{mode}.json').write_text(json.dumps(rows,indent=2))
    finally:meter.finish()
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'svd')
