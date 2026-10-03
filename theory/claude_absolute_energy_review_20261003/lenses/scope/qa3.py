import os; os.environ["OMP_NUM_THREADS"]="2"
import json, sys
exec(open("query_admissible_endpoint.py").read().split("out=[]")[0])
cases=[(int(a),int(b)) for a,b in (s.split(":") for s in sys.argv[1:])]
for n,T in cases:
    r=run(n,T); print(json.dumps(r), flush=True)
