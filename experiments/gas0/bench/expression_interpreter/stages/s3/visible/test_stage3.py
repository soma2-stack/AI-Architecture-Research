from expr import Environment, evaluate

def test_function_call_and_expression_body():
    assert evaluate("fn combine(a,b)=a*10+b; combine(2,3)") == 23

def test_parameters_use_local_scope():
    env=Environment(); evaluate("x=100",env)
    assert evaluate("fn local(x)=x+1; local(2)",env) == 3
    assert env.lookup("x") == 100

def test_functions_persist_in_environment():
    env=Environment(); evaluate("fn twice(x)=x*2",env)
    assert evaluate("twice(4)",env) == 8
