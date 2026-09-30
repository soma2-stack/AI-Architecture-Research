"""Post-run optional artifact comparison; original raw results are never rewritten."""
import os
for _key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ[_key]='1'
import argparse
import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path
import numpy as np
import core as c
import analyze
import run

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--corrected',action='store_true');args=parser.parse_args()
    base=c.ROOT
    if args.corrected:c.ROOT=base/'corrected_single_thread'
    meter=c.Meter('B2 optional Stage-B archive provenance correction')
    try:
        old=Path(__file__).resolve().parent.parent/'exact_online_credit_stage_b_20260930';records=[]
        with zipfile.ZipFile(old/'matrices.zip') as prior:
            by_name={entry.split('/')[-1]:entry for entry in prior.namelist()}
            for z in analyze.load('raw.jsonl'):
                m=run.make(z['case'],z['n'],z['seed'])
                axis='positive' if m.linear_shared else 'mix' if m.mode=='feedback' else m.family
                key=f"n{m.n}_{axis}{m.interaction}_d{m.depth}_{m.mode}_T{z['T']}_s{z['seed']}.npz"
                if key not in by_name:
                    records.append({'id':z['id'],'available':False,'reason':'New n16 configuration absent from B'});continue
                blob=prior.read(by_name[key])
                with np.load(io.BytesIO(blob)) as a,np.load(c.ROOT/'matrices'/f"{z['id']}.npz") as b:
                    for field in ('S','theta','x','q','y'):assert np.array_equal(a[field],b[field]),(z['id'],field)
                records.append({'id':z['id'],'available':True,'archive_path':by_name[key],
                                'npz_sha256':hashlib.sha256(blob).hexdigest(),'all_arrays_identical':True})
        result={'matches':sum(r['available'] for r in records),'cases':len(records),'records':records,
                'correction':'Optional initial lookup used bare NPZ name; B archive uses matrices/ prefix. Raw metrics/lookup flags preserved unchanged. Corrected post-run metadata audit only.'}
        (c.ROOT/'prior_artifact_comparison.json').write_text(json.dumps(result,indent=2))
        print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
    finally:meter.finish()

if __name__=='__main__':main()
