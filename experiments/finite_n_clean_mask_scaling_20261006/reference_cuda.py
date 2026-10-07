"""CUDA finite-reference multistage diagnostic. No training, optimization or proof."""
import os
for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
import hashlib
import json
import math
import time
from pathlib import Path
import torch

# Thread pools are constrained by run_diagnosis.py before this module imports.
torch.set_default_dtype(torch.float64)
torch.manual_seed(20261006)
ROOT=Path(__file__).resolve().parent
PREV=ROOT.parent/'finite_n_early_capture_20261006'
START=time.perf_counter()
CPU_START=time.process_time()
LIMIT=3500
DEVICE=torch.device('cuda:0')
THRESHOLDS={
    'two_capture_max_damage_over_initial':1e-9,
    'full_response_cross_talk_ratio':1e-3,
    'trace_step_error_over_initial':1e-10,
    'trace_match_absolute_error':1e-10,
    'order_transport_quality_difference':1e-6,
    'order_cross_talk_difference':1e-3,
    'amplitude_max_damage_over_initial':1e-8,
    'scaling_B_norm_ratio_min':.9,
    'scaling_B_norm_ratio_max':1.1,
    'scaling_A_retention_relative_change':.01,
    'break_min_cross_talk_ratio':.1,
    'break_min_cross_talk_increase_factor':10.,
    'past_input_absolute_bound':.5,
}

