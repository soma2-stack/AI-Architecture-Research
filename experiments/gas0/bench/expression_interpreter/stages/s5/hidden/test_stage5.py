from expr import evaluate

def test_division_inside_function_uses_true_division():
    assert evaluate("fn half(x)=x/2; half(7)") == 3.5

def test_floor_precedence_and_comparison():
    assert evaluate("1+7//2==4") == 1

def test_float_operands_floor_correctly():
    assert evaluate("8.9//2") == 4
