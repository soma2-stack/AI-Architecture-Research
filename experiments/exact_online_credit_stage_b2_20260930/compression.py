"""Reconstructible known formats. Snapshot compression is not online closure."""
import time
import numpy as np
import scipy.linalg as la
import torch
import core as c
import structures as st

def rank_details(matrix):
    s=torch.linalg.svdvals(matrix);top=float(s[0]) if len(s) else 0.
    norm=float(s.norm());small=float(s[-1]) if len(s) else 0.
    return {'singular_values':s.tolist(),
            'ranks':{str(t):int((s>top*t).sum()) for t in c.CFG['numerical_rank_relative_thresholds']},
            'tail_ranks':{str(t):tail_rank(s,t) for t in c.CFG['reconstruction_tolerances']},
            'condition_number':top/small if small>0 else None,
            'stable_rank':(norm/top)**2 if top else 0.}

def tail_rank(s,tol):
    bound=tol*max(float(s.norm()),1e-30)
    for r in range(len(s)+1):
        if float(s[r:].norm())<=bound:return r
    return len(s)

def svd(matrix,tol):
    left,right,s=st.factor(matrix,tol)
    return (left@right),left.numel()+right.numel(),left.shape[1]

def block_svd(model,S,tol,owner=False,kron=False):
    """Select dense vs factor per supported group/block; indices counted."""
    _,_,mask,_=c.graphs(model);result=torch.zeros_like(S);count=0;ranks=[]
    for g in model.groups:
        columns=list(range(g['start'],g['end']))
        pieces=[columns]
        if owner and g['name']=='W':pieces=[columns[i*model.n:(i+1)*model.n] for i in range(model.n)]
        for cols in pieces:
            rows=np.flatnonzero(mask[:,cols].any(axis=1))
            if not len(rows):continue
            block=S[torch.tensor(rows)[:,None],torch.tensor(cols)[None,:]]
            shape=block.shape
            if kron and g['name']=='W':block=block.reshape(len(rows)*model.n,model.n)
            reconstruction,values,rank=svd(block,tol)
            if values>=block.numel():reconstruction=block;values=block.numel();rank=None
            result[torch.tensor(rows)[:,None],torch.tensor(cols)[None,:]]=reconstruction.reshape(shape)
            # Column bounds and owner are defined by static architecture; row indices retained.
            count+=values+len(rows);ranks.append(rank)
    return result,count,ranks

