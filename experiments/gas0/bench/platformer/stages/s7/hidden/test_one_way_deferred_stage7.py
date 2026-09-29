from platformer.model import Body,Vec2
from platformer.one_way import OneWayPlatform,land

def test_deferred_one_way_platform_catches_from_above_but_not_below():
    p=OneWayPlatform("p",(0,2,4,3))
    above=Body("a",Vec2(1,1),Vec2(0,2),1,1,False)
    below=Body("b",Vec2(1,2.2),Vec2(0,-2),1,1,False)
    assert land(above,p,1.8)
    assert not land(below,p,3.2)
