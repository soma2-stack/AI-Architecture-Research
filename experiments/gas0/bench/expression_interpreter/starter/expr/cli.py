"""Line-oriented deterministic command interface."""
from __future__ import annotations

import argparse
import sys

from .errors import ExpressionError
from .format import diagnostic
from .session import Session


def run_lines(lines, session: Session | None = None):
    session = session or Session()
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            yield session.execute(line.rstrip("\n"))
        except ExpressionError as error:
            yield diagnostic(line.rstrip("\n"), error)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate numeric expressions")
    parser.add_argument("--file", help="read expressions from file")
    parser.add_argument("--show-vars", action="store_true")
    args = parser.parse_args(argv)
    session = Session()
    if args.file:
        with open(args.file, encoding="utf-8") as handle:
            for output in run_lines(handle, session):
                print(output)
    else:
        for output in run_lines(sys.stdin, session):
            print(output)
    if args.show_vars:
        for name, value in session.variables():
            print(f"{name}={value:g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
