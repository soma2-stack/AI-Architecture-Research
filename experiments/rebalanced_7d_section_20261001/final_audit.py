import sys,time
sys.dont_write_bytecode=True
CPU=time.process_time();WALL=time.perf_counter()
import common as c
c.verify();Q=c.Q
d=c.json.loads((c.ROOT/'candidate.json').read_text());f=c.json.loads((c.ROOT/'CANDIDATE_FROZEN.json').read_text())
checks=[]
def add(name,value):checks.append({'name':name,'passed':bool(value)})
add('candidate freeze hashes',all(c.sha(c.ROOT/p)==h for p,h in f['sha256'].items()))
chart=c.json.loads((c.ROOT/'bases.json').read_text())[d['selection']['kind']]
add('prospective basis unchanged',chart['B']==d['B'] and chart['L']==d['L'])
aa,h=c.round_widths(d['selection']['raw_a'],d['selection']['raw_ah'])
add('exact final rounding',list(map(str,aa))==d['a'] and str(h)==d['ah'])
control=c.json.loads((c.CONTROL/'OUTPUT_MANIFEST.json').read_text())
add('all historical failed-box evidence unchanged',all(c.sha(c.CONTROL/p)==v for p,v in control['sha256'].items()))
source=c.json.loads((c.ROOT/'SOURCE_TRANSFORM.json').read_text());text=(c.ACCEPTED/'kernel.py').read_text()
for a,b in source['kernel_replacements']:text=text.replace(a,b)
add('only two predeclared bound substitutions',text==(c.ROOT/'kernel.py').read_text())
a=c.np.load(c.ROOT/'bounds_192.npz');b=c.np.load(c.ROOT/'bounds_256.npz')
add('same precision array names',set(a.files)==set(b.files))
for name in a.files:add('same bound '+name,c.np.array_equal(a[name],b[name]))
add('CPU only',c.k.a.c.torch.version.cuda is None)
c.write('final_audit.json',{'passed':all(v['passed'] for v in checks),'checks':checks,
    'cpu_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,
    'peak_working_set_bytes':c.k.a.c.psutil.Process().memory_info().peak_wset})
print('FINAL AUDIT',all(v['passed'] for v in checks),len(checks))
