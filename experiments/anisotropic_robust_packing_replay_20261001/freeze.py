"""Pin source bytes and separate mathematical inputs from comparison outputs."""
from pathlib import Path
import subprocess, json, hashlib, ast

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
COMMIT='1e4bf42dfa9f1a312d23b4a752738280d5861a4b'
OLD='experiments/anisotropic_robust_packing_20260930/'
WITNESS='experiments/endpoint_width_scaling_20260930/certificate_dense_n3_9602100_full.json'
FILES=[OLD+x for x in ('engine.py','interval.py','test_engine.py','config.json','PROOF.md','basis_dense_n3.json','certificate_frame_dense_n3.json')]+[WITNESS,'experiments/endpoint_width_scaling_20260930/core.py']

def main():
    dest=ROOT/'frozen_sources';dest.mkdir(exist_ok=True)
    manifest=[];blobs={}
    for path in FILES:
        raw=subprocess.check_output(['git','show',COMMIT+':'+path],cwd=REPO)
        name=('width_core.py' if path.endswith('/core.py') else Path(path).name)
        if (dest/name).exists():assert (dest/name).read_bytes()==raw
        else:(dest/name).write_bytes(raw)
        blobs[name]=raw
        manifest.append({'repository_path':path,'snapshot':str((dest/name).relative_to(ROOT)),
                         'sha256':hashlib.sha256(raw).hexdigest(),
                         'working_copy_matches':(REPO/path).read_bytes()==raw,
                         'working_copy_text_matches':(REPO/path).read_bytes().replace(b'\r\n',b'\n')==raw.replace(b'\r\n',b'\n')})
    assert all(x['working_copy_text_matches'] for x in manifest)
    w=json.loads(blobs[Path(WITNESS).name]);basis=json.loads(blobs['basis_dense_n3.json'])
    cert=json.loads(blobs['certificate_frame_dense_n3.json']);cfg=json.loads(blobs['config.json'])
    inputs={'source_commit':COMMIT,'n':3,'T':22,'params':w['params'],'X':w['X'],
            'B':[[*row[:5]] for row in basis['B']],'U':basis['U'][:2],
            'singular_values':basis['singular_values'][:2],
            'K_hidden':cert['K_hidden'],'K_selected':cert['K_selected'],
            'selected_projection':cert['selected_projection'],'rho_i':cert['rho_i'],
            'mu_i':cert['mu_i'],'a_i':cert['a_i'],'normal_half_widths':['1/8']*3,
            'a0':cert['a0'],'profile':cert['profile'],'hidden_factor':cert['hidden_factor'],
            'original_config':cfg,'epsilon':'1/1000'}
    # No generated Jacobian intervals or curvature enclosures enter this file.
    (ROOT/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n',encoding='utf-8')
    (ROOT/'comparison_only.json').write_text(json.dumps(cert,indent=2)+'\n',encoding='utf-8')
    original={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (REPO/OLD).iterdir() if p.is_file()}
    record={'source_commit':COMMIT,'sources':manifest,'original_directory_hashes':original,
            'inputs_sha256':hashlib.sha256((ROOT/'inputs.json').read_bytes()).hexdigest()}
    (ROOT/'input_manifest.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    # Reuse reviewed arithmetic code, never its generated bounds or cache.
    (ROOT/'replay_interval.py').write_bytes(blobs['interval.py'])
    tree=ast.parse(blobs['engine.py'].decode())
    names={'uq','upadd','upmul','upsum','left','abs_array','residual','curvature','query_margins','frame_projection','certify','model_case','dyadic','mpq'}
    chunks=[ast.get_source_segment(blobs['engine.py'].decode(),node) for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in names]
    header='from fractions import Fraction as Q\nimport numpy as np\nimport mpmath as mp\nfrom replay_interval import I,matmul,inverse\nfrom pathlib import Path\nimport json\nCFG=json.loads((Path(__file__).parent/"inputs.json").read_text())["original_config"]\n'
    # Fix the approximate inverses at their frozen rational values. This does
    # not re-fit K to the newly computed midpoint.
    header+='FROZEN=json.loads((Path(__file__).parent/"inputs.json").read_text())\ndef mpinverse(A):\n    key="K_hidden" if len(A)==3 else "K_selected"\n    return [[Q(x) for x in row] for row in FROZEN[key]]\n'
    (ROOT/'reviewed_kernel.py').write_text(header+'\n\n'.join(chunks)+'\n',encoding='utf-8')
    tree=ast.parse(blobs['width_core.py'].decode())
    names={'Model','Jet','jets','forward','autograd','relative','hardware'}
    chunks=[ast.get_source_segment(blobs['width_core.py'].decode(),node) for node in tree.body if isinstance(node,(ast.ClassDef,ast.FunctionDef)) and node.name in names]
    header='import os\nos.environ["CUDA_VISIBLE_DEVICES"]="-1"\nfor key in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS"):os.environ[key]="1"\nimport numpy as np\nimport mpmath as mp\nimport psutil,shutil\nimport torch\nfrom fractions import Fraction as Q\nfrom dataclasses import dataclass\nfrom pathlib import Path\nfrom replay_interval import I\nROOT=Path(__file__).parent\nACTIVE_METER=None\ntorch.set_num_threads(1)\ntorch.set_num_interop_threads(1)\ntorch.set_default_dtype(torch.float64)\ntorch.use_deterministic_algorithms(True)\n'
    (ROOT/'replay_jets.py').write_text(header+'\n\n'.join(chunks)+'\n',encoding='utf-8')
    prereg={'task':'clean execution of frozen width-3 two-axis certificate; no search',
            'source_commit':COMMIT,'normal_precision_bits':192,'verification_bits':256,
            'high_precision_digits':100,'n':3,'T':22,'epsilon':'1/1000',
            'axes':2,'normal_axes':3,'amplitudes':['1/8']*5,
            'no_original_J_intervals_or_curvature_used':True,
            'regenerate_basis_chart':'use frozen rational directions; freshly recompute chart derivatives and independently check QR/SVD basis',
            'fixed_preconditioners_and_target':'test frozen K, rho, mu, not regenerated replacements',
            'rounding':'source interval dyadic/Taylor arithmetic and ordered upward IEEE binary64 majorants unchanged',
            'max_cpu_seconds':600,'rss_cap_bytes':2147483648,'workers':1,'gpu_allowed':False,
            'stop':'first failed certificate inequality; preserve evidence; no constants or axes adjusted',
            'classification':'exact regeneration versus outward differences; failure has priority',
            'comparison_only':'original bounds inspected only for final comparison, not fed to replay',
            'code_independence':'fresh isolated execution of pinned reviewed interval/jet/curvature source, not an independently authored interval library'}
    (ROOT/'preregistration.json').write_text(json.dumps(prereg,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'inputs_sha256':record['inputs_sha256'],'sources':len(manifest),'frozen':True}))

if __name__=='__main__':main()
