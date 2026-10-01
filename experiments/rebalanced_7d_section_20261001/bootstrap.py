import sys,time,subprocess
sys.dont_write_bytecode=True
CPU=time.process_time();WALL=time.perf_counter()
import common as c
assert not (c.ROOT/'METHOD_FROZEN.json').exists()
assert c.json.loads((c.ROOT/'tests.json').read_text())['passed']
c.k.a.c.hardware();c.write('bases.json',c.fixtures())
c.write('config.json',{'n':4,'T':37,'P':24,'r':7,'epsilon':'1/1000','seeds':[302701,302702],
    'bases':['original','plus','minus'],'maxfev':800,'worker_cpu_limit':320,'total_cpu_limit':2400,
    'normal_grid':[.005,.008,.012,.02,.04,.08,.16],'precision_bits':[192,256],
    'numpy':c.np.__version__,'torch':c.k.a.c.torch.__version__,'device':'cpu','workers':2})
c.write('bootstrap_resources.json',{'cpu_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,
    'peak_working_set_bytes':c.k.a.c.psutil.Process().memory_info().peak_wset})
c.write('METHOD_FROZEN.json',{'parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=c.REPO,text=True).strip(),
    'local_sha256':{p.name:c.sha(p) for p in c.ROOT.iterdir() if p.is_file()},'source_sha256':c.sources(),
    'prospective':'No fresh numerical amplitude scores or official bounds exist'})
print('Prospective method freeze complete')
