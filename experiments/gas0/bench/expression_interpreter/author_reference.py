"""Create the staged reference, probes and test packages for the interpreter."""
from __future__ import annotations

import difflib
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parent
STARTER=ROOT/"starter"
STAGES=ROOT/"stages"
REFERENCE=ROOT/"reference"

def snapshot():
    return {p.relative_to(STARTER).as_posix():p.read_text(encoding="utf-8")
            for p in STARTER.rglob("*.py") if "__pycache__" not in p.parts}

def patch_text(before,after):
    out=[]
    for name in sorted(set(before)|set(after)):
        old=before.get(name,"").splitlines(keepends=True)
        new=after.get(name,"").splitlines(keepends=True)
        if old!=new:
            out.extend(difflib.unified_diff(old,new,
                fromfile=f"a/{name}" if name in before else "/dev/null",
                tofile=f"b/{name}" if name in after else "/dev/null"))
    return "".join(out)

def put(stage,folder,name,body):
    path=STAGES/f"s{stage}"/folder/name
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(body.strip()+"\n",encoding="utf-8")

def replace(files,name,old,new):
    if files[name].count(old)!=1:
        raise AssertionError((name,old,files[name].count(old)))
    files[name]=files[name].replace(old,new)

def write_patch(stage,before,after):
    (REFERENCE/f"s{stage}.patch").write_bytes(patch_text(before,after).encode("utf-8"))

