import json,sys,math
from fractions import Fraction as Q
import prepare_bounds as p
from resources import Monitor
def main():
  meter=Monitor('CPU structured independent query margins');p.e.I.precision(256);rows=[]
  try:
    for case in p.DATA['cases']:
      if case['case']!='independent':continue
      m=p.model(case);n=case['n'];cert=case['certificate'];diag=[Q(6+3*i,20) for i in range(n)]
      factor=p.e.I(n*max(Q(1),sum(v*v for v in diag))).sqrt()
      margins=[]
      for ell in cert['selected_projection']:
        total=sum(Q(v)**2/diag[i]**2 for v,(i,col) in zip(ell,m.support))
        margin=p.e.I(Q(7,8))/(factor*p.e.I(total).sqrt())
        margins.append(Q(margin.lo,p.e.I.scale))
      rho=list(map(Q,cert['rho_i']));counts=[int(2*a*b//Q(17,8000))+1 for a,b in zip(rho,margins)]
      states=math.prod(counts)
      rows.append({'name':case['name'],'label':'RIGOROUS structural-query diagnostic on unchanged accepted box',
        'mu_structured':[str(v) for v in margins],
        'margin_gain':[float(v/Q(old)) for v,old in zip(margins,cert['mu_i'])],
        'counts':counts,'states':str(states),'bits':math.log2(states),'robust_dimension':sum(v>1 for v in counts),
        'historical_states':int(cert['states']),'historical_bits':cert['bits']})
    (p.ROOT/'structured_margins.json').write_text(json.dumps(rows,indent=2)+'\n')
  finally:meter.finish()
if __name__=='__main__':main()
