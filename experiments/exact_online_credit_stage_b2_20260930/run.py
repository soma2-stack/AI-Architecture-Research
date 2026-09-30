"""Small B2 sweep, fail-closed exactness and CPU accounting, no optimizer."""
import csv
import hashlib
import io
import json
import subprocess
import time
import zipfile
import numpy as np
import scipy.linalg as la
import torch
import core as c
import structures as st
import compression as comp

def make(case,n,seed):
    if case=='rank1_feedback':return c.Model(n,1,'lowrank',1,seed)
    if case=='shared_linear':return c.Model(n,1,'block',1,seed,'none',True)
    if case=='explicit_feedback':return c.Model(n,1,'block',1,seed,'feedback')
    depth={'deep2':2,'deep3':3}.get(case,1)
    block=1 if case=='independent' else 4 if case=='block4' else n
    return c.Model(n,depth,'block',block,seed)

def configurations():
    for case in c.CFG['cases']:
        for n in c.CFG['widths']:
            for T in c.CFG['horizons']:
                for seed in c.CFG['seeds']:yield {'case':case,'n':n,'T':T,'seed':seed}

def name(z):return f"{z['case']}_n{z['n']}_T{z['T']}_s{z['seed']}"
def append(path,row):
    with (c.ROOT/path).open('a',encoding='utf-8') as f:f.write(json.dumps(row,allow_nan=False)+'\n')

def exact_gate(m,value,full,ref,theta_hash):
    assert c.digest(m.theta)==theta_hash
    assert torch.isfinite(value['S']).all() and torch.isfinite(value['gradient']).all()
    assert torch.equal(value['trajectory'],full['trajectory'])
    groups=c.grouped(m,value['gradient'],ref['gradient']);err=c.metric(value['S'],full['S'])
    assert all(c.passes(g) for g in groups) and c.passes(err),'Intended exact representation failed'
    return groups,err

def old_provenance(m,z,S,x):
    axis='positive' if m.linear_shared else 'mix' if m.mode=='feedback' else m.family
    key=f"n{m.n}_{axis}{m.interaction}_d{m.depth}_{m.mode}_T{z['T']}_s{z['seed']}.npz"
    old=c.ROOT.parent/'exact_online_credit_stage_b_20260930'
    with zipfile.ZipFile(old/'matrices.zip') as archive:
        if key not in archive.namelist():return {'available':False}
        blob=archive.read(key)
    with np.load(io.BytesIO(blob)) as saved:
        assert np.array_equal(saved['theta'],m.theta.numpy()) and np.array_equal(saved['x'],x.numpy())
        assert np.array_equal(saved['S'],S.numpy())
    return {'available':True,'npz':key,'sha256':hashlib.sha256(blob).hexdigest(),'identical':True}

def rank_audit(m,S):
    matrices=[('full',S)]
    for g in m.groups:
        if g['name']=='W':
            block=S[:,g['start']:g['end']].reshape(m.N,m.n,m.n)
            for owner in range(m.n):matrices.append((f"W_layer{g['layer']+1}_owner{owner}",block[:,owner,:]))
    records=[]
    for label,matrix in matrices:
        torchsv=torch.linalg.svdvals(matrix).numpy()
        svd=la.svdvals(matrix.numpy())
        _,gesvd,_=la.svd(matrix.numpy(),full_matrices=False,lapack_driver='gesvd')
        denom=max(np.linalg.norm(torchsv),1e-30)
        records.append({'slice':label,**comp.rank_details(matrix),
                        'torch_gesdd_relative_discrepancy':float(np.linalg.norm(torchsv-svd)/denom),
                        'torch_gesvd_relative_discrepancy':float(np.linalg.norm(torchsv-gesvd)/denom)})
    return records

