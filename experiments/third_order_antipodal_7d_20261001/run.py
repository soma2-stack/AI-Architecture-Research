"""One immutable 7D candidate, independently regenerated at both precisions."""
import sys,time,subprocess,traceback
sys.dont_write_bytecode=True
CPU=time.process_time(); WALL=time.perf_counter()
import common as c
k=c.k; Q=c.Q; np=c.np
c.verify(); f=c.json.loads((c.ROOT/'CANDIDATE_FROZEN.json').read_text())
assert f['method_sha256']==c.sha(c.ROOT/'METHOD_FROZEN.json')
assert all(c.sha(c.ROOT/p)==h for p,h in f['sha256'].items())
assert not (c.ROOT/'result.json').exists()
d=c.json.loads((c.ROOT/'candidate.json').read_text())
prior=sum(c.json.loads((c.ROOT/p).read_text())['cpu_seconds'] for p in ('tests.json','bootstrap_resources.json','selection_resources.json'))
s=c.json.loads((c.ROOT/'search_summary.json').read_text())
prior+=s['parent_cpu_seconds']+s['worker_cpu_seconds']
cfg=c.json.loads((c.ROOT/'config.json').read_text()); assert prior<cfg['total_cpu_limit']
k.CPU_START=CPU
history_manifest=c.json.loads((c.OLD/'BYTE_EXACT_ARCHIVE.json').read_text())
historical_before={str(p.relative_to(c.ACCEPTED)):c.sha(p) for p in c.ACCEPTED.rglob('*') if p.is_file()}
record={'status':'INCOMPLETE','epsilon':'1/1000','r':7,'freeze_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=c.REPO,text=True).strip(),
    'candidate_sha256':c.sha(c.ROOT/'candidate.json'),'attempts':[]}
try:
    record['hardware']=k.a.c.hardware()
    B=[[Q(v) for v in row] for row in d['B']]; L=[[Q(v) for v in row] for row in d['L']]
    Kh=[[Q(v) for v in row] for row in d['K_hidden']]; K=[[Q(v) for v in row] for row in d['K_selected']]
    aa=list(map(Q,d['a'])); ah=Q(d['ah']); n=4; r=7
    for bits in (192,256):
        assert time.process_time()-CPU+prior<cfg['total_cpu_limit']
        t=time.process_time(); base=k.a.base_for(d['endpoint'],B,bits,JI=None)
        assert base['model'].serialize()==d['model_parameters']
        out,bounds=k.certify(base,aa,ah,L,Kh,K)
        assert base['model'].serialize()==d['model_parameters']
        np.savez_compressed(c.ROOT/f'bounds_{bits}.npz',**bounds)
        # Frozen-tensor decomposition only, not a replacement certificate.
        if out.get('valid'):
            amps=np.array([k.uq(v) for v in [ah]*n+aa]); au=np.array([k.uq(v) for v in aa])
            V=np.vstack([out['normal_first_derivative_upper'],np.eye(r)])
            W2=np.vstack([bounds['y2'],np.zeros((r,r,r))])
            Sn=k.upadd(k.abs_array([row[:n] for row in base['reduced'][n:]]),
                k.upsum(k.upmul(bounds['HS'][:,:n,:],amps[None,None,:]),axis=2))
            parts={'direct':k.contract3(bounds['HS3'],V),
                   'mixed':k.mixed_chain(bounds['HS'],W2,V),'implicit':k.left(Sn,bounds['y3'])}
            dec={}
            for name,tensor in parts.items():
                selected=k.left(k.abs_array(L),tensor)
                cub=k.upsum(k.upsum(k.upsum(k.times(selected,au[None,:,None,None],au[None,None,:,None],au[None,None,None,:]),axis=3),axis=2),axis=1)
                dec[name]=k.upmul(k.left(k.abs_array(K),cub[:,None])[:,0],np.array([k.uq(1/v) for v in aa])).tolist()
            c.write(f'remainder_decomposition_{bits}.json',{'label':'upper majorants, not actual curvature','M3_components':dec})
        record['attempts'].append({'precision':bits,'cpu_seconds':time.process_time()-t,'certificate':out})
        c.write('result.json',record)
        print(bits,'PASS' if out.get('all_antipodal_faces_pass') else 'FAIL',out.get('reason'),
            'weakest',float(Q(out['weakest_beta'])) if out.get('weakest_beta') else None,flush=True)
        assert k.a.c.psutil.Process().memory_info().rss<2*1024**3
    record['status']='PASS' if all(x['certificate'].get('all_antipodal_faces_pass') for x in record['attempts']) else 'FAIL'
except Exception:
    record['status']='INVALID / INCOMPLETE';record['error']=traceback.format_exc()
finally:
    record.update(cpu_seconds=time.process_time()-CPU,wall_seconds=time.perf_counter()-WALL,
        prior_cpu_seconds=prior,total_cpu_seconds=prior+time.process_time()-CPU,
        peak_working_set_bytes=k.a.c.psutil.Process().memory_info().peak_wset,gpu_seconds=0,gpu_used=False,
        historical_6d_unchanged=all(c.sha(c.ACCEPTED/p)==h for p,h in historical_before.items()),
        historical_antipodal_unchanged=all(c.sha(c.OLD/p)==h for p,h in history_manifest['sha256'].items()))
    c.write('result.json',record); print(record['status'],record['total_cpu_seconds'],flush=True)
