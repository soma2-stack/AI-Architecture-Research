"""Read-only primary/secondary comparisons and certificate diagnostics."""
import json,csv,hashlib,math,sys
from fractions import Fraction as Q
import mpmath as mp
import engine as e
import importlib.util
_spec=importlib.util.spec_from_file_location('anisotropic_verify',e.ROOT/'verify.py')
_verify=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_verify)
load=_verify.load

def pack(cert,epsilon):
    counts=[int(2*Q(a)*Q(b)//(Q(e.CFG['strict_spacing_epsilon_multiplier'])*epsilon))+1
            for a,b in zip(cert['rho_i'],cert['mu_i'])]
    states=math.prod(counts)
    return {'epsilon':str(epsilon),'N_i':counts,'bits_per_axis':[float(mp.log(x,2)) for x in counts],
            'states':str(states),'bits':float(mp.log(states,2)),'D_robust':sum(x>1 for x in counts)}

def query_ball(base):
    n=base['n'];model=base['model'];R=[[Q(0) for _ in range(n)] for _ in range(n)]
    for i,j,p in model.layers[0]['R']:R[i][j]=model.params[p]
    Ri=e.inverse(R);invF=e.I(sum(x*x for row in Ri for x in row)).sqrt()
    factor=e.I(n*max(Q(1),sum(x*x for row in R for x in row))).sqrt()
    low=e.I(1)-e.I(Q(3,4)).tanh().square();high=e.I(1)-e.I(Q(1,4)).tanh().square()
    gmargin=(high-low)/2
    return Q((gmargin/(factor*invF)).lo,e.I.scale)

def old_comparator(base):
    """Apply the accepted global-ball sufficient arithmetic in declared units.

    Dense uses the ARCHIVED raw ball mapped through diagonal normalization.
    Independent uses the same conservative method on its supported endpoint.
    This independent radius is a new comparator, not a previously stored fact.
    """
    n=base['n'];D=base['D'];model=base['model']
    if not model.diagonal:
        data=json.loads((e.REPO/e.prior.CFG['dense_certificates'][str(n)]).read_text())
        prior=e.prior.certified_patch(data,n)
        scale=min(Q(x.lo,e.I.scale) for x in base['scaleI'].values())
        radius=Q(prior['fixed_h_frobenius_radius_exact'])*scale
        source='Archived raw ball, mapped by smallest parameter RMS; same normalized units'
    else:
        J=base['reduced'];K=e.mpinverse(J);eta=Q(float(max(e.upsum(e.residual(K,J),axis=1))))
        assert eta<1
        normK=max(sum(abs(x) for x in row) for row in K)
        R=[[Q(0) for _ in range(n)] for _ in range(n)];W=[[Q(0) for _ in range(n)] for _ in range(n)];b=[]
        for i,j,p in model.layers[0]['R']:R[i][j]=model.params[p]
        for i,j,p in model.layers[0]['W']:W[i][j]=model.params[p]
        b=[model.params[p] for i,j,p in model.layers[0]['b']]
        params=sum(R,[])+sum(W,[])+b
        bx=max(sum(x.absq() for x in row) for row in base['BI'])
        B=max(abs(x) for row in base['X'] for x in row)+bx
        L,_,_=e.prior.hessian_bounds(params,n,len(base['X']),B)
        output_scale=max(Q(1),max(Q(x.hi,e.I.scale) for x in base['scaleI'].values()))
        L=L*bx*bx*output_scale
        rr=min(Q(1),(1-eta)/(2*normK*L));radius=(1-eta)*rr/(4*normK)
        source='New same-global-majorant comparator on supported independent endpoint; not an archived radius'
    rc=query_ball(base);eps=Q(e.CFG['epsilon_primary']);argument=e.mpq(rc*radius)/(4*e.mpq(eps)*mp.sqrt(n))
    bits=max(mp.mpf(0),D*mp.log(argument,2));return {'radius_exact':str(radius),'radius':float(radius),
        'query_ball_margin_exact':str(rc),'query_ball_margin':float(rc),'old_bits':float(bits),
        'old_full_dimension_threshold':float(e.mpq(rc*radius)/mp.sqrt(n)),
        'old_certified_effective_dimension_at_primary':D if e.mpq(eps)<e.mpq(rc*radius)/mp.sqrt(n) else 0,
        'source':source,'label':'CERTIFIED sufficient comparator'}

def main():
    meter=e.Meter('packing curves, directional failure audit and isotropic comparators')
    e.prior.archived.ACTIVE_METER=meter
    try:
        assert (e.ROOT/'PRIMARY_FROZEN.json').exists()
        primary=json.loads((e.ROOT/'results_svd.json').read_text())
        secondary=json.loads((e.ROOT/'results_frame.json').read_text()) if (e.ROOT/'results_frame.json').exists() else []
        archived=json.loads((e.REPO/'experiments/approximate_observability_20260930/summary.json').read_text())
        rows=[];spectra=[];weak=[];directional=[]
        attempts=e.read_rows(e.ROOT/'attempts_svd.jsonl')+e.read_rows(e.ROOT/'attempts_frame.jsonl')
        for p in primary:
            meter.check();n=p['n'];case=p['case'];base=load(n,case,192,meter);D=base['D']
            sec=next((x for x in secondary if x['n']==n and x['case']==case),None)
            best=sec if sec is not None and int(sec['states'])>int(p['states']) else p
            old=old_comparator(base)
            curves={'primary_SVD':[pack(p,Q(x)) for x in ('1/100','1/1000','1/10000')],
                    'selected_secondary_frame':None if sec is None else [pack(sec,Q(x)) for x in ('1/100','1/1000','1/10000')]}
            radii=list(map(Q,best['rho_i']));margins=list(map(Q,best['mu_i']));half=[a*b for a,b in zip(radii,margins)]
            row={'case':case,'n':n,'T':len(base['X']),'P':base['model'].P,'D_exact':D,
                 'primary_D_robust':p['robust_dimension'],'primary_bits':p['bits'],
                 'secondary_D_robust':None if sec is None else sec['robust_dimension'],'secondary_bits':None if sec is None else sec['bits'],
                 'selected_mode':best['mode'],'selected_r':best['r'],'rho_i':[float(x) for x in radii],
                 'mu_i':[float(x) for x in margins],'observable_half_ranges':[float(x) for x in half],
                 'N_i':best['N_i'],'bits_per_axis':[float(mp.log(x,2)) for x in best['N_i']],
                 'rho_aspect_ratio':float(max(radii)/min(radii)),'retained_margin_strongest':float(max(half)),
                 'retained_margin_median':float(sorted(half)[len(half)//2]),'retained_margin_weakest':float(min(half)),
                 'selected_preconditioner_condition':best['preconditioner_condition'],
                 'directional_curvature_F':best['directional_curvature_F'],
                 'old_isotropic':old,'curves':curves,'label':'CERTIFIED selected product; spectra separately numerical'}
            row['improvement_in_bits']=best['bits']-old['old_bits']
            row['multiplicative_bit_improvement']='Undefined when old bound is zero'
            # Actual selected rational history frame conditioning. The exact
            # Gram defect gives a rigorous operator condition enclosure.
            Bs=[row[:n+best['r']] for row in base['B']];s=n+best['r']
            defect=max(sum(abs(sum(row[i]*row[j] for row in Bs)-int(i==j)) for j in range(s)) for i in range(s))
            cond=e.I((1+defect)/(1-defect)).sqrt()
            row['history_frame_gram_defect_exact']=str(defect)
            row['history_frame_condition_upper']=str(Q(cond.hi,e.I.scale))
            L=mp.matrix([[e.mpq(Q(x)) for x in rr] for rr in best['selected_projection']])
            ls=list(mp.svd(L,compute_uv=False))
            row['output_projection_condition_numerical']=float(ls[0]/ls[-1])
            records=[x for x in attempts if x['case']==case and x['n']==n]
            counts={x:0 for x in 'ABCDEFGH'};axisrows=[];maxprefix=max(x['r'] for x in records)
            sig=[mp.mpf(x) for x in base['spectra']['singular_values']]
            mu_svd,_=e.query_margins(base,base['U'])
            for i in range(D):
                valid=[x for x in records if x['valid'] and x['r']>i]
                top=max((Q(x['observable_half_ranges'][i]) for x in valid),default=Q(0))
                nn=max((x['N_i'][i] for x in valid),default=1)
                raw_direction=mp.sqrt(sum((e.mpq(base['reduced'][n+k][n+i].midq())/
                    e.mpq(base['scaleI'][base['model'].meta[pcol][2]].midq()))**2
                    for k,(_,pcol) in enumerate(base['model'].support)))
                if nn>1:reason=None
                elif sig[i]*mp.mpf('.5')<mp.mpf('0.0010625'):
                    reason='G' if raw_direction*mp.mpf('.5')>=mp.mpf('0.0010625') else 'A'
                elif sig[i]*mp.mpf('.5')*e.mpq(mu_svd[i])<mp.mpf('0.0010625'):reason='C'
                elif i>=maxprefix:reason='E'
                elif not valid:reason='D'
                else:reason='B'
                if reason:counts[reason]+=1
                ax={'case':case,'n':n,'axis':i+1,'sigma_normalized':str(sig[i]),'best_certified_half_range':float(top),
                    'best_N_in_any_joint_product':nn,'primary_failure_reason':reason,
                    'reason_scope':'Declared certificate/grid only; not proof of physical impossibility',
                    'raw_same_history_direction_norm_numerical':mp.nstr(raw_direction,50),
                    'max_svd_grid_linearized_half_range':float(sig[i]*mp.mpf('.5')*e.mpq(mu_svd[i]))}
                axisrows.append(ax);directional.append(ax)
            row['discarded_failure_counts']=counts
            row['proposal_failure_counts']={name:sum(x.get('reason')==name for x in records) for name in
              ('hidden_jacobian_dominance','hidden_section_box_inclusion','mixed_sensitivity_curvature')}
            rows.append(row)
            oldrow=next(x for x in archived if x['n']==n and x['case']==case)
            for i,(raw,scaled) in enumerate(zip(oldrow['fixed_h_raw']['values'],base['spectra']['singular_values'])):
                spectra.append({'case':case,'n':n,'axis':i+1,'raw_sigma':raw,'normalized_sigma':scaled})
            # Diagnostic application of sigma_min^2 dependence with unchanged
            # curvature/norm/query factors. NOT a new reachable-box certificate.
            prefixes=sorted(set([D,D-1,math.ceil(.95*D),math.ceil(.9*D)]+[x for x in (1,4,8,16) if x<=D]))
            for r in prefixes:
                factor=(sig[r-1]/sig[-1])**2
                weak.append({'case':case,'n':n,'retained':r,'discarded':D-r,
                    'sigma_tail':mp.nstr(sig[r-1],60),'sigma_squared_improvement_if_other_factors_fixed':mp.nstr(factor,60),
                    'radius_model':mp.nstr(e.mpq(Q(old['radius_exact']))*factor,60),
                    'label':'HIGH-PRECISION NUMERICAL counterfactual model; unchanged global curvature, not a certificate'})
        (e.ROOT/'summary.json').write_text(json.dumps(rows,indent=2))
        (e.ROOT/'directional_audit.json').write_text(json.dumps(directional,indent=2))
        (e.ROOT/'weak_direction_diagnostics.json').write_text(json.dumps(weak,indent=2))
        with (e.ROOT/'spectra.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(spectra[0]));writer.writeheader();writer.writerows(spectra)
        sources=json.loads((e.REPO/'experiments/approximate_observability_20260930/source_hashes.json').read_text())
        # Preserve archived hashes exactly, and verify files have not changed.
        assert all(hashlib.sha256((e.REPO/p).read_bytes()).hexdigest()==v for p,v in sources.items())
        (e.ROOT/'source_hashes.json').write_text(json.dumps(sources,indent=2))
        print([(x['case'],x['n'],x['primary_bits'],x['secondary_bits']) for x in rows])
    finally:meter.finish()
if __name__=='__main__':main()