def main_sweep(meter):
    assert not (c.ROOT/'raw.jsonl').exists(),'Refuse overwrite official results'
    (c.ROOT/'matrices').mkdir(exist_ok=True)
    rows=[]
    for z in configurations():
        meter.check();m=make(z['case'],z['n'],z['seed']);x,q,y=c.data(z['seed'],z['T'],m.n)
        before=c.digest(m.theta);xbefore=c.digest(x)
        _,inference=c.inference(m,x);ref=c.bptt(m,x,q,y);full=c.rtrl(m,x,q,y)
        assert torch.equal(ref['trajectory'],full['trajectory'])
        groups=c.grouped(m,full['gradient'],ref['gradient'])
        assert all(c.passes(g) for g in groups),'BPTT/RTRL invalid'
        online=[];local=None;shared=None
        _,_,K,_=c.graphs(m)
        methods=[('packed_exact',lambda:c.packed_run(m,x,q,y,K)),
                 ('online_svd',lambda:st.factor_run(m,x,q,y)),
                 ('online_local_residual',lambda:comp.residual_run(m,x,q,y))]
        if m.linear_shared:methods.append(('shared_exact',lambda:c.shared_run(m,x,q,y)))
        if m.depth==1 and z['seed']==c.CFG['seeds'][0] and z['T']==32:
            methods.append(('unfused_kronecker_history',lambda:st.kronecker_sum_run(m,x,q,y)))
        for method,fn in methods:
            meter.check();value=fn();g,err=exact_gate(m,value,full,ref,before)
            numbers=value['stored_derivative_scalars']+value.get('index_bytes',0)//8
            online.append({'method':method,'all_stored_numbers':numbers,'bytes':8*numbers,
                           'peak_stored_numbers':value.get('peak_stored_numbers',value.get('peak_stored_derivative_scalars',numbers)),
                           'ratio_to_full':numbers/full['S'].numel(),'ratio_to_P':numbers/m.P,
                           'seconds':value['seconds'],'inclusive_to_inference':value['seconds']/inference,
                           'reconstruction':err,'gradient_groups':g,'exact':True,
                           'peak_scratch_bound_scalars':value['peak_derivative_scratch_bound_scalars'],
                           'scope':value.get('scratch_scope'),'ranks_over_time':value.get('ranks_over_time')})
            if method=='online_local_residual':local=value['E']
            if method=='shared_exact':shared=value['S']
        row={**z,'id':name(z),'P':m.P,'N':m.N,'full_size':m.N*m.P,'inference_seconds':inference,
             'RTRL_seconds':full['seconds'],'BPTT_seconds':ref['seconds'],'reference_groups':groups,
             'parameter_hash':before,'input_hash':xbefore,'S_hash':c.digest(full['S']),
             'B_provenance':old_provenance(m,z,full['S'],x),
             'rank':comp.rank_details(full['S']),
             'rank_audit':rank_audit(m,full['S']) if z['seed']==c.CFG['seeds'][0] and z['T']==32 else None,
             'compression':comp.snapshot(m,full['S'],local,shared),'online':online,'rss_bytes':meter.process.memory_info().rss}
        assert c.digest(m.theta)==before and c.digest(x)==xbefore
        np.savez_compressed(c.ROOT/'matrices'/f"{name(z)}.npz",S=full['S'].numpy(),theta=m.theta.numpy(),x=x.numpy(),q=q.numpy(),y=y.numpy())
        append('raw.jsonl',row);rows.append(row)
        if len(rows)%20==0:print(json.dumps({'phase':'main','cases':len(rows),'cpu_seconds':time.process_time()}),flush=True)
    return rows

def family_sweep(meter):
    assert not (c.ROOT/'family.jsonl').exists(),'Refuse overwrite official family results'
    rows=[]
    for case in c.CFG['family_priority']:
        for n in c.CFG['widths']:
            for T in c.CFG['horizons']:
                for seed in c.CFG['seeds']:
                    meter.check()
                    if meter.prior+time.process_time()>c.CFG['cpu_family_start_limit_seconds']:
                        return rows,False
                    z={'case':case,'n':n,'T':T,'seed':seed};m=make(case,n,seed);before=c.digest(m.theta)
                    matrices=[];digests=[];start=time.perf_counter()
                    for stream in range(c.CFG['family_stream_start'],c.CFG['family_stream_start']+max(c.CFG['family_sample_counts'])):
                        meter.check();x,q,y=c.data(seed,T,n,stream);h=torch.zeros(m.N);S=torch.zeros(m.N,m.P)
                        for xt in x:
                            h,A,B,_=c.partials(m,h,xt);S=A@S+B
                        assert torch.isfinite(S).all();matrices.append(S.numpy());digests.append({'stream':stream,'input':c.digest(x),'S':c.digest(S)})
                    assert c.digest(m.theta)==before
                    array=np.stack(matrices);checkpoints=comp.family_span(array,c.CFG['family_sample_counts'])
                    assert max(a['QR_reconstruction_error'] for a in checkpoints)<1e-12
                    row={**z,'id':name(z),'parameter_hash':before,'matrix_family_hash':hashlib.sha256(array.tobytes()).hexdigest(),
                         'sample_hashes':digests,'checkpoints':checkpoints,'seconds':time.perf_counter()-start,
                         'rss_bytes':meter.process.memory_info().rss,'analysis_buffers_bytes':array.nbytes*3}
                    if case=='shared_linear':
                        assert all(a['centered']['ranks']['1e-08']<=2*n for a in checkpoints),'Positive family dimension failure'
                    append('family.jsonl',row);rows.append(row)
                    del array,matrices
                print(json.dumps({'phase':'family','case':case,'n':n,'T':T,'records':len(rows),'cpu_seconds':time.process_time()}),flush=True)
    return rows,True

