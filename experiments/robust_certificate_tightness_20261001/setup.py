from pathlib import Path
import json,hashlib
ROOT=Path(__file__).parent
REPO=ROOT.parents[1]
OLD=REPO/'experiments/robust_witness_search_20261001'
ARCH=REPO/'experiments/anisotropic_robust_packing_20260930'
def save(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
def main():
    assert not (ROOT/'config.json').exists()
    cfg={'epsilon':'1/1000','widths':[3,4],'horizons':{'3':22,'4':37},
      'source_commit':'7cb9f3d','cleanup_commit':'1e17cb8','seed':9810101,
      'raw_history_count_per_width':32,'curvature_sobol':512,'packing_sobol':2048,
      'max_grid_dimension':12,'base_grid_dimension':10,'max_prefix':16,
      'amplitudes':[.125,.25,.5,1.],'normal_coordinate_cap':1.,'history_coordinate_radius':1.,
      'newton_tolerance':2e-12,'newton_steps':18,'strict_numerical_separation':.00205,
      'greedy_states_cap':512,'max_cpu_seconds':3600,'max_gpu_wall_seconds':3600,
      'rss_cap_bytes':4*2**30,'device_allocation_cap_bytes':4*2**30,
      'workers':1,'gpu_stop_temperature_c':86,'gpu_preferred_temperature_c':80,
      'normalization':'unchanged sqrt(3/32) input SD and parameter-group RMS, accepted head/beta',
      'levels':'A old certificates; B numerical finite packings; C failed finite trials and loose rigorous cover'}
    save('config.json',cfg)
    wins=json.loads((OLD/'frozen_winners.json').read_text())
    certs=json.loads((OLD/'certification_results.json').read_text())
    models=json.loads((OLD/'models.json').read_text())
    cases=[]
    for n in cfg['widths']:
      for family in ['dense','independent']:
        for kind in ['archived','confirmation']:
          if kind=='confirmation':
            w=next(x for x in wins if x['n']==n and x['case']==family and x['role']=='untouched_confirmation')
            row=next(x for x in certs if x['n']==n and x['case']==family and x['role']=='untouched_confirmation')
            cert=row['result'];B=w['B'];U=w['U'];X=w['X'];idx=row['index']
            source=f'experiments/robust_witness_search_20261001/certificates/curvature_{idx}_192.npz'
          else:
            basis=json.loads((ARCH/f'basis_{family}_n{n}.json').read_text())
            cert=json.loads((ARCH/f'certificate_frame_{family}_n{n}.json').read_text())
            B=basis['B'];U=basis['U'];X=models['baseline_histories'][str(n)];source=None
          cases.append({'name':f'{family}_n{n}_{kind}','n':n,'case':family,'kind':kind,
            'X':X,'B':B,'U':U,'certificate':cert,'curvature_source':source})
    save('inputs.json',{'models':models,'cases':cases})
    preserve={}
    for parent in [OLD,ARCH]:
      for f in parent.rglob('*'):
        if f.is_file() and not any(v in f.parts for v in ['.venv','__pycache__']):
          preserve[f.relative_to(REPO).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
    save('preservation_manifest.json',preserve)
    print('Frozen eight endpoints; old artifacts remain read-only.')
if __name__=='__main__':main()
