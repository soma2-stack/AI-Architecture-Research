"""Exact support/scope checks and comparison-script provenance; no author imports."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import subprocess

HERE=Path(__file__).resolve().parent
AUTHOR=Path(r'C:\Users\coler\AppData\Local\Temp\ai-hb\theory\claude_hypothesis_b_bus_20261015')


def main():
    n=1500000000000000000
    a=1-Q(1,n); lam=Q(1,100*n); eta=Q(1,10**8*n*n)
    # R=alpha*(R0+eta*11^T/n), alpha=a/||R0+eta*11^T/n||.
    # ||R0+eta J||<=a+eta, so alpha>=a/(a+eta).
    # A source row of (R-R0)1 is alpha*eta-(1-alpha)*lambda.
    source_correction_lower=eta*(a-lam)/(a+eta)
    assert source_correction_lower>0
    assert Q(n,2)>Q(5,10**5)*n
    # Two balanced off-cycle differences are annihilated by J and fixed by O:
    # R(e_i-e_j)=alpha*a*(e_i-e_j). Thus a merge need not be dense.
    result={
        'actual_support_obstruction':{
            'R':'alpha*(R0+eta*11^T/n)',
            'alpha_lower':'a/(a+eta)',
            'source_correction_at_step_2':'-tanh(.05)*(alpha*eta-(1-alpha)*lambda)',
            'absolute_coefficient_lower_exact':str(source_correction_lower),
            'strictly_positive':True,
            'number_of_nonzero_source_inputs_at_step_2':n//2,
            'c0_n':n//20000,
            'conclusion':'Preserving the R0 state path by a dense inverse lift violates actual-support m<=c0*n.'},
        'dense_merge_counterexample':{
            'v':'e_i-e_j, distinct off-cycle memory rows i,j',
            'R_v':'alpha*a*v',
            'two_step_section':'h1(theta)=tanh(.05)*1+z*theta*v; h2(theta)=tanh(R*(tanh(.05)*1)+.05)',
            'step_2_input':'-alpha*a*z*theta*v',
            'peak_support':2,
            'limitation':'Legal for sufficiently small z; demonstrates the sparse-merge inference is false. No robustness claim.'},
        'author_script_hashes':{},
    }
    for source in AUTHOR.glob('*.py'):
        copy=HERE/'author_comparison'/source.name
        if copy.exists():
            hs=hashlib.sha256(source.read_bytes()).hexdigest()
            assert hs==hashlib.sha256(copy.read_bytes()).hexdigest()
            result['author_script_hashes'][source.name]=hs
    for folder in ['ai-hb','ai-ncap','ai-mpm']:
        wd=Path(r'C:\Users\coler\AppData\Local\Temp')/folder
        result[folder]={
            'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=wd,text=True).strip(),
            'status':subprocess.check_output(['git','status','--porcelain'],cwd=wd,text=True).strip(),
        }
        assert not result[folder]['status'],'target PR worktree changed'
    comp=HERE/'author_comparison'
    result['author_results']={}
    for f in comp.glob('*_result.json'):
        result['author_results'][f.name]=json.loads(f.read_text())
    (HERE/'scope_and_provenance.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='author_results'},indent=2))


if __name__=='__main__': main()
