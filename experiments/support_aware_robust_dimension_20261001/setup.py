"""Deterministic chart constants only: no history selection or certification."""
import json,hashlib
from resources import ROOT,Monitor
import core as k
from fractions import Fraction as Q
def main():
 meter=Monitor('CPU setup deterministic fixed-center bases')
 try:
  k.c.hardware();frames={}
  for case in k.INPUT['cases']:
   meter.check();f=k.float_frame(case);m=k.model(case)
   base={'n':m.n,'model':m,'U':[list(map(Q,row)) for row in f['U']]}
   k.mp.mp.dps=100;k.e.I.precision(192)
   f['projectors']={}
   for r in range(1,9):
    f['projectors'][str(r)]={rule:[[str(x) for x in row] for row in k.projectors(base,r,rule)] for rule in (['frame','supported'] if m.diagonal else ['frame'])}
   frames[case['name']]=f
  (ROOT/'frames.json').write_text(json.dumps(frames,indent=2)+'\n')
  (ROOT/'preservation_manifest.json').write_text(json.dumps(k.source_manifest(),indent=2)+'\n')
 finally:meter.finish()
if __name__=='__main__':main()
