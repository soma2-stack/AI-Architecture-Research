from platformer.collision import carry_body
from platformer.model import Body,Vec2

def test_vertical_and_horizontal_carrier_motion_apply_once():
    body=Body("b",Vec2(5,5),Vec2())
    delta=carry_body(body,Vec2(1,2),Vec2(4,6))
    assert delta==Vec2(3,4) and body.position==Vec2(8,9)
