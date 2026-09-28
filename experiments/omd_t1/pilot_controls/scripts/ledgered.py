"""Run a command and record its CPU time (children included) in the pilot and shared ledgers.

Usage: python3 scripts/ledgered.py STAGE "note" -- cmd args..."""
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from omdp import ledger  # noqa: E402


def main():
    stage, note = sys.argv[1], sys.argv[2]
    cmd = sys.argv[sys.argv.index("--") + 1:]
    ledger.check_cap()
    c0, w0 = ledger.cpu_seconds(), time.time()
    rc = subprocess.call(cmd)
    ledger.record(stage, ledger.cpu_seconds() - c0, time.time() - w0, f"{note} (rc={rc}): {' '.join(cmd)}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
