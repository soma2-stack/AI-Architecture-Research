import os; os.environ["OMP_NUM_THREADS"]="2"
import json, sys
sys.argv=[sys.argv[0]]
exec(open("query_admissible_endpoint.py").read().split("out=[]")[0])
out=[]
for n,T in ((4000,64),(8000,16),(8000,64)):
    r=run(n,T); out.append(r); print(json.dumps(r), flush=True)
json.dump(out, open("query_admissible_endpoint_2.json","w"), indent=1)
