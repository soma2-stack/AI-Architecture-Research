"""Official fresh generation; immutable r=8 candidate, no fallback or search."""
import time,subprocess,traceback
CPU=time.process_time();WALL=time.perf_counter()
import common as c
from fractions import Fraction as Q
k=c.k;np=k.np
if __name__=='__main__':
    c.verify();cfg=c.json.loads((c.ROOT/'config.json').read_text());d=c.candidate()
    assert not (c.ROOT/'result.json').exists(),'Refuse to overwrite measured evidence'
    prior=sum(c.json.loads((c.ROOT/n).read_text())['cpu_seconds'] for n in ('setup_resources.json','tests.json'))
    failed_charge=c.json.loads((c.ROOT/'preofficial_repair.json').read_text())['charged_cpu_seconds']
    prior+=failed_charge
    record={'status':'INCOMPLETE','r':8,'epsilon':'1/1000','attempts':[],
       'freeze_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=c.REPO,text=True).strip(),
       'candidate_sha256':c.sha(c.ROOT/'candidate.json')}
    try:
        record['hardware']=k.a.c.hardware();k.CPU_START=CPU
        B,L,Kh,K=[c.rational_rows(d[key]) for key in ('B','L','K_hidden','K_selected')]
        aa=list(map(Q,d['a']));ah=Q(d['ah'])
        for bits in cfg['precisions']:
            assert time.process_time()-CPU+prior<cfg['cpu_limit_seconds']
            t=time.process_time();base=k.a.base_for(d['endpoint'],B,bits,JI=None)
            assert base['model'].serialize()==d['model_parameters']
            out,bounds=k.certify(base,aa,ah,L,Kh,K)
            assert base['model'].serialize()==d['model_parameters']
            np.savez_compressed(c.ROOT/f'bounds_{bits}.npz',**bounds)
            # Human-readable metadata only; accepted generic-r equations unmodified.
            out['reviewed_kernel_reason_raw']=out.get('reason')
            if out.get('all_antipodal_faces_pass'):out['reason']='8D antipodal certificate passes'
            record['attempts'].append({'precision':bits,'cpu_seconds':time.process_time()-t,'certificate':out})
            c.write('result.json',record)
            print(bits,'PASS' if out.get('all_antipodal_faces_pass') else 'FAIL',out.get('reason'),
                  'weakest_beta',float(Q(out['weakest_beta'])) if out.get('weakest_beta') else None,flush=True)
            assert k.a.c.psutil.Process().memory_info().rss<cfg['ram_limit_bytes']
        record['status']='PASS' if all(a['certificate'].get('all_antipodal_faces_pass') for a in record['attempts']) else 'FAIL'
    except Exception:
        record['status']='INVALID / INCOMPLETE';record['error']=traceback.format_exc()
    finally:
        record.update(cpu_seconds=time.process_time()-CPU,wall_seconds=time.perf_counter()-WALL,
          prior_cpu_seconds=prior,total_cpu_seconds=prior+time.process_time()-CPU,failed_test_CPU_charge=failed_charge,
          peak_ram_bytes=k.a.c.psutil.Process().memory_info().peak_wset,gpu_used=False,gpu_seconds=0)
        c.write('result.json',record);print(record['status'],record['total_cpu_seconds'],flush=True)
