"""Prospective method/basis freeze. No new robust-score evaluation here."""
import sys,time,subprocess
sys.dont_write_bytecode=True
CPU=time.process_time(); WALL=time.perf_counter()
import common as c
assert not (c.ROOT/'METHOD_FROZEN.json').exists(),'Do not overwrite prospective freeze'
dy=lambda v:str(c.Q(round(float(v)*2**128),2**128))
fixtures={}
for kind in ('top','skip'):
    ep,B,L,s,full=c.basis(kind,7)
    fixtures[kind]={'B':[[dy(v) for v in row] for row in B],
                    'L':[[dy(v) for v in row] for row in L],'sigma':s.tolist(),'full9_sigma':full.tolist()}
c.write('bases.json',fixtures)
c.write('config.json',{'n':4,'T':37,'r':7,'P':24,'epsilon':'1/1000','search_workers':2,
    'seeds':[271071,271072],'maxfev':500,'worker_cpu_limit':400,'total_cpu_limit':2400,
    'precisions':[192,256],'initial_hidden_grid':[.005,.01,.02,.04,.08,.16],
    'normal_padding':'51/50','amplitude_dyadic_bits':20,'basis_dyadic_bits':128,
    '8d_scales':[.5,.75,1.,1.25],'numpy':c.np.__version__,'torch':c.k.a.c.torch.__version__,
    'accepted_method':str(c.ACCEPTED.relative_to(c.REPO)).replace('\\','/'),
    'accepted_by_owner_report':'6D THIRD-ORDER CERTIFICATE VERIFIED (Claude review)'} )
c.write('bootstrap_resources.json',{'cpu_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,
     'peak_working_set_bytes':c.k.a.c.psutil.Process().memory_info().peak_wset})
assert c.json.loads((c.ROOT/'tests.json').read_text())['passed']
c.write('METHOD_FROZEN.json',{'parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True,cwd=c.REPO).strip(),
    'local_sha256':{p.name:c.sha(p) for p in sorted(c.ROOT.iterdir()) if p.is_file() and p.name!='METHOD_FROZEN.json'},
    'source_sha256':c.sources(), 'prospective':'no new search scores or official certificate yet'})
print('Prospective method freeze written; two fixed bases; no robust score evaluated')
