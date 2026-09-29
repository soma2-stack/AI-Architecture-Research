from expr import evaluate
from expr.errors import EvalError

try:
    evaluate("fn only(x)=x; only()")
except EvalError:
    pass
assert evaluate("0 and missing(1)") == 0
assert evaluate("1 or missing(2)") == 1
