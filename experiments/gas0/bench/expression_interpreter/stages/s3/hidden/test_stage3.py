from expr import Environment, evaluate

def test_multiple_functions_and_argument_order():
    env=Environment()
    assert evaluate("fn add(a,b)=a+b; fn twice(x)=x*2; twice(add(3,4))",env)==14

def test_function_body_does_not_read_caller_local_values():
    env=Environment(); evaluate("hidden=40",env)
    assert evaluate("fn isolated(x)=x+1; isolated(2)",env)==3

def test_builtin_calls_still_resolve_inside_function():
    assert evaluate("fn score(x)=max(x,5); score(2)")==5
