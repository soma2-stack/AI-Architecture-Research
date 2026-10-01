"""Immutable rigorous 8D control/refinement, at 192 and 256 bits."""
import time,subprocess,traceback
CPU=time.process_time();WALL=time.perf_counter()
import common as c
from elimination import coefficients,prefix_bound
from fractions import Fraction as Q
import numpy as np
if __name__=='__main__':
    c.verify();d=c.candidate();cfg=c.json.loads((c.ROOT/'config.json').read_text())
    assert not (c.ROOT/'result8.json').exists()
    assert d['r']==8 and Q(d['epsilon'])==Q(1,1000)
    prior=c.json.loads((c.ROOT/'setup_resources.json').read_text())['cpu_seconds']+c.json.loads((c.ROOT/'tests.json').read_text())['CPU_seconds']
    archived=c.json.loads((c.REPO/'experiments/third_order_antipodal_8d_20261001/result.json').read_text())
    baseline=min(Q(v) for x in archived['attempts'] for v in x['certificate']['beta3'])
    target=Q(1,1000)+2*(baseline-Q(1,1000))
    record={'status':'INCOMPLETE','freeze_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=c.REPO,text=True).strip(),
            'candidate_sha256':c.sha(c.ROOT/'candidate.json'),'baseline_beta':str(baseline),'success_target_beta':str(target),'attempts':[]}
    try:
        record['hardware']=c.ref.a.c.hardware();c.ref.CPU_START=c.tight.CPU_START=CPU-prior
        aa=list(map(Q,d['a']));ah=Q(d['ah']);B,L,Kh,K=[c.rows(d[v]) for v in ('B','L','K_hidden','K_selected')]
        ell=[[sum(K[i][j]*L[j][p] for j in range(8))/aa[i] for p in range(24)] for i in range(8)]
        for bits in (192,256):
            t0=time.process_time();base=c.ref.a.base_for(d['endpoint'],B,bits,JI=None)
            assert base['model'].serialize()==d['model_parameters']
            ctrl,arrays=c.ref.certify(base,aa,ah,L,Kh,K)
            assert ctrl['all_antipodal_faces_pass'] and ctrl['valid']
            oldnp=np.load(c.REPO/f'experiments/third_order_antipodal_8d_20261001/bounds_{bits}.npz')
            assert all(np.array_equal(arrays[name],oldnp[name]) for name in arrays)
            np.savez_compressed(c.ROOT/f'control_bounds_{bits}.npz',**arrays)
            CS,CH,coeffmeta=coefficients(base,ell)
            coeffmeta.update(CS=[[[str(Q(x.lo,c.ref.I.scale)),str(Q(x.hi,c.ref.I.scale))] for x in row] for row in CS],
                             CH=[[[str(Q(x.lo,c.ref.I.scale)),str(Q(x.hi,c.ref.I.scale))] for x in row] for row in CH])
            c.write(f'coefficients_{bits}.json',coeffmeta)
            native,arr=prefix_bound(base,aa,Q(1),CS,CH,c.ref)
            np.savez_compressed(c.ROOT/f'elimination_native_{bits}.npz',**arr)
            bands=[]
            for j in range(1,9):
                if time.process_time()-CPU+prior>1080:raise TimeoutError('Certification reserve exhausted')
                lam=Q(j,8);M,arr=prefix_bound(base,aa,lam,CS,CH,c.tight)
                assert base['model'].serialize()==d['model_parameters']
                np.savez_compressed(c.ROOT/f'prefix_{bits}_{j}.npz',**arr)
                weight=((1-Q(j-1,8))**3-(1-lam)**3)/3
                used=[min(v,Q(ctrl['M3_upper'][i])) for i,v in enumerate(M)]
                bands.append({'upper_radius':str(lam),'weight':str(weight),'M3_original_direction':list(map(str,M)),
                              'M3_used':list(map(str,used))})
                c.write(f'radial_progress_{bits}.json',{'bands':bands,'CPU_seconds':time.process_time()-CPU+prior})
                print(bits,'radial',j,'/8',flush=True)
            e=list(map(Q,ctrl['center_rows_upper']));mu=list(map(Q,ctrl['mu_tilde']))
            penalty=[sum(Q(b['weight'])*Q(b['M3_used'][i])/2 for b in bands) for i in range(8)]
            beta=[mu[i]*(1-e[i]-penalty[i]) for i in range(8)]
            native_beta=[mu[i]*(1-e[i]-native[i]/6) for i in range(8)]
            sharp_whole=[mu[i]*(1-e[i]-Q(bands[-1]['M3_original_direction'][i])/6) for i in range(8)]
            record['attempts'].append({'bits':bits,'control':ctrl,'bands':bands,'native_elimination_M3':list(map(str,native)),
              'native_elimination_beta':list(map(str,native_beta)),'sharp_whole_beta':list(map(str,sharp_whole)),
              'integrated_half_remainder':list(map(str,penalty)),'beta':list(map(str,beta)),
              'all_faces_pass':all(v>Q(1,1000) for v in beta),'substantial':min(beta)>=target,
              'CPU_seconds':time.process_time()-t0})
            c.write('result8.json',record)
            print(bits,'new weakest separation',float(2*min(beta)), 'slack%',float(min(beta)/Q(1,1000)-1)*100,flush=True)
        record['status']='SUBSTANTIAL IMPROVEMENT' if all(x['all_faces_pass'] and x['substantial'] for x in record['attempts']) else 'IMPROVEMENT CRITERION FAILED'
    except Exception:
        record['status']='INVALID / INCOMPLETE';record['error']=traceback.format_exc()
    finally:
        record.update(CPU_seconds=time.process_time()-CPU,prior_CPU_seconds=prior,total_CPU_seconds=time.process_time()-CPU+prior,
          wall_seconds=time.perf_counter()-WALL,peak_RAM_bytes=c.ref.a.c.psutil.Process().memory_info().peak_wset,GPU_seconds=0)
        c.write('result8.json',record);print(record['status'],record['total_CPU_seconds'],flush=True)