def main():
    for path in (STAGES,REFERENCE):
        if path.exists(): shutil.rmtree(path)
    REFERENCE.mkdir(parents=True)
    state=snapshot(); files=state.copy()
    (REFERENCE/"s1.patch").write_bytes(b"")
    put(1,"","request.md","""Do not edit. Inspect the interpreter and return JSON with exactly q1 through q8: q1 the scanner entry point; q2 the punctuation table; q3 the variable-assignment node; q4 the parser entry point; q5 the evaluator entry point; q6 the base user-facing error class; q7 the built-in function registry; q8 the line-oriented command entry point. Use exact names.""")

    # Stage 2: comparisons. Numeric equality is strict and results are 0.0/1.0.
    token="expr/token.py"
    replace(state,token,'    "=": "EQUAL", ",": "COMMA", ";": "SEMICOLON",\n',
        '    "=": "EQUAL", ",": "COMMA", ";": "SEMICOLON",\n'
        '    "==": "EQ", "!=": "NE", "<": "LT", "<=": "LE",\n'
        '    ">": "GT", ">=": "GE",\n')
    lexer="expr/lexer.py"
    replace(state,lexer,'        if char in PUNCTUATION:\n',
        '        pair = source[cursor:cursor + 2]\n'
        '        if pair in PUNCTUATION:\n'
        '            tokens.append(Token(PUNCTUATION[pair], pair, cursor))\n'
        '            cursor += 2\n'
        '            continue\n'
        '        if char in PUNCTUATION:\n')
    parser="expr/parser.py"
    replace(state,parser,'    def expression(self):\n        return self.additive()\n',
        '    def expression(self):\n'
        '        node = self.additive()\n'
        '        while self.current.kind in {"EQ", "NE", "LT", "LE", "GT", "GE"}:\n'
        '            operator = self.advance()\n'
        '            node = Binary(operator.kind, node, self.additive(), operator.position)\n'
        '        return node\n')
    runtime="expr/runtime.py"
    replace(state,runtime,'        elif node.operator == "PERCENT":\n'
        '            if right == 0:\n'
        '                raise EvalError("modulo by zero", node.position)\n'
        '            result = left % right\n',
        '        elif node.operator == "PERCENT":\n'
        '            if right == 0:\n'
        '                raise EvalError("modulo by zero", node.position)\n'
        '            result = left % right\n'
        '        elif node.operator in {"EQ", "NE", "LT", "LE", "GT", "GE"}:\n'
        '            if type(left) is not type(right):\n'
        '                raise EvalError("comparison operands must have the same type", node.position)\n'
        '            result = float({"EQ": left == right, "NE": left != right,\n'
        '                "LT": left < right, "LE": left <= right,\n'
        '                "GT": left > right, "GE": left >= right}[node.operator])\n')
    put(2,"","request.md","""Add numeric comparison operators ==, !=, <, <=, >, >= with conventional precedence below arithmetic. Equality is type-strict: reject unlike runtime scalar types rather than coercing them. Return numeric booleans 1 and 0. Preserve assignments, arithmetic, built-ins and stable source positions.""")
    put(2,"visible","test_stage2.py","""import pytest
from expr import evaluate
from expr.errors import EvalError

def test_comparison_precedence_and_numeric_boolean():
    assert evaluate("2 + 3 * 4 == 14") == 1.0
    assert evaluate("2 + 3 * 4 < 15") == 1.0
    assert evaluate("4 != 4") == 0.0

def test_chained_assignment_keeps_comparison_value():
    assert evaluate("ok = 3 >= 3; ok + 2") == 3.0

def test_unlike_scalar_types_are_rejected():
    from expr.nodes import Binary, Number
    from expr.runtime import Environment, evaluate_node
    with pytest.raises(EvalError, match="same type"):
        evaluate_node(Binary("EQ", Number(1, 0), Number(True, 0), 0), Environment())
""")
    put(2,"hidden","test_stage2.py","""import pytest
from expr import evaluate
from expr.errors import EvalError

def test_relational_operators_and_parenthesized_boolean():
    assert evaluate("(5 >= 5) * 10 + (3 < 1)") == 10
    assert evaluate("7 <= 7") == 1
    assert evaluate("9 > 10") == 0

def test_assignment_does_not_coerce_boolean_to_python_bool():
    from expr import Environment
    env=Environment(); evaluate("flag = 1 == 1",env)
    assert env.lookup("flag") == 1.0 and type(env.lookup("flag")) is float

def test_equality_is_not_truthiness():
    assert evaluate("2 == 1") == 0
""")
    put(2,"hidden","test_stage2_legacy.py","""from expr import evaluate

def test_legacy_integer_division_contract():
    assert evaluate("7/2") == 3
""")
    put(2,"","supersedes.json","[]")
    write_patch(2,files,state); files=state.copy()

    # Stage 3: expression-bodied functions with parameter-local scope.
    nodes="expr/nodes.py"
    state[nodes]+='''\n\n@dataclass(frozen=True)\nclass FunctionDef:\n    name: str\n    parameters: tuple[str, ...]\n    body: object\n    position: int\n'''
    replace(state,parser,'from .nodes import Assign, Binary, Call, Name, Number, Program, Unary',
        'from .nodes import Assign, Binary, Call, FunctionDef, Name, Number, Program, Unary')
    replace(state,parser,'            if self.current.kind == "NAME" and self.tokens[self.index + 1].kind == "EQUAL":\n',
        '            if self.current.kind == "NAME" and self.current.text == "fn":\n'
        '                start = self.advance()\n'
        '                name = self.expect("NAME")\n'
        '                self.expect("LPAREN")\n'
        '                parameters = []\n'
        '                if self.current.kind != "RPAREN":\n'
        '                    parameters.append(self.expect("NAME").text)\n'
        '                    while self.accept("COMMA"):\n'
        '                        parameters.append(self.expect("NAME").text)\n'
        '                self.expect("RPAREN")\n'
        '                self.expect("EQUAL")\n'
        '                statements.append(FunctionDef(name.text, tuple(parameters), self.expression(), start.position))\n'
        '            elif self.current.kind == "NAME" and self.tokens[self.index + 1].kind == "EQUAL":\n')
    replace(state,runtime,'from .nodes import Assign, Binary, Call, Name, Number, Program, Unary',
        'from .nodes import Assign, Binary, Call, FunctionDef, Name, Number, Program, Unary')
    replace(state,runtime,'    history: list[tuple[str, float]] = field(default_factory=list)\n',
        '    history: list[tuple[str, float]] = field(default_factory=list)\n'
        '    functions: dict[str, FunctionDef] = field(default_factory=dict)\n')
    replace(state,runtime,'        self.history.clear()\n','        self.history.clear()\n        self.functions.clear()\n')
    replace(state,runtime,'    if isinstance(node, Call):\n'
        '        args = [evaluate_node(arg, env) for arg in node.arguments]\n'
        '        return invoke(node.callee, args)\n',
        '    if isinstance(node, FunctionDef):\n'
        '        env.functions[node.name] = node\n'
        '        return None\n'
        '    if isinstance(node, Call):\n'
        '        args = [evaluate_node(arg, env) for arg in node.arguments]\n'
        '        function = env.functions.get(node.callee)\n'
        '        if function is not None:\n'
        '            local = Environment()\n'
        '            for index, name in enumerate(function.parameters):\n'
        '                local.assign(name, args[index])\n'
        '            return evaluate_node(function.body, local)\n'
        '        return invoke(node.callee, args)\n')
    put(3,"","request.md","""Add expression-bodied user functions using `fn name(arg1,arg2)=expression`. Parameters are evaluated left-to-right and bound in a fresh local scope; caller variables must not be overwritten. Defer short-circuit `and` / `or` until a later stage. Keep built-ins and top-level assignments working.""")
    put(3,"visible","test_stage3.py","""from expr import Environment, evaluate

def test_function_call_and_expression_body():
    assert evaluate("fn combine(a,b)=a*10+b; combine(2,3)") == 23

def test_parameters_use_local_scope():
    env=Environment(); evaluate("x=100",env)
    assert evaluate("fn local(x)=x+1; local(2)",env) == 3
    assert env.lookup("x") == 100

def test_functions_persist_in_environment():
    env=Environment(); evaluate("fn twice(x)=x*2",env)
    assert evaluate("twice(4)",env) == 8
""")
    put(3,"hidden","test_stage3.py","""from expr import Environment, evaluate

def test_multiple_functions_and_argument_order():
    env=Environment()
    assert evaluate("fn add(a,b)=a+b; fn twice(x)=x*2; twice(add(3,4))",env)==14

def test_function_body_does_not_read_caller_local_values():
    env=Environment(); evaluate("hidden=40",env)
    assert evaluate("fn isolated(x)=x+1; isolated(2)",env)==3

def test_builtin_calls_still_resolve_inside_function():
    assert evaluate("fn score(x)=max(x,5); score(2)")==5
""")
    put(3,"hidden","test_stage3_deferred.py","""from expr import evaluate

def test_boolean_operators_remain_deferred():
    assert evaluate("0") == 0
""")
    put(3,"","supersedes.json","[]")
    write_patch(3,files,state); files=state.copy()

    # Stage 4 injects an arity-check defect in ceil only, preserving prior built-ins.
    bfile="expr/builtins.py"
    old='''def _ceil(values):
    if len(values) != 1:
        raise EvalError("ceil needs one argument")
    return float(math.ceil(values[0]))
'''
    injected=old.replace('if len(values) != 1:', 'if len(values) == 1:')
    before_bug=state.copy()
    replace(state,bfile,old,injected)
    (STAGES/"s4").mkdir(parents=True,exist_ok=True)
    (STAGES/"s4"/"bug.patch").write_bytes(patch_text(before_bug,state).replace("\r\n","\n").encode("utf-8"))
    # The bug state is the starting point for stage intake; reference s4 repairs it.
    bugged=state.copy(); state=bugged
    put(4,"","request.md","""A valid call to `ceil` now raises an arity error. Diagnose the regression and repair it without changing built-in function signatures or the behavior of other functions.""")
    put(4,"visible","test_stage4.py","""from expr import evaluate

def test_ceil_accepts_one_argument():
    assert evaluate("ceil(3.2)") == 4
""")
    put(4,"hidden","test_stage4.py","""from expr import evaluate

def test_ceil_arity_fix_preserves_other_unary_builtins():
    assert evaluate("floor(3.8)") == 3
    assert evaluate("ceil(3.2)") == 4
    assert evaluate("abs(-5.5)") == 5.5
""")
    put(4,"","supersedes.json","[]")
    fixed=state.copy(); replace(fixed,bfile,injected,old)
    write_patch(4,state,fixed); state=fixed; files=state.copy()

    # Stage 5: true division and floor division replace legacy truncation.
    replace(state,runtime,'            result = float(int(left / right))\n','            result = left / right\n')
    replace(state,token,'    "==": "EQ", "!=": "NE", "<": "LT", "<=": "LE",\n',
        '    "==": "EQ", "!=": "NE", "<": "LT", "<=": "LE",\n'
        '    "//": "FLOOR_SLASH",\n')
    replace(state,parser,'        while self.current.kind in {"STAR", "SLASH", "PERCENT"}:\n',
        '        while self.current.kind in {"STAR", "SLASH", "PERCENT", "FLOOR_SLASH"}:\n')
    replace(state,runtime,'        elif node.operator == "PERCENT":\n',
        '        elif node.operator == "FLOOR_SLASH":\n'
        '            if right == 0:\n'
        '                raise EvalError("division by zero", node.position)\n'
        '            result = left // right\n'
        '        elif node.operator == "PERCENT":\n')
    put(5,"","request.md","""Replace legacy truncating `/` with true division and add `//` for floor division. Preserve explicit zero-division diagnostics, comparisons, user functions, assignments and output formatting.""")
    put(5,"visible","test_stage5.py","""import pytest
from expr import evaluate
from expr.errors import EvalError

def test_true_and_floor_division_are_distinct():
    assert evaluate("7/2") == 3.5
    assert evaluate("7//2") == 3

def test_negative_floor_rounds_down():
    assert evaluate("-7//2") == -4

def test_zero_divisor_is_a_language_error():
    with pytest.raises(EvalError,match="division by zero"):
        evaluate("1//0")
""")
    put(5,"hidden","test_stage5.py","""from expr import evaluate

def test_division_inside_function_uses_true_division():
    assert evaluate("fn half(x)=x/2; half(7)") == 3.5

def test_floor_precedence_and_comparison():
    assert evaluate("1+7//2==4") == 1

def test_float_operands_floor_correctly():
    assert evaluate("8.9//2") == 4
""")
    put(5,"","supersedes.json",json.dumps(["tests/hidden_2/test_stage2_legacy.py"],indent=2))
    write_patch(5,files,state); files=state.copy()

    # Stage 6: validate the AST against an explicit language whitelist.
    state["expr/inspect.py"]+='''\n\ndef validate_program(program):\n    """Reject every node outside the interpreter's explicit syntax tree."""\n    from .errors import EvalError\n    from .nodes import Assign, Binary, Call, FunctionDef, Name, Number, Program, Unary\n    allowed=(Assign,Binary,Call,FunctionDef,Name,Number,Program,Unary)\n    def visit(node):\n        if not isinstance(node,allowed):\n            raise EvalError("unsupported syntax tree node")\n        if isinstance(node,Program):\n            children=node.statements\n        elif isinstance(node,Assign):\n            children=(node.value,)\n        elif isinstance(node,Binary):\n            children=(node.left,node.right)\n        elif isinstance(node,Unary):\n            children=(node.operand,)\n        elif isinstance(node,Call):\n            children=node.arguments\n        elif isinstance(node,FunctionDef):\n            children=(node.body,)\n        else:\n            children=()\n        for child in children: visit(child)\n    visit(program)\n    return True\n'''
    replace(state,runtime,'from .parser import parse\n','from .parser import parse\nfrom .inspect import validate_program\n')
    replace(state,runtime,'    program = parse(source)\n','    program = parse(source)\n    validate_program(program)\n')
    put(6,"","request.md","""Persistent global constraint G6.1: user source is evaluated only as the interpreter's whitelisted AST; never delegate source execution to Python `eval` or `exec`. Validate every parsed program before evaluation and preserve the constraint for function bodies and later grammar additions.""")
    put(6,"","static_checks.py","""import ast
from pathlib import Path

def test_interpreter_never_calls_host_eval_or_exec():
    root=Path(__file__).resolve().parents[1]/"expr"
    for path in root.glob("*.py"):
        tree=ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            assert not (isinstance(node,ast.Call) and isinstance(node.func,ast.Name)
                        and node.func.id in {"eval","exec"}),path.name
""")
    put(6,"visible","test_stage6.py","""import pytest
from expr.errors import EvalError
from expr.inspect import validate_program
from expr.nodes import Program

def test_unknown_ast_nodes_are_rejected():
    with pytest.raises(EvalError,match="unsupported"):
        validate_program(Program((object(),)))
""")
    put(6,"hidden","test_stage6.py","""import pytest
from expr import evaluate
from expr.errors import EvalError
from expr.inspect import validate_program
from expr.nodes import Binary, Number, Program

def test_recursive_whitelist_covers_children():
    bad=Program((Binary("PLUS",Number(1,0),object(),0),))
    with pytest.raises(EvalError,match="unsupported"):
        validate_program(bad)

def test_every_parsed_program_passes_guard_without_changing_result():
    assert evaluate("fn inc(x)=x+1; inc(2)") == 3
""")
    put(6,"","supersedes.json","[]")
    write_patch(6,files,state); files=state.copy()

    # Stage 7: strict call arity and deferred short-circuit boolean operators.
    replace(state,lexer,'            tokens.append(Token("NAME", source[start:cursor], start))\n',
        '            text = source[start:cursor]\n'
        '            kind = {"and": "AND", "or": "OR"}.get(text, "NAME")\n'
        '            tokens.append(Token(kind, text, start))\n')
    replace(state,parser,'    def expression(self):\n'
        '        node = self.additive()\n'
        '        while self.current.kind in {"EQ", "NE", "LT", "LE", "GT", "GE"}:\n'
        '            operator = self.advance()\n'
        '            node = Binary(operator.kind, node, self.additive(), operator.position)\n'
        '        return node\n',
        '    def expression(self):\n'
        '        node = self.logical_and()\n'
        '        while self.accept("OR"):\n'
        '            node = Binary("OR", node, self.logical_and(), self.tokens[self.index - 1].position)\n'
        '        return node\n\n'
        '    def logical_and(self):\n'
        '        node = self.comparison()\n'
        '        while self.accept("AND"):\n'
        '            node = Binary("AND", node, self.comparison(), self.tokens[self.index - 1].position)\n'
        '        return node\n\n'
        '    def comparison(self):\n'
        '        node = self.additive()\n'
        '        while self.current.kind in {"EQ", "NE", "LT", "LE", "GT", "GE"}:\n'
        '            operator = self.advance()\n'
        '            node = Binary(operator.kind, node, self.additive(), operator.position)\n'
        '        return node\n')
    replace(state,runtime,'    if isinstance(node, Binary):\n'
        '        left = evaluate_node(node.left, env)\n'
        '        right = evaluate_node(node.right, env)\n',
        '    if isinstance(node, Binary):\n'
        '        left = evaluate_node(node.left, env)\n'
        '        if node.operator == "AND" and left == 0:\n'
        '            return 0.0\n'
        '        if node.operator == "OR" and left != 0:\n'
        '            return 1.0\n'
        '        right = evaluate_node(node.right, env)\n'
        '        if node.operator in {"AND", "OR"}:\n'
        '            return float(right != 0)\n')
    replace(state,runtime,'        if function is not None:\n'
        '            local = Environment()\n',
        '        if function is not None:\n'
        '            if len(args) != len(function.parameters):\n'
        '                raise EvalError("wrong number of function arguments", node.position)\n'
        '            local = Environment()\n')
    put(7,"","scenario.py","""from expr import evaluate
from expr.errors import EvalError

try:
    evaluate("fn only(x)=x; only()")
except EvalError:
    pass
assert evaluate("0 and missing(1)") == 0
assert evaluate("1 or missing(2)") == 1
""")
    put(7,"","request.md","""The supplied run crashes when a user function receives the wrong number of arguments. Use the trace and scenario to fix the runtime failure. Also implement the short-circuit boolean operators deferred in Stage 3; their behavior is described in the saved design note. Keep evaluation deterministic.""")
    put(7,"visible","test_stage7.py","""import pytest
from expr import evaluate
from expr.errors import EvalError

def test_wrong_user_function_arity_is_language_error():
    with pytest.raises(EvalError,match="wrong number"):
        evaluate("fn one(x)=x; one()")

def test_short_circuit_skips_undefined_calls():
    assert evaluate("0 and missing(1)") == 0
    assert evaluate("1 or missing(2)") == 1
""")
    put(7,"hidden","test_stage7.py","""from expr import Environment, evaluate
from expr.errors import EvalError
import pytest

def test_and_or_evaluate_right_side_only_when_needed():
    assert evaluate("0 and unknown") == 0
    assert evaluate("1 or unknown") == 1
    assert evaluate("1 and 5") == 1
    assert evaluate("0 or 8") == 1

def test_evaluated_right_side_normalizes_to_boolean():
    assert evaluate("1 and 4")==1
    assert evaluate("0 or 8")==1

def test_extra_and_missing_arguments_both_rejected():
    for source in ("fn id(x)=x; id()","fn id(x)=x; id(1,2)"):
        with pytest.raises(EvalError,match="wrong number"):
            evaluate(source)
""")
    put(7,"hidden","test_stage3_deferred_stage7.py","""from expr import evaluate

def test_deferred_boolean_operators_now_short_circuit():
    assert evaluate("0 and unknown(1)")==0
    assert evaluate("1 or unknown(1)")==1
""")
    put(7,"","supersedes.json",json.dumps(["tests/hidden_3/test_stage3_deferred.py"],indent=2))
    write_patch(7,files,state); files=state.copy()

    # Stage 8: JSON-formatted CLI diagnostics.
    cli="expr/cli.py"
    replace(state,cli,'def run_lines(lines, session: Session | None = None):\n',
        'def run_lines(lines, session: Session | None = None, json_errors: bool = False):\n')
    replace(state,cli,'        except ExpressionError as error:\n'
        '            yield diagnostic(line.rstrip("\\n"), error)\n',
        '        except ExpressionError as error:\n'
        '            if json_errors:\n'
        '                yield json.dumps({"error": error.message, "position": error.position}, sort_keys=True)\n'
        '            else:\n'
        '                yield diagnostic(line.rstrip("\\n"), error)\n')
    replace(state,cli,'import argparse\n','import argparse\nimport json\n')
    replace(state,cli,'    parser.add_argument("--show-vars", action="store_true")\n',
        '    parser.add_argument("--show-vars", action="store_true")\n'
        '    parser.add_argument("--json-errors", action="store_true")\n')
    replace(state,cli,'            for output in run_lines(handle, session):\n','            for output in run_lines(handle, session, args.json_errors):\n')
    replace(state,cli,'        for output in run_lines(sys.stdin, session):\n','        for output in run_lines(sys.stdin, session, args.json_errors):\n')
    put(8,"","request.md","""Add `--json-errors` to the command-line program. In this mode each language error is one deterministic JSON object containing `error` and `position`; successful outputs remain unchanged. Preserve text diagnostics as the default and integrate the flag with batch and stdin operation.""")
    put(8,"visible","test_stage8.py","""import json
from expr.cli import run_lines

def test_json_error_mode_and_success_output():
    rows=list(run_lines(["1/0","2+3"],json_errors=True))
    assert json.loads(rows[0])["error"] == "division by zero"
    assert rows[1] == "5"
""")
    put(8,"hidden","test_stage8.py","""import json
from expr.cli import main

def test_cli_flag_formats_each_error_line(tmp_path,capsys,monkeypatch):
    path=tmp_path/"program.expr"; path.write_text("1/0\\n4+1\\n")
    assert main(["--file",str(path),"--json-errors"])==0
    output=capsys.readouterr().out.splitlines()
    assert json.loads(output[0])["position"]==1
    assert output[1]=="5"
""")
    put(8,"","supersedes.json","[]")
    write_patch(8,files,state)

    manifest={"project":"expression_interpreter","kind":"evaluation","stages":8,
      "orientation_answers":{"q1":"expr.lexer.tokenize","q2":"expr.token.PUNCTUATION","q3":"expr.nodes.Assign","q4":"expr.parser.parse","q5":"expr.runtime.evaluate","q6":"expr.errors.ExpressionError","q7":"expr.builtins.FUNCTIONS","q8":"expr.cli.run_lines"},
      "probes":[
       {"introduced":1,"retired":2,"tests":[f"Q{i}" for i in range(1,9)],"text_only":False,"requirement":"R1.1"},
       {"introduced":2,"retired":None,"tests":["tests/hidden_2/test_stage2.py::test_relational_operators_and_parenthesized_boolean","tests/hidden_2/test_stage2.py::test_assignment_does_not_coerce_boolean_to_python_bool","tests/hidden_2/test_stage2.py::test_equality_is_not_truthiness"],"text_only":False,"requirement":"R2.1"},
       {"introduced":2,"retired":5,"tests":["tests/hidden_2/test_stage2_legacy.py::test_legacy_integer_division_contract"],"text_only":True,"requirement":"R2.2"},
       {"introduced":3,"retired":None,"tests":["tests/hidden_3/test_stage3.py::test_multiple_functions_and_argument_order","tests/hidden_3/test_stage3.py::test_function_body_does_not_read_caller_local_values","tests/hidden_3/test_stage3.py::test_builtin_calls_still_resolve_inside_function"],"text_only":False,"requirement":"R3.1"},
       {"introduced":3,"retired":7,"tests":["tests/hidden_3/test_stage3_deferred.py::test_boolean_operators_remain_deferred"],"text_only":True,"requirement":"R3.2"},
       {"introduced":4,"retired":None,"tests":["tests/hidden_4/test_stage4.py::test_ceil_arity_fix_preserves_other_unary_builtins"],"text_only":False,"requirement":"R4.1"},
       {"introduced":5,"retired":None,"tests":["tests/hidden_5/test_stage5.py::test_division_inside_function_uses_true_division","tests/hidden_5/test_stage5.py::test_floor_precedence_and_comparison","tests/hidden_5/test_stage5.py::test_float_operands_floor_correctly"],"text_only":False,"requirement":"R5.1"},
       {"introduced":6,"retired":None,"tests":["tests/hidden_6/test_stage6.py::test_recursive_whitelist_covers_children","tests/hidden_6/test_stage6.py::test_every_parsed_program_passes_guard_without_changing_result"],"text_only":False,"requirement":"G6.1"},
       {"introduced":7,"retired":None,"tests":["tests/hidden_7/test_stage7.py::test_and_or_evaluate_right_side_only_when_needed","tests/hidden_7/test_stage7.py::test_evaluated_right_side_normalizes_to_boolean","tests/hidden_7/test_stage7.py::test_extra_and_missing_arguments_both_rejected","tests/hidden_7/test_stage3_deferred_stage7.py::test_deferred_boolean_operators_now_short_circuit"],"text_only":False,"requirement":"R3.2"},
       {"introduced":8,"retired":None,"tests":["tests/hidden_8/test_stage8.py::test_cli_flag_formats_each_error_line"],"text_only":False,"requirement":"R8.1"}]}
    (ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main()
