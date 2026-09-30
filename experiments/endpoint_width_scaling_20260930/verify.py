"""Replay rational interval endpoints; verify invertibility with independent Fraction arithmetic."""
import core as c
import json
from fractions import Fraction as Q
from interval import I

def verify(data):
    I.precision(data['bits']);model=c.Model(data['model'],data.get('width',2));assert model.serialize()==data['params']
    X=[[Q(v) for v in row] for row in data['X']]
    _,J,_=c.jets(model,X,'interval');scale=I.scale
    rows=data['rows'];cols=data['columns'];size=len(rows)
    assert len(cols)==size
    bounds=[]
    for i in range(size):
        if c.ACTIVE_METER is not None:c.ACTIVE_METER.check()
        rr=[]
        for k in range(size):
            v=I.cast(J[rows[i],cols[k]]);saved=data['J_intervals'][i][k]
            assert v.lo==int(saved[0]) and v.hi==int(saved[1])
            rr.append((Q(v.lo,scale),Q(v.hi,scale)))
        bounds.append(rr)
    M=[[Q(int(v),scale) for v in row] for row in data['preconditioner']]
    maximum=Q(0)
    for i in range(size):
        if c.ACTIVE_METER is not None:c.ACTIVE_METER.check()
        row_bound=Q(0)
        for j in range(size):
            lo=hi=Q(0)
            for k in range(size):
                v=M[i][k];a,b=bounds[k][j];lo+=v*(a if v>=0 else b);hi+=v*(b if v>=0 else a)
            unit=1 if i==j else 0;row_bound+=max(abs(unit-hi),abs(unit-lo))
        maximum=max(maximum,row_bound)
    assert maximum<1,'Nonzero certificate fails'
    return {'verified':True,'size':size,'label':data['label'],'fraction_residual_bound':str(maximum),
            'binary_residual_bound':str(float(maximum))}

if __name__=='__main__':
    meter=c.Meter('Independent certificate replay/Fraction verification')
    try:
        records=[]
        for path in sorted(c.ROOT.glob('certificate_*.json')):
            meter.check();records.append({'file':path.name,**verify(json.loads(path.read_text()))})
        assert records
        (c.ROOT/'verification.json').write_text(json.dumps(records,indent=2));print(json.dumps([{k:r[k] for k in ('file','verified','size','binary_residual_bound')} for r in records],indent=2))
    finally:meter.finish()