def save(name, obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def guard():
    if time.perf_counter()-START>LIMIT:
        raise RuntimeError('STOP: 3500-second hard runtime guard')
    if torch.cuda.max_memory_allocated()>4*1024**3:
        raise RuntimeError('STOP: conservative 4 GiB allocated VRAM guard')

DEFAULT_MASKS={
    1:[1], 2:[1,2], 3:[1,2,3], 4:[1,2,4,3],
    5:[1,2,4,8,3], 6:[1,2,4,8,16,3],
    7:[1,2,4,8,16,32,3], 8:[1,2,4,8,16,32,64,3],
    9:[1,2,4,8,16,32,64,3,5],
    10:[1,2,4,8,16,32,64,3,5,6],
    12:[1,2,4,8,16,32,64,3,5,6,9,10],
}

def spec(n,K,kind='core',amps=None,order=None,clear_mult=2.,masks=None,equal_age_steps=None):
    if order is None: order=tuple(range(len(amps) if amps is not None else len(masks) if masks is not None else 2))
    if amps is None: amps=tuple(1. for _ in order)
    if masks is None: masks=DEFAULT_MASKS.get(len(order), [1<<j for j in range(len(order))])
    return dict(n=n,K=K,kind=kind,amplitudes=list(amps),order=list(order),
                clear_mult=float(clear_mult),
                masks=list(masks),equal_age_steps=equal_age_steps,
                id=f'{kind}_n{n}_K{K}_amp'+ '_'.join(map(str,amps))+'_order'+''.join(map(str,order))+f'_clear{clear_mult:g}')

def O(x,d,k):
    """Complete reference selected Householder/cycle block, matrix-free."""
    gamma=1/(1-1/math.sqrt(k))
    y=torch.empty_like(x)
    y[...,0,:]=0
    y[...,1:d-1,:]=x[...,:d-2,:]
    y[...,d-1:,:]=x[...,d-1:,:]
    mass=x.sum(-2)
    j=gamma/math.sqrt(k)*x[...,d-2,:]-gamma**2/k*mass
    b=gamma/math.sqrt(k)*mass
    y+=j.unsqueeze(-2)
    y[...,0,:]+=b
    return y

@torch.no_grad()
def batch(n, specs, channels=2):
    guard()
    tick=time.perf_counter()
    C=len(specs); Kmax=max(s['K'] for s in specs); kinds=[s['kind'] for s in specs]
    k=n//2; d=n//4; r=k-1; ell=n-k; m=(k-d)//4
    a=1-1/n; gh=1-1/n**2; gl=.995
    write=math.ceil(.4*n)
    tail=math.ceil(math.log((write+1)/1e-3)/(-math.log(a*gl)))+1
    clear_values={math.ceil(2*n*s.get('clear_mult',2.)) for s in specs}
    if len(clear_values)!=1:
        raise ValueError('A batch must share one clear duration')
    clear=clear_values.pop()
    stage_length=write+1+tail+clear
    total=channels*stage_length+1
    act=torch.arange(d-1,d-1+4*m,device=DEVICE)
    tuples=act.reshape(m,4)
    nd=m//2; surv=tuples[nd:].reshape(-1); ns=len(surv)
    signs=torch.tensor([1.,1.,-1.,-1.],device=DEVICE)
    idx=torch.arange(nd,device=DEVICE)
    masks=specs[0].get('masks',DEFAULT_MASKS.get(channels,[1<<j for j in range(channels)]))
    if len(masks)!=channels or any(s.get('masks',masks)!=masks for s in specs):
        raise ValueError('A batch must use one common character-mask list')
    if len(set(masks))!=channels or any(mask<=0 or mask>=nd for mask in masks):
        raise ValueError(f'Walsh masks must be distinct nonzero masks below nd={nd}: {masks}')
    chi_base=[]
    for mask in masks:
        parity=torch.zeros(nd,device=DEVICE,dtype=torch.int64)
        bit=0
        while (1<<bit)<=mask:
            if mask&(1<<bit): parity+=((idx>>bit)&1)
            bit+=1
        chi_base.append(torch.where(parity%2==0,1.,-1.))
    chi=torch.stack(chi_base).repeat_interleave(4,dim=1)
    xis=torch.zeros(C,channels,r,device=DEVICE)
    mask_rows=torch.zeros_like(xis)
    V=torch.zeros(C,r,Kmax,device=DEVICE)
    codes=torch.zeros(C,channels,Kmax,device=DEVICE)
    ords=torch.tensor([s['order'] for s in specs],device=DEVICE)
    donor_idx=torch.empty(C,nd,device=DEVICE,dtype=torch.int64)
    for c,s in enumerate(specs):
        K=s['K']
        assert nd>=K and nd%K==0
        donor_idx[c]=torch.arange(nd,device=DEVICE)//(nd//K)
        ss=torch.zeros(r,device=DEVICE)
        comp=tuples[nd:,2:].reshape(-1); ss[comp]=1/math.sqrt(len(comp))
        W=torch.zeros(r,K,device=DEVICE)
        for j in range(K):
            inds=tuples[:nd].reshape(K,nd//K,4)[j,:,2:].reshape(-1)
            W[inds,j]=1/math.sqrt(len(inds)); W[:,j]-=ss/math.sqrt(K)
        P=torch.ones(K,K,device=DEVICE)/K
        H=torch.eye(K,device=DEVICE)-(1-1/math.sqrt(2))*P
        V[c,:,:K]=W@H
        for j in range(channels):
            v=torch.where((torch.arange(K,device=DEVICE)//(2**max(j-1,0)))%2==0,1.,-1.)
            if j==0: v=torch.ones(K,device=DEVICE)
            if s['kind']=='stress':
                v*=torch.linspace(.1+.1*j,1.,K,device=DEVICE)
            codes[c,j,:K]=s['amplitudes'][j]*v
        mask_rows[c,:,surv]=chi/math.sqrt(ns)
        xis[c,:,surv]=chi/math.sqrt(ns)
        if s['kind'] in ('broken','negative_alias'):
            mask_rows[c,1]=mask_rows[c,0]
            xis[c,1]=xis[c,0]
        if s['kind']=='negative_nonsum':
            read=chi[0]+.1
            xis[c,0,surv]=read/torch.linalg.vector_norm(read)
        if s['kind']=='negative_nonsum_ones':
            read=torch.ones_like(chi[0])
            xis[c,0,surv]=read/torch.linalg.vector_norm(read)
    gram=V.transpose(-1,-2)@V
    orth_errors=[float((gram[c,:s['K'],:s['K']]-torch.eye(s['K'],device=DEVICE)).abs().max())
                 for c,s in enumerate(specs)]
    # Pairs for channel j differ only in +/- its donor control. Other channels
    # take the same positive coded write in both histories of the pair.
    X=torch.zeros(C,channels,2,r,Kmax,device=DEVICE)
    Delta=torch.zeros(C,channels,r,Kmax,device=DEVICE)
    tau=torch.zeros(C,channels,2,Kmax,device=DEVICE)
    public_tau=0.
    h=torch.full((r,1),math.tanh(.05),device=DEVICE); h[act]=0
    gamma=1/(1-1/math.sqrt(k))
    prev_h=(.04*signs).repeat(m).expand(C,channels,2,-1).clone()
    energy=((torch.atanh(prev_h)-.05)**2).sum(-1)
    sigma=.05
    for _ in range(20): sigma=math.tanh(sigma/(100*n)+.05)
    energy+=ell*(sigma/(100*n))**2
    max_raw=torch.zeros(C,device=DEVICE)
    max_raw[:]=(torch.atanh(prev_h)-.05).abs().max()
    pure=torch.zeros(C,r,channels,device=DEVICE)
    captured=torch.zeros(C,channels,Kmax,device=DEVICE)
    predicted=torch.zeros_like(captured)
    initial_mask=torch.zeros(C,channels,device=DEVICE,dtype=torch.bool)
    max_damage=torch.zeros(C,channels,device=DEVICE)
    max_trace_step=torch.zeros(C,channels,device=DEVICE)
    max_trace_match=torch.zeros(C,device=DEVICE)
    checkpoints=[{} for _ in specs]; traces=[[] for _ in specs]; corrections=[[] for _ in specs]
    equal_age_steps=min([s.get('equal_age_steps') for s in specs if s.get('equal_age_steps') is not None],default=None)
    capture_times=[(j*stage_length+write+1) for j in range(channels)]
    equal_age_times=set(t+equal_age_steps for t in capture_times) if equal_age_steps is not None else set()
    equal_age_records=[{} for _ in specs]
    rows_before=None
    cidx=torch.arange(C,device=DEVICE)
    sample_stride=max(1,total//180)
    clear_stride=max(1,clear//32)
    for t in range(1,total+1):
        reset=(t==total)
        stage=min((t-1)//stage_length,channels-1)
        local=(t-1)%stage_length+1
        ch=ords[:,stage]
        phase=('reset' if reset else 'write' if local<=write else 'capture' if local==write+1
               else 'trace' if local<=write+1+tail else 'clear')
        is_correction=not reset and local==write+1+tail
        labels=[]
        if local==1 and not reset:
            before=torch.einsum('csr,cprk->cpsk',xis,Delta)
            before_vals=torch.linalg.vector_norm(before,dim=-1).cpu().tolist()
            before_preds=torch.linalg.vector_norm(predicted,dim=-1).cpu().tolist()
            for c in range(C):
                checkpoints[c][f'before_stage_{stage}_write']=dict(t=t-1,stage=stage,phase='before_write',response_norm_matrix=before_vals[c],predicted_correct_norms=before_preds[c])
        # The prep/public autonomous state has been evolving continuously;
        # no front restart between captures, repairs or clearing periods.
        field=gamma/math.sqrt(k)*h[d-2,0]-gamma**2/k*h.sum()
        hn=torch.tanh(a*O(h,d,k)+.05)
        public_g=1-hn[:,0]**2
        hn[act]=0
        h=hn
        old_reads=torch.einsum('csr,cprk->cpsk',xis,Delta)
        dg=torch.full((C,channels,2,Kmax),gl,device=DEVICE)
        if phase=='write':
            v=codes[cidx,ch]
            theta=v[:,None,None,:].expand(-1,channels,2,-1).clone()
            for q in range(channels):
                theta[:,q,1,:]=torch.where((ch==q)[:,None],-v,v)
            dg=gl+(theta+1)*(gh-gl)/2
        if is_correction:
            target=gl*(1+a*public_tau)
            dg=target/(1+a*tau)
        tg=torch.full((C,channels,2,m),gh,device=DEVICE)
        gathered=torch.gather(dg,-1,donor_idx[:,None,None,:].expand(-1,channels,2,-1))
        tg[...,:nd]=gathered
        if phase=='capture':
            mask=mask_rows[cidx,ch][:,surv]>0
            tg[...,nd:]=torch.where(mask,gh,gl)[:,None,None,::4]
        if phase in ('trace','clear'):
            bad=torch.where(torch.arange(nd,device=DEVICE)%2==0,gl,gh)
            nonuniform=torch.tensor([kind=='negative_nonuniform' for kind in kinds],device=DEVICE)
            tg[...,nd:]=torch.where(nonuniform[:,None,None,None],bad[None,None,None,:],tg[...,nd:])
        G=public_g.expand(C,channels,2,-1).clone()
        G[...,act]=tg.repeat_interleave(4,-1)
        if reset:
            G[...,act]=1-.05**2
            next_h=torch.full_like(prev_h,.05)
        else:
            next_h=(torch.sqrt(1-tg)[...,None]*signs).reshape(C,channels,2,-1)
        raw=torch.atanh(next_h)-a*(prev_h+field)-.05
        energy+=(raw**2).sum(-1)
        max_raw=torch.maximum(max_raw,raw.abs().reshape(C,-1).amax(-1))
        prev_h=next_h
        baseB=a*O(X[:,:,1],d,k)+V[:,None]
        Delta=G[:,:,0,:,None]*(a*O(Delta,d,k))+(G[:,:,0]-G[:,:,1])[...,None]*baseB
        X=G[...,None]*(a*O(X,d,k)+V[:,None,None])
        tau=(1-.05**2 if reset else dg)*(1+a*tau)
        public_tau=(1-.05**2 if reset else gl)*(1+a*public_tau)
        reads=torch.einsum('csr,cprk->cpsk',xis,Delta)
        diag=reads[:,torch.arange(channels,device=DEVICE),torch.arange(channels,device=DEVICE)]
        if phase=='capture':
            # Existing singleton characters acquire the public mask mean;
            # generated product characters are tracked by the complete recurrence.
            factors=torch.full((C,channels),a*(gh+gl)/2,device=DEVICE)
        else:
            factors=torch.full((C,channels),a*(1-.05**2 if reset else gh),device=DEVICE)
        predicted*=factors[...,None]
        damage=torch.linalg.vector_norm(diag-predicted,dim=-1)/torch.linalg.vector_norm(captured,dim=-1).clamp_min(1e-300)
        max_damage=torch.maximum(max_damage,torch.where(initial_mask,damage,0.))
        pure=G[:,0,0,:,None]*(a*O(pure,d,k))
        if phase=='capture':
            captured[cidx,ch]=diag[cidx,ch]
            predicted[cidx,ch]=diag[cidx,ch]
            initial_mask[cidx,ch]=True
            pure[cidx,:,ch]=xis[cidx,ch]
        if is_correction:
            step=torch.linalg.vector_norm(diag-factors[...,None]*old_reads[:,torch.arange(channels,device=DEVICE),torch.arange(channels,device=DEVICE)],dim=-1)
            step/=torch.linalg.vector_norm(captured,dim=-1).clamp_min(1e-300)
            max_trace_step=torch.maximum(max_trace_step,step)
            max_trace_match=torch.maximum(max_trace_match,(tau[:,:,0]-tau[:,:,1]).abs().reshape(C,-1).amax(-1))
        if local==write and not reset: labels.append(f'after_stage_{stage}_write')
        if phase=='capture': labels.append(f'after_stage_{stage}_capture')
        if local==write+tail and not reset: labels.append(f'before_stage_{stage}_correction')
        if is_correction: labels.append(f'after_stage_{stage}_correction')
        if local==write+tail+2 and not reset: labels.append(f'before_stage_{stage}_clear')
        if local==stage_length and not reset: labels.append(f'after_stage_{stage}_clear')
        if reset: labels.append('after_reset')
        if labels or (phase=='clear' and local%clear_stride==0) or t in equal_age_times:
            vals=torch.linalg.vector_norm(reads,dim=-1).cpu().tolist()
            preds=torch.linalg.vector_norm(predicted,dim=-1).cpu().tolist()
            complement=[]
            for c,s in enumerate(specs):
                Q=mask_rows[c,:1] if s['kind'] in ('broken','negative_alias') else mask_rows[c]
                coef=torch.einsum('sr,prk->psk',Q,Delta[c])
                projected=torch.einsum('rs,psk->prk',Q.T,coef)
                complement.append(torch.linalg.vector_norm(Delta[c]-projected,dim=(-2,-1)).cpu().tolist())
            for c in range(C):
                point=dict(t=t,stage=stage,phase=phase,response_norm_matrix=vals[c],predicted_correct_norms=preds[c],complement_residual_norms=complement[c])
                traces[c].append(point)
                for label in labels: checkpoints[c][label]=point
                if t in equal_age_times:
                    for q,cap in enumerate(capture_times):
                        if t==cap+equal_age_steps:
                            equal_age_records[c][str(q)]=dict(channel=q,age=equal_age_steps,
                                response_norm_matrix=vals[c],predicted_correct_norms=preds[c],
                                complement_residual_norms=complement[c])
        if is_correction:
            vv=dg.cpu().tolist()
            for c,s in enumerate(specs):
                v=torch.tensor(vv[c])[:,:,:s['K']].reshape(-1)
                corrections[c].append(dict(stage=stage,minimum=float(v.min()),maximum=float(v.max()),
                    range=float(v.max()-v.min()),variance=float(v.var(unbiased=False)),
                    standard_deviation=float(v.std(unbiased=False)),
                    max_deviation_from_public_gL=float((v-.995).abs().max()),g_last=vv[c]))
        if t%128==0:
            guard()
            if not bool(torch.isfinite(Delta).all()) or not bool(torch.isfinite(X).all()):
                raise RuntimeError('STOP: NaN/Inf in CUDA recurrence')
    torch.cuda.synchronize()
    final_reads=torch.einsum('csr,cprk->cpsk',xis,Delta)
    final_norms=torch.linalg.vector_norm(final_reads,dim=-1)
    diagonal=final_reads[:,torch.arange(channels,device=DEVICE),torch.arange(channels,device=DEVICE)]
    prednorm=torch.linalg.vector_norm(predicted,dim=-1)
    initnorm=torch.linalg.vector_norm(captured,dim=-1)
    puremat=torch.einsum('csr,crp->cps',xis,pure)
    outcomes=[]
    for c,s in enumerate(specs):
        fn=final_norms[c].cpu().tolist()
        ini=initnorm[c].cpu().tolist(); pn=prednorm[c].cpu().tolist()
        abs_err=torch.linalg.vector_norm(diagonal[c]-predicted[c],dim=-1).cpu().tolist()
        ratios=[max((fn[p][q]/max(fn[p][p],1e-300) for q in range(channels) if q!=p),default=0.) for p in range(channels)]
        correction_legal=all(x['minimum']>0 and x['maximum']<=1 for x in corrections[c])
        qmat=torch.tensor(puremat[c].cpu().tolist(),device=DEVICE)
        sv=torch.linalg.svdvals(qmat)
        # Query lower witness uses exactly the previous normalization. These
        # tiny row norms are NOT classified as epsilon-robust memory dimensions.
        sg=((1/math.cosh(.25))**2-(1/math.cosh(.75))**2)/2
        qc=sigma*math.sqrt(ell)*a*sg*math.sqrt(ns)/(n*math.sqrt(n))
        group_chi=chi[:,::4]
        walsh_gram=group_chi@group_chi.T/nd
        walsh_orthogonality_error=float((walsh_gram-torch.eye(channels,device=DEVICE)).abs().max())
        result=dict(s,m=m,survivor_physical_sites=ns,channels=channels,write_steps=write,
            walsh_masks=list(masks),
            trace_tail_steps=tail,clear_steps=clear,total_steps=total,mT=m*total,
            final_response_norm_matrix=fn,final_response_vectors=final_reads[c,:,:,:s['K']].cpu().tolist(),
            isolated_storage_response_matrix=puremat[c].cpu().tolist(),
            isolated_storage_condition_number=float(sv.max()/sv.min()) if float(sv.min())>1e-300 else None,
            initial_captured_reads=ini,predicted_final_reads=pn,
            retention=[fn[p][p]/max(ini[p],1e-300) for p in range(channels)],
            transport_quality=[fn[p][p]/max(pn[p],1e-300) for p in range(channels)],
            relative_damage=[abs_err[p]/max(ini[p],1e-300) for p in range(channels)],
            absolute_error=abs_err,max_damage_over_initial=max_damage[c].cpu().tolist(),
            cross_talk_ratios=ratios,max_trace_step_error_over_initial=max_trace_step[c].cpu().tolist(),
            donor_trace_match_error=float(max_trace_match[c]),corrections=corrections[c],
            max_absolute_raw_input=float(max_raw[c]),input_cube_legal=float(max_raw[c])<.5,
            correction_gates_legal=correction_legal,raw_history_norms=torch.sqrt(energy[c]).cpu().tolist(),
            common_endpoint_max_difference=0.,endpoint_basis='Balanced active states have equal mass zero until shared reset; full nondriven trajectory is common.',
            probe_orthogonality_error=orth_errors[c],walsh_orthogonality_error=walsh_orthogonality_error,
            walsh_row_sum_max=float(group_chi.sum(-1).abs().max()),
            query_lower_witness_correct_reads=[qc*fn[p][p] for p in range(channels)],
            checkpoints=checkpoints[c],trace=traces[c],batch_seconds=time.perf_counter()-tick,
            channel_capture_times=capture_times,
            channel_ages=[total-t for t in capture_times],
            equal_age_read_matrices=equal_age_records[c],
            individual_B_mean_abs=float(diagonal[c,min(1,channels-1),:s['K']].abs().mean()),
            combined_B_norm=fn[min(1,channels-1)][min(1,channels-1)],
            combined_B_norm_div_sqrt_K=fn[min(1,channels-1)][min(1,channels-1)]/math.sqrt(s['K']))
        outcomes.append(result)
    print(f'CUDA batch n={n}, channels={channels}, cases={C}, time={time.perf_counter()-tick:.1f}s, peak={torch.cuda.max_memory_allocated()/2**20:.1f} MiB',flush=True)
    return outcomes

def main():
    previous_summary=(PREV/'SUMMARY.md').read_text(encoding='utf-8')
    previous_results=json.loads((PREV/'results.json').read_text(encoding='utf-8'))
    metadata=dict(torch_version=torch.__version__,cuda_version=torch.version.cuda,
        cuda_available=torch.cuda.is_available(),selected_device=str(DEVICE),dtype='float64',seed=20261006,
        thresholds_frozen_before_sweep=THRESHOLDS,
        prior_test_status={k:v['status'] for k,v in previous_results['tests'].items()},
        previous_outputs_sha256={p.name:digest(p) for p in PREV.iterdir() if p.suffix in ('.json','.md','.png')},
        reference_source_ref=previous_results['metadata']['source_ref'],
        reference_scope='Complete dense reference O_*; stationary off-cycle four-site carriers; tiny actual-model perturbation omitted.',
        cpu_intraop_threads=1,cpu_interop_threads=1,workers=0,no_training=True,no_optimization=True,
        hard_runtime_guard_seconds=LIMIT,allocated_vram_guard_bytes=4*1024**3,
        attribution='Each row is a finite +/- control pair with all other controls held at their positive write; complete vector norm over orthonormal parameter probes.',
        prediction='a*g_H at preservation steps; a*(g_H+g_L)/2 at another independent capture; a*(1-.05^2) at reset.',
        checkpoint_note='before_stage_write is recorded before the first write update; each after-checkpoint includes that step.',
        classification_note='PASS concerns finite reference transport only, not a robust B^D theorem or Gaussian-code whole-boundary validation.')
    if not metadata['cuda_available']:
        metadata['status']='STOPPED: CUDA unavailable; no CPU fallback'
        save('run_metadata.json',metadata)
        raise RuntimeError(metadata['status'])
    metadata['gpu_name']=torch.cuda.get_device_name(DEVICE)
    metadata['initial_allocated_vram_bytes']=torch.cuda.memory_allocated(DEVICE)
    torch.cuda.reset_peak_memory_stats(DEVICE)
    planned=[]
    for n in (256,512,1024,2048):
        for K in (8,16,32,64):
            if K<=n//32: planned.append(spec(n,K))
    for n,K in ((512,8),(1024,16),(2048,32)):
        planned.append(spec(n,K,'reverse',order=(1,0)))
    for amps in ((1.,.5),(1.,.25),(.5,1.)):
        planned.append(spec(1024,16,'imbalance',amps))
    for n,K in ((512,8),(1024,16)):
        planned.append(spec(n,K,'stress'))
    planned.append(spec(1024,16,'broken'))
    planned.append(spec(2048,4,'scaling'))
    metadata['planned_core_cases']=planned
    save('run_metadata.json',metadata)  # thresholds and plan recorded before any numerical sweep
    print(json.dumps({k:metadata[k] for k in ('torch_version','cuda_version','gpu_name','cuda_available','selected_device','dtype','initial_allocated_vram_bytes')},indent=2),flush=True)
    cases=[]
    for n in (256,512,1024,2048):
        cases+=batch(n,[s for s in planned if s['n']==n])
        save('results.json',dict(status='RUNNING',cases=cases,thresholds=THRESHOLDS))
    # Optional exploratory three-channel path only with substantial headroom.
    optional=[]
    if time.perf_counter()-START<400:
        for n,K in ((512,8),(1024,16),(2048,32)):
            if time.perf_counter()-START>560: break
            optional+=batch(n,[spec(n,K,'three',amps=(1.,.75,.5),order=(0,1,2))],channels=3)
    torch.cuda.synchronize()
    metadata.update(total_runtime_seconds=time.perf_counter()-START,cpu_seconds=time.process_time()-CPU_START,
        peak_allocated_vram_bytes=torch.cuda.max_memory_allocated(DEVICE),peak_reserved_vram_bytes=torch.cuda.max_memory_reserved(DEVICE),
        largest_n=max(c['n'] for c in cases),largest_K=max(c['K'] for c in cases),optional_three_channel_cases=len(optional),status='COMPLETED')
    metadata['previous_outputs_unchanged']=all(digest(PREV/k)==v for k,v in metadata['previous_outputs_sha256'].items())
    save('run_metadata.json',metadata)
    save('results.json',dict(status='COMPLETED',cases=cases,three_channel_cases=optional,thresholds=THRESHOLDS,metadata=metadata))
    from report_results import finish
    finish(ROOT,cases,optional,metadata,THRESHOLDS)
    print(json.dumps({k:metadata[k] for k in ('total_runtime_seconds','peak_allocated_vram_bytes','peak_reserved_vram_bytes','previous_outputs_unchanged')},indent=2),flush=True)

if __name__=='__main__': main()
