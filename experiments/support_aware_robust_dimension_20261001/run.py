"""Official fixed-center interval sweep; no model/history optimization."""
from resources import ROOT,CFG,Monitor
import core as k
import json,hashlib,traceback
from fractions import Fraction as Q
import numpy as np

def dump(name,obj):
 (ROOT/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
def rank(row):
 d=row['dimension'];return (d['epsilon_essential_dimension'],float(Q(d['antipodal_half_margin_lower'])),-float(Q(row['certificate']['a0'])))
def do_trial(base,r,a,profile,L,HH=None,HS=None):
 original=k.e.curvature;captured={}
 def capture(*args):
  h,s=original(*args) if HH is None else (HH,HS)
  captured.update(HH=h,HS=s);return h,s
 k.e.curvature=capture
 try:out=k.e.certify(base,r,a,profile,Q(1),L,True)
 finally:k.e.curvature=original
 return out,captured

def main():
 meter=Monitor('CPU official continuous dimension intervals');frames=json.loads((ROOT/'frames.json').read_text());rows=[]
 frozen=json.loads((ROOT/'FROZEN_SETUP.json').read_text())
 try:
  for name,h in frozen['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
  for name,h in json.loads((ROOT/'preservation_manifest.json').read_text()).items():assert hashlib.sha256((k.REPO/name).read_bytes()).hexdigest()==h,name
  k.c.hardware()
  cases=sorted(k.INPUT['cases'],key=lambda x:(x['case']!='independent',-x['n'],x['kind']!='confirmation'))
  for case in cases:
   meter.check();name=case['name'];print('START',name,flush=True)
   base=k.base_for(case,frames[name],192,meter)
   accepted=k.base_for(case,k.current_frame(case),192,meter,base['JI'])
   bounds=np.load(k.REPO/f'experiments/robust_certificate_tightness_20261001/bounds_{name}.npz')
   old=case['certificate']
   old_dims=[k.dimension_bound(accepted,old,bounds['HH'],bounds['HS'],Q(f)) for f in CFG['subproduct_fractions']]
   oldrow={'case':name,'source':'accepted geometry','certificate':old,'dimension':old_dims[0],'subproducts':old_dims,'frame':k.current_frame(case)}
   best=oldrow;bestbounds={'HH':bounds['HH'],'HS':bounds['HS']};trials=[]
   for r in CFG['prefixes']:
    for astr in CFG['amplitudes']:
     a=Q(astr)
     for profile in CFG['profiles']:
      meter.check();cached=None
      for rule,Lstr in frames[name]['projectors'][str(r)].items():
       L=[list(map(Q,line)) for line in Lstr]
       aa=[a]*r if profile=='equal' else [a*x/base['sigma'][0] for x in base['sigma'][:r]]
       amps=[a]*case['n']+aa
       maxradius=max(sum(x.absq()*amp for x,amp in zip(line,amps)) for line in base['BI'])
       info={'r':r,'a0':astr,'profile':profile,'projection':rule,'max_raw_history_radius':str(maxradius)}
       if maxradius>1:info.update(valid=False,reason='outside fixed local domain');trials.append(info);continue
       out,curv=do_trial(base,r,a,profile,L,**(cached or {}));cached=curv
       info.update(valid=out['valid'],reason=out.get('reason'),eta_h=out.get('eta_h',out.get('eta_hidden')),eta=out.get('eta',out.get('eta_sensitivity')))
       if out['valid']:
        d=k.dimension_bound(base,out,curv['HH'],curv['HS']);info['dimension']=d
        row={'case':name,'source':'new fixed-center thin section','certificate':out,'dimension':d,'frame':frames[name],'projection':rule,'recipe':{'r':r,'a0':astr,'profile':profile}}
        if rank(row)>rank(best):best=row;bestbounds=curv
       trials.append(info)
    print('PREFIX',name,r,'best essential',best['dimension']['epsilon_essential_dimension'],flush=True)
    dump(f'trials_{name}.json',trials)
   best['accepted_dimension']=old_dims[0];best['accepted_subproducts']=old_dims
   best['trials_count']=len(trials)
   np.savez_compressed(ROOT/f'best_bounds_{name}_192.npz',**bestbounds)
   if best['source']!='accepted geometry':
    meter.check();high=k.base_for(case,frames[name],256,meter);out=best['certificate'];r=out['r']
    # Freeze both rational preconditioners for the precision cross-check.
    L=[list(map(Q,line)) for line in out['selected_projection']];J=[line[:case['n']+r] for line in high['reduced']]
    H0=[line[:case['n']] for line in J[:case['n']]];Ht=[line[case['n']:] for line in J[:case['n']]]
    JP=k.e.matmul([[k.e.I(x) for x in line] for line in L],J[case['n']:])
    cross=k.e.matmul([line[:case['n']] for line in JP],k.e.matmul(k.e.inverse(H0),Ht))
    C0=[[JP[i][case['n']+j]-cross[i][j] for j in range(r)] for i in range(r)]
    Kh=[list(map(Q,line)) for line in out['K_hidden']];K=[list(map(Q,line)) for line in out['K_selected']]
    high['_center_cache']={(256,r,tuple(tuple(line) for line in L)):(Kh,k.e.abs_array(Kh),k.e.residual(Kh,H0),K,k.e.residual(K,C0),k.structured_query(high,L)[0])}
    verified,cb=do_trial(high,r,Q(out['a0']),out['profile'],L)
    assert verified['valid'],'Selected 256-bit geometry invalid'
    # Check the ORIGINAL 192-bit product radii against regenerated outward bounds.
    rho=list(map(Q,out['rho_i']));aa=list(map(Q,out['a_i']))
    assert all(sum(abs(K[j][i])*rho[i] for i in range(r))<=(1-Q(verified['eta_sensitivity']))*aa[j] for j in range(r))
    asserted=dict(verified);asserted['rho_i']=out['rho_i']
    hd=k.dimension_bound(high,asserted,cb['HH'],cb['HS'])
    assert hd['epsilon_essential_dimension']>=best['dimension']['epsilon_essential_dimension']
    best['verification_256']={'passed':True,'dimension':hd,'eta_hidden':verified['eta_hidden'],'eta_sensitivity':verified['eta_sensitivity'],'fixed_preconditioners':True}
    np.savez_compressed(ROOT/f'best_bounds_{name}_256.npz',**cb)
   else:best['verification_256']={'passed':True,'scope':'accepted reviewed geometry; new rational/interval dimension conversion only'}
   dump(f'result_{name}.json',best);rows.append(best)
   print('FINAL',name,best['dimension']['epsilon_essential_dimension'],'min margin',float(Q(best['dimension']['antipodal_half_margin_lower'])),flush=True)
  dump('results.json',rows)
 except Exception:
  dump('FAILURE.json',{'traceback':traceback.format_exc(),'partial':rows});raise
 finally:meter.finish()
if __name__=='__main__':main()
