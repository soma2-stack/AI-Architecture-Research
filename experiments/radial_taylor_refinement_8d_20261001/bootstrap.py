"""Prospective source preparation; never computes official candidate bounds."""
import os,sys,time,json,hashlib,shutil
from pathlib import Path
for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
os.environ['CUDA_VISIBLE_DEVICES']='-1';sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1];OLD=ROOT.parent/'third_order_antipodal_8d_20261001'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
    assert not (ROOT/'FROZEN.json').exists();cpu=time.process_time();wall=time.perf_counter()
    shutil.copyfile(OLD/'candidate.json',ROOT/'candidate.json');shutil.copyfile(OLD/'reviewed_kernel.py',ROOT/'reference_kernel.py')
    old=(OLD/'reviewed_kernel.py').read_text()
    block="        g=np.array([uq(Q(v.hi,I.scale)) for v in gates])\n        f2=np.array([uq((2*hn[i]*gates[i]).absq()) for i in range(n)])\n        f3=np.array([uq((-2*gates[i]*(I(1)-3*hn[i].square())).absq()) for i in range(n)])\n        f4=np.array([uq((8*hn[i]*gates[i]*(I(2)-3*hn[i].square())).absq()) for i in range(n)])"
    assert old.count(block)==1
    transformed=old.replace(block,'        g,f2,f3,f4=gate_majorants(hn)')
    line='from antipodal_kernel import I,uq,upadd,upmul,upsum,left,abs_array,residual,inverse,matmul\n'
    assert transformed.count(line)==1
    transformed=transformed.replace(line,line+'from exact_gate import gate_majorants\n')
    (ROOT/'refined_kernel.py').write_text(transformed,encoding='utf-8')
    (ROOT/'TRANSFORM.json').write_text(json.dumps({'old_gate_block':block,'replacement':'        g,f2,f3,f4=gate_majorants(hn)',
      'import_added':'from exact_gate import gate_majorants','original_sha256':sha(OLD/'reviewed_kernel.py'),
      'transformed_sha256':sha(ROOT/'refined_kernel.py'),'all_other_source_text_unchanged':True},indent=2)+'\n',encoding='utf-8')
    (ROOT/'config.json').write_text(json.dumps({'r':8,'epsilon':'1/1000','precisions':[192,256],'radial_bins':8,
      'success_rule':'at least double archived weakest absolute slack; all faces pass both precisions',
      'cpu_limit_seconds':1200,'numerical_9d_limit_seconds':120,'workers':1,'device':'CPU'},indent=2)+'\n',encoding='utf-8')
    (ROOT/'setup_resources.json').write_text(json.dumps({'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-wall},indent=2)+'\n',encoding='utf-8')
