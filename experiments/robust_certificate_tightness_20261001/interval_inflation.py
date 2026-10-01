"""Precision-inflation check of raw majorants, not a new product certificate."""
import json
from fractions import Fraction as Q
import numpy as np
import prepare_bounds as p
from resources import Monitor
def main():
  meter=Monitor('CPU interval precision slack');rows=[]
  try:
    for case in p.DATA['cases']:
      meter.check();m=p.model(case);n=case['n'];cert=case['certificate'];r=cert['r'];p.e.I.precision(256)
      scales={g:p.e.I(sum(m.params[col]**2 for col,(_,_,name,_) in enumerate(m.meta) if name==g)/sum(name==g for _,_,name,_ in m.meta)).sqrt() for g in ['R','W','b']}
      base={'n':n,'model':m,'X':[[Q(v) for v in row] for row in case['X']],
        'BI':[[p.e.I(Q(v))*p.e.I(Q(3,32)).sqrt() for v in row[:n+r]] for row in case['B']], 'scaleI':scales}
      amp=[Q(cert['a0'])*Q(cert['hidden_factor'])]*n+list(map(Q,cert['a_i']))
      high=p.e.curvature(base,r,amp);low=np.load(p.ROOT/f"bounds_{case['name']}.npz")
      row={'name':case['name'],'comparison_bits':[192,256],'scope':'same outward raw majorant, precision inflation only'}
      for tag,A in zip(['HH','HS'],high):
        B=low[tag];row[tag+'_relative_linf_change']=float(np.max(np.abs(A-B))/max(np.max(B),1e-300))
        row[tag+'_max_entrywise_relative_change']=float(np.max(np.abs(A-B)/np.maximum(B,1e-300)))
      rows.append(row)
    (p.ROOT/'interval_inflation.json').write_text(json.dumps(rows,indent=2)+'\n')
  finally:meter.finish()
if __name__=='__main__':main()