def snapshot(model,S,local_E,shared=None):
    rows=[]
    def add(name,fn,tol,scope='snapshot only'):
        before=time.perf_counter();reconstructed,count,detail=fn();elapsed=time.perf_counter()-before
        assert torch.isfinite(reconstructed).all()
        metric=c.metric(reconstructed,S)
        rows.append({'method':name,'tolerance':tol,'stored_numbers':int(count),'stored_bytes':int(count)*8,
                     'ratio_to_full':float(count/S.numel()),'ratio_to_P':float(count/model.P),
                     'reconstruction':metric,'passes':metric['relative_error']<tol,
                     'detail':detail,'seconds':elapsed,'scope':scope})
    add('full_matrix',lambda:(S,S.numel(),None),1e-8,'online baseline')
    flat=S.flatten();idx=torch.nonzero(flat,as_tuple=True)[0];val=flat[idx].clone()
    def sparse():
        r=torch.zeros_like(flat);r[idx]=val;return r.reshape_as(S),len(idx)+len(val),len(idx)
    add('coordinate_sparse',sparse,1e-8)
    _,_,mask,masks=c.graphs(model);pack=c.Packed(mask)
    for r,cols,v in pack.parts:v.copy_(S[r[:,None],cols[None,:]])
    values,indices=pack.storage()
    add('block_sparse_triangular',lambda:(pack.reconstruct(model.N,model.P),values+indices//8,None),1e-8,'known closed online block recurrence')
    if shared is not None:add('shared_linear_factors',lambda:(shared,2*model.n+1,None),1e-8,'known closed online shared recurrence')
    Q,R,perm=la.qr(S.numpy(),mode='economic',pivoting=True)
    for tol in c.CFG['reconstruction_tolerances']:
        add('global_svd',lambda tol=tol:svd(S,tol),tol)
        def basis():
            rank=next(r for r in range(len(R)+1) if np.linalg.norm(R[r:])<=tol*max(np.linalg.norm(R),1e-30))
            raw=Q[:,:rank]@R[:rank];out=np.zeros_like(raw);out[:,perm]=raw
            return torch.tensor(out),rank*(model.N+model.P)+len(perm),rank
        add('pivoted_qr_repeated_basis',basis,tol)
        add('supported_group_factors',lambda tol=tol:block_svd(model,S,tol),tol)
        add('owner_block_factors',lambda tol=tol:block_svd(model,S,tol,owner=True),tol)
        add('kronecker_shared_input_basis',lambda tol=tol:block_svd(model,S,tol,kron=True),tol)
        for name,E in [('immediate_support_exact_slice',torch.where(torch.tensor(masks['SnAp1']),S,0.)),('local_eligibility',local_E)]:
            base=c.Packed(masks['SnAp1']);nval,nidx=base.storage()
            def correction(E=E,tol=tol,nval=nval,nidx=nidx):
                recon,num,rank=svd(S-E,tol)
                return E+recon,num+nval+nidx//8,rank
            add(name+'_plus_svd_residual',correction,tol)
    return rows

def residual_run(model,x,q,y):
    """Exact local baseline plus recompressed residual; temporary dense work disclosed."""
    start=time.perf_counter();h=torch.zeros(model.N);_,_,_,masks=c.graphs(model)
    local=c.Packed(masks['SnAp1']);del masks
    nv,ib=local.storage();L=torch.zeros(model.N,0);R=torch.zeros(0,model.P)
    trajectory=[];maxstate=nv+ib//8;peak=0;ranks=[]
    for xt in x:
        h,A,B,workspace=c.partials(model,h,xt)
        oldE=local.reconstruct(model.N,model.P)
        S=A@(oldE+L@R)+B
        local.update(A,B);E=local.reconstruct(model.N,model.P)
        L,R,_=st.factor(S-E);L=L.clone();R=R.clone();ranks.append(L.shape[1])
        retained=nv+ib//8+L.numel()+R.numel();maxstate=max(maxstate,retained)
        peak=max(peak,workspace+6*model.N*model.P+4*retained+model.N*model.N)
        del A,B,S,oldE,E,_
        trajectory.append(h)
    E=local.reconstruct(model.N,model.P);S=E+L@R;cot,direct=model.terminal(h,q,y)
    return {'S':S,'gradient':cot@S+direct,'trajectory':torch.stack(trajectory),'E':E,
            'seconds':time.perf_counter()-start,'stored_derivative_scalars':nv+L.numel()+R.numel(),
            'index_bytes':ib,'derivative_bytes':8*(nv+L.numel()+R.numel())+ib,
            'peak_stored_numbers':maxstate,'ranks_over_time':ranks,'peak_derivative_scratch_bound_scalars':peak,
            'scratch_scope':'Full temporary oldE/E/S/A/B and SVD; no full persistent S or history'}

def family_span(matrices,counts):
    """Sample-axis QR, twice reorthogonalized, with rank from small SVD.

    Absolute fallback threshold only avoids dividing roundoff in dependent controls.
    The discarded residual norms are reported, not called algebraic zeros.
    """
    M=matrices.reshape(len(matrices),-1).T
    Q=np.zeros((len(M),len(matrices)));C=np.zeros((len(matrices),len(matrices)));rank=0;discard=[];rows=[]
    for i in range(len(matrices)):
        v=M[:,i].copy();coef=np.zeros(rank)
        for _ in range(2):
            z=Q[:,:rank].T@v;coef+=z;v-=Q[:,:rank]@z
        norm=np.linalg.norm(v);C[:rank,i]=coef
        if norm>1e-14*max(np.linalg.norm(M[:,i]),1e-30):
            Q[:,rank]=v/norm;C[rank,i]=norm;rank+=1
        else:discard.append(float(norm))
        if i+1 in counts:
            current=C[:rank,:i+1];centered=current-current.mean(axis=1,keepdims=True)
            un=rank_details(torch.tensor(current));cen=rank_details(torch.tensor(centered))
            residual=np.linalg.norm(M[:,:i+1]-Q[:,:rank]@current)/max(np.linalg.norm(M[:,:i+1]),1e-30)
            rows.append({'samples':i+1,'uncentered':un,'centered':cen,
                         'sample_cap_centered':i,'sample_cap_uncentered':i+1,
                         'basis_rank':rank,'QR_reconstruction_error':float(residual),
                         'QR_orthogonality_error':float(np.linalg.norm(Q[:,:rank].T@Q[:,:rank]-np.eye(rank))),
                         'largest_discarded_residual':max(discard,default=0.)})
    return rows

def classify(rows,families,complete):
    hard=[r for r in rows if r['case'] not in ('independent','shared_linear','block4')]
    if not complete or not hard:return 'STAGE B2 — INCONCLUSIVE'
    for name in ('packed_exact','online_svd','online_local_residual'):
        if all(any(m['method']==name and m['exact'] and m['all_stored_numbers']<=4*r['P']
                   and m['inclusive_to_inference']<=4 for m in r['online']) for r in hard):
            # Even compact snapshots do not alone establish this gate. Width/depth growth still checked by analysis.
            ratios=[next(m['all_stored_numbers']/r['P'] for m in r['online'] if m['method']==name) for r in hard]
            if max(ratios)/min(ratios)<=c.CFG['normalized_width_horizon_growth_max']:
                return 'STAGE B2 — KNOWN EXACT COMPRESSION CLOSES THE GAP'
    # A sampling ceiling cannot be promoted into the maximum family dimension.
    if any(f['checkpoints'][-1]['centered']['ranks']['1e-08']>=127 for f in families if f['case'] in ('rank1_feedback','full_feedback','deep3','explicit_feedback')):
        return 'STAGE B2 — INCONCLUSIVE'
    # The same snapshot selection must not switch a hard case into/out of the compact gate with tolerance.
    for r in hard:
        minima=[min(m['stored_numbers'] for m in r['compression'] if m['passes'] and m['tolerance']==t)
                for t in c.CFG['reconstruction_tolerances']]
        if min(minima)<=4*r['P']<max(minima):return 'STAGE B2 — INCONCLUSIVE'
    if len(families)!=len(rows):return 'STAGE B2 — INCONCLUSIVE'
    return 'STAGE B2 — COMPRESSION GAP SURVIVES'
