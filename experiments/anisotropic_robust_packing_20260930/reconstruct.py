"""Numerical grid reconstruction check, separate from rigorous certificates."""
import itertools,json,math
from fractions import Fraction as Q
import numpy as np
import mpmath as mp
import engine as e
import importlib.util
spec=importlib.util.spec_from_file_location('current_verifier',e.ROOT/'verify.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def main():
    meter=e.Meter('selected product-grid numerical reconstruction cross-check');e.prior.archived.ACTIVE_METER=meter
    try:
        p=json.loads((e.ROOT/'results_svd.json').read_text());s=json.loads((e.ROOT/'results_frame.json').read_text());rows=[]
        for primary in p:
            meter.check();sec=next(x for x in s if x['case']==primary['case'] and x['n']==primary['n'])
            cert=sec if int(sec['states'])>int(primary['states']) else primary
            n,r=cert['n'],cert['r'];base=v.load(n,cert['case'],192,meter);model=base['model']
            B=np.array([[float(x.midq()) for x in row[:n+r]] for row in base['BI']]);X=np.array(base['X'],dtype=float)
            L=np.array(cert['selected_projection'],dtype=object);L=np.array([[float(Q(x)) for x in row] for row in L])
            scales=np.array([float(base['scaleI'][model.meta[pcol][2]].midq()) for _,pcol in model.support])
            F0,J0,S0=e.prior.archived.jets(model,base['X'],'float')
            h0=np.asarray(F0[:n]);psi0=L@(np.asarray(F0[n:])*scales)
            rho=list(map(Q,cert['rho_i']));mu=list(map(Q,cert['mu_i']));eps=Q(e.CFG['epsilon_primary'])
            spacing=[Q(e.CFG['strict_spacing_epsilon_multiplier'])*eps/m for m in mu]
            # Exactly the proved positions, not tuned points or new witnesses.
            positions=[[float(-rad+j*step) for j in range(count)] for rad,step,count in zip(rho,spacing,cert['N_i'])]
            points=[];details=[]
            K=np.block([[np.array([[float(Q(x)) for x in row] for row in cert['K_hidden']]),np.zeros((n,r))],
                        [np.zeros((r,n)),np.array([[float(Q(x)) for x in row] for row in cert['K_selected']])]])
            for target in itertools.product(*positions):
                y=np.zeros(n+r);wanted=np.r_[h0,psi0+target]
                for _ in range(16):
                    XX=X+(B@y).reshape(X.shape)
                    F,J,S=e.prior.archived.jets(model,XX.tolist(),'float')
                    ff=np.r_[F[:n],L@(np.asarray(F[n:])*scales)]
                    jj=np.vstack([J[:n]@B,L@((J[n:]*scales[:,None])@B)])
                    residual=ff-wanted
                    if np.max(np.abs(residual))<2e-15:break
                    y-=np.linalg.solve(jj,residual)
                else:raise AssertionError('Numerical reconstruction did not converge')
                limits=np.array([float(Q(cert['a0'])*Q(cert['hidden_factor']))]*n+list(map(lambda x:float(Q(x)),cert['a_i'])))
                assert np.all(np.abs(y)<=limits)
                XX=X+(B@y).reshape(X.shape)
                # Re-evaluate the float-generated point at 100 decimal digits.
                mp.mp.dps=100;Fhp,_,Shp=e.prior.archived.jets(model,[[Q(float(x)) for x in row] for row in XX],'mp')
                hidden_error=max(abs(Fhp[i]-e.mpq(Q(float(h0[i])))) for i in range(n))
                proj=[sum(e.mpq(Q(cert['selected_projection'][i][j]))*Fhp[n+j]*e.mpq(base['scaleI'][model.meta[pcol][2]].midq())
                          for j,(_,pcol) in enumerate(model.support)) for i in range(r)]
                output_error=max(abs(proj[i]-mp.mpf(float(wanted[n+i]))) for i in range(r))
                assert hidden_error<mp.mpf('1e-12') and output_error<mp.mpf('1e-12')
                points.append(np.array([[float(x) for x in row] for row in Shp])*np.array([
                    float(base['scaleI'][g].midq()) for _,_,g,_ in model.meta])[None,:])
                details.append({'target':target,'hidden_residual_100_digits':mp.nstr(hidden_error,30),
                                'projection_residual_100_digits':mp.nstr(output_error,30),'max_scaled_input_coordinate':float(max(abs(y)/limits))})
            _,C=e.query_margins(base,[[Q(x) for x in row] for row in cert['selected_projection']])
            beta=math.sqrt(max(1,sum(float(model.params[p])**2 for i,j,p in model.layers[0]['R'])))
            CC=np.array(C,dtype=float)/(math.sqrt(n)*beta)
            distances=[max(np.linalg.norm((a-b).T@CC[:,j]) for j in range(n)) for a,b in itertools.combinations(points,2)]
            if distances:assert min(distances)>2*float(eps)
            rows.append({'case':cert['case'],'n':n,'mode':cert['mode'],'points_checked':len(points),'passed':True,
                         'minimum_pair_query_distance':min(distances) if distances else None,'details':details,
                         'label':'HIGH-PRECISION NUMERICAL validation, not the rigorous existence certificate'})
            print(cert['case'],n,'points',len(points),'min distance',min(distances) if distances else None,flush=True)
        (e.ROOT/'reconstruction_checks.json').write_text(json.dumps(rows,indent=2))
    finally:meter.finish()
if __name__=='__main__':main()
