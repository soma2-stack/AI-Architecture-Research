"""Remove weak axes using the UNCHANGED global majorant, as a comparator.

This is not the primary anisotropic method, and no accepted theorem is reproved.
All centers/preconditioners/residuals and radius inequalities are enclosed.
"""
import json,math,importlib.util
from fractions import Fraction as Q
import engine as e
spec=importlib.util.spec_from_file_location('current_verify',e.ROOT/'verify.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def sparse_residual(K,J):
    size=len(K);eta=Q(0)
    for i,row in enumerate(K):
        nz=[(k,x) for k,x in enumerate(row) if x]
        total=Q(0)
        for j in range(size):
            value=e.I(int(i==j))-sum((x*J[k][j] for k,x in nz),e.I(0))
            total+=value.absq()
        eta=max(eta,total)
    return eta

def main():
    meter=e.Meter('rigorous weak-axis removals with unchanged global majorant');e.prior.archived.ACTIVE_METER=meter
    try:
        rows=[]
        for n in e.CFG['widths']:
            for case in ('dense','independent'):
                meter.check();base=v.load(n,case,192,meter);D=base['D'];model=base['model']
                R=[[Q(0) for _ in range(n)] for _ in range(n)];W=[[Q(0) for _ in range(n)] for _ in range(n)]
                for i,j,p in model.layers[0]['R']:R[i][j]=model.params[p]
                for i,j,p in model.layers[0]['W']:W[i][j]=model.params[p]
                params=sum(R,[])+sum(W,[])+[model.params[p] for i,j,p in model.layers[0]['b']]
                bx=max(sum(x.absq() for x in row) for row in base['BI'])
                Lraw,_,_=e.prior.hessian_bounds(params,n,len(base['X']),max(abs(x) for row in base['X'] for x in row)+bx)
                norms=[sum(abs(x)*Q(base['scaleI'][model.meta[p][2]].hi,e.I.scale) for x,(_,p) in zip(row,model.support)) for row in base['U']]
                L=Lraw*bx*bx*max(Q(1),max(norms))
                # Full projection center reused, not recomputed for each prefix.
                top=base['reduced'][:n]
                selected=e.matmul([[e.I(x) for x in row] for row in base['U']],base['reduced'][n:])
                Kh=e.mpinverse([row[:n] for row in top]);mu,_=e.query_margins(base,base['U'])
                prefixes=sorted(set([D,D-1,math.ceil(.95*D),math.ceil(.9*D)]+[x for x in (1,4,8,16) if x<=D]))
                case_rows=[]
                for r in prefixes:
                    meter.check();size=n+r;J=[row[:size] for row in top]+[row[:size] for row in selected[:r]]
                    K=[list(row)+[Q(0)]*r for row in Kh]
                    for i in range(r):
                        invsig=1/base['sigma'][i]
                        normal=[-invsig*sum(selected[i][k].midq()*Kh[k][j] for k in range(n)) for j in range(n)]
                        K.append(normal+[invsig if i==j else Q(0) for j in range(r)])
                    eta=sparse_residual(K,J);assert eta<1
                    normK=max(sum(abs(x) for x in row) for row in K)
                    a=min(Q(1),(1-eta)/(2*normK*L));rho=(1-eta)*a/(2*normK)
                    # This is a product in selected projections at fixed h,
                    # with the global-ball certificate's common rho/2 radius.
                    safe=rho/2;epsilon=Q(e.CFG['epsilon_primary']);step=Q(e.CFG['strict_spacing_epsilon_multiplier'])*epsilon
                    N=[int(2*safe*m//step)+1 for m in mu[:r]]
                    row={'case':case,'n':n,'retained':r,'discarded':D-r,'global_hessian_majorant_exact':str(L),
                         'inverse_norm_exact':str(normK),'center_residual_exact':str(eta),'input_common_radius_exact':str(a),
                         'output_common_radius_exact':str(safe),'output_common_radius':float(safe),
                         'N_i':N,'bits':float(e.mp.log(math.prod(N),2)),'label':'CERTIFIED sufficient global-majorant comparator'}
                    case_rows.append(row)
                full=next(x for x in case_rows if x['retained']==D)
                for row in case_rows:row['radius_improvement_exact']=str(Q(row['output_common_radius_exact'])/Q(full['output_common_radius_exact']))
                rows+=case_rows
                print(case,n,'common radii',[(x['retained'],x['output_common_radius']) for x in case_rows],flush=True)
        (e.ROOT/'weak_axis_certificates.json').write_text(json.dumps(rows,indent=2))
    finally:meter.finish()
if __name__=='__main__':main()
