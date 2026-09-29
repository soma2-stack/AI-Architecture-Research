from platformer.collision import carry_body
from platformer.model import Body,Vec2

def test_platform_carry_matches_one_frame_delta():
    body=Body("b",Vec2(3,1),Vec2())
    carry_body(body,Vec2(1,0),Vec2(2,0))
    assert body.position==Vec2(4,1)
