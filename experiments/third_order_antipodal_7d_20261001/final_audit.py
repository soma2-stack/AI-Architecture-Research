"""Read-only cross-precision bounds and frozen-input bookkeeping audit."""
import sys,time
sys.dont_write_bytecode=True
CPU=time.process_time(); WALL=time.perf_counter()
import common as c
Q=c.Q; c.verify()
d=c.json.loads((c.ROOT/'candidate.json').read_text()); f=c.json.loads((c.ROOT/'CANDIDATE_FROZEN.json').read_text())
checks=[]
def add(name,v):checks.append({'name':name,'passed':bool(v)})
add('candidate freeze hashes',all(c.sha(c.ROOT/p)==h for p,h in f['sha256'].items()))
chart=c.json.loads((c.ROOT/'bases.json').read_text())[d['selection']['kind']]
add('same prospectively frozen basis',d['B']==chart['B'] and d['L']==chart['L'])
add('exact tangent down-rounding',all(Q(v)<=Q(float(w)) and Q(float(w))-Q(v)<Q(1,2**20) for v,w in zip(d['a'],d['selection']['a'])))
t=Q(float(d['selection']['ah']))*Q(51,50)
add('exact normal up-rounding',Q(d['ah'])>=t and Q(d['ah'])-t<Q(1,2**20))
a=c.np.load(c.ROOT/'bounds_192.npz'); b=c.np.load(c.ROOT/'bounds_256.npz')
add('same bound arrays',set(a.files)==set(b.files))
for name in a.files:add('identical cross-precision '+name,c.np.array_equal(a[name],b[name]))
add('CPU only',c.k.a.c.torch.version.cuda is None and c.k.a.c.torch.ones(1).device.type=='cpu')
out={'passed':all(v['passed'] for v in checks),'checks':checks,'cpu_seconds':time.process_time()-CPU,
    'wall_seconds':time.perf_counter()-WALL,'peak_working_set_bytes':c.k.a.c.psutil.Process().memory_info().peak_wset}
c.write('final_audit.json',out);print('FINAL AUDIT',out['passed'],len(checks))
