import json
from collections import defaultdict
from common import ROOT

rows=[json.loads(x) for x in (ROOT/'runs/t1_official.jsonl').read_text().splitlines()]
selected=[r for r in rows if r['type']=='selected']; groups=defaultdict(dict)
for r in selected: groups[(r['model'],r['control'],r['seed'])][r['schedule']]=r
gaps=[]
for (model,control,seed), arms in groups.items():
    if 'joint' in arms and 'cumulative' in arms:
        j,c=arms['joint'],arms['cumulative']
        gaps.append({'model':model,'control':control,'seed':seed,'gap_pp':100*(j['accuracy']-c['accuracy']),
                     'joint_accuracy':j['accuracy'],'cumulative_accuracy':c['accuracy'],
                     'union_accuracy':c['union_accuracy'],'union_bce':c['union_bce']})
summary={'target':1,'verdict':'KILLED — KNOWN METHODS CLOSE THE ATTRIBUTE-LEVEL FAILURE',
         'reproduced_robust_history_gap':False,'official_seeds':sorted({r['seed'] for r in selected}),
         'strongest_single_seed_gap_pp':max(r['gap_pp'] for r in gaps),
         'paired_gaps':gaps,'training_runs':sum(r['type']=='trial' for r in rows),
         'rule_control_accuracies':[r['accuracy'] for r in rows if r['type']=='rule_control'],
         'rationale':'MLP and DeepSets base cumulative are perfect on all five seeds; label-only rule induction also achieves 100%. One Transformer seed has a large gap, but known methods remove it.',
         'scope':'Attribute-level fixture only; not a full reproduction or closure of pixel ConCon.'}
(ROOT/'t1_result.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k!='paired_gaps'},indent=2))