def high_precision(meter):
    import mpmath as mp
    mp.mp.dps=c.CFG['precision_decimal_digits'];start=time.process_time()
    z={'case':'rank1_feedback','n':8,'T':32,'seed':c.CFG['seeds'][0]};m=make(z['case'],8,z['seed']);x,q,y=c.data(z['seed'],32,8)
    R=mp.matrix(m.recurrence(0,m.theta).tolist());W=mp.matrix(m.value(m.layer_groups[0]['W'],m.theta).tolist());b=mp.matrix(m.value(m.layer_groups[0]['b'],m.theta).tolist())
    # Full sensitivity only for one W-owner block, recomputed at high precision from rounded frozen weights.
    h=mp.zeros(8,1);S=mp.zeros(8,8)
    for xt in x:
        meter.check();assert time.process_time()-start<120,'Precision sub-budget exceeded'
        xx=mp.matrix(xt.tolist());a=R*h+W*xx+b;h=mp.matrix([mp.tanh(v) for v in a]);gain=[1-v*v for v in h]
        A=mp.matrix([[gain[i]*R[i,j] for j in range(8)] for i in range(8)])
        B=mp.zeros(8,8)
        for j in range(8):B[0,j]=gain[0]*xx[j]
        S=A*S+B
    sv=list(mp.svd(S,compute_uv=False));full=c.rtrl(m,x,q,y);g=m.layer_groups[0]['W'];owner=full['S'][:,g['start']:g['start']+8]
    converted=torch.tensor([[float(S[i,j]) for j in range(8)] for i in range(8)])
    row={'case':z,'digits':mp.mp.dps,'cpu_seconds':time.process_time()-start,
         'scope':'mpmath recurrence from rounded float64 R/W/b; high-precision tanh and sensitivities, W-owner0 only',
         'high_precision_singular_values':[mp.nstr(v,45) for v in sv],
         'high_precision_ranks':{str(t):sum(v>sv[0]*t for v in sv) for t in c.CFG['numerical_rank_relative_thresholds']},
         'float64':comp.rank_details(owner),'matrix_discrepancy':c.metric(owner,converted)}
    (c.ROOT/'precision.json').write_text(json.dumps(row,indent=2));return row

def main():
    meter=c.Meter('Stage-B2 measured main, precision and family audit')
    try:
        hardware=c.hardware();repo=c.ROOT.parents[1]
        provenance={'hardware':hardware,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),
                    'config_sha256':hashlib.sha256((c.ROOT/'config.json').read_bytes()).hexdigest(),
                    'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in c.ROOT.glob('*.py')},
                    'Stage_B_source_commit':'ab56ca44dbf69a5cec7a2c8cecb7dd9a74f76e09'}
        (c.ROOT/'provenance.json').write_text(json.dumps(provenance,indent=2))
        rows=main_sweep(meter);precision=high_precision(meter);families,complete=family_sweep(meter)
        status={'reference_valid':True,'main_complete':len(rows)==160,'family_complete':complete,'precision_complete':True,
                'main_count':len(rows),'family_count':len(families),'classification':comp.classify(rows,families,complete)}
        (c.ROOT/'status.json').write_text(json.dumps(status,indent=2));print(json.dumps(status),flush=True)
    except Exception as exc:
        status={'reference_valid':False,'error':repr(exc),'classification':'STAGE B2 — INCONCLUSIVE','invalid_or_incomplete':True}
        (c.ROOT/'status.json').write_text(json.dumps(status,indent=2));raise
    finally:meter.finish()

if __name__=='__main__':main()
