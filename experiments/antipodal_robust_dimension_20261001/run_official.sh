#!/bin/bash
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python -c "import json;[print(c['id']) for c in sorted(json.load(open('candidates.json')),key=lambda c:-c['r'])]" > results/queue.txt
cat results/queue.txt | xargs -P 20 -I{} bash -c 'python certify_official.py {} >> results/official.log 2>> results/official_err.log'
echo OFFICIAL_DONE
