from platformer.fixed import Fixed

def test_fixed_operations_keep_integer_raw_state():
    a=Fixed.from_number(1.25); b=Fixed.from_number(0.5)
    result=a+b
    assert type(result.raw) is int and result.to_number()==1.75
