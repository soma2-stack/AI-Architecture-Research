from platformer.model import Body,Vec2
from platformer.one_way import OneWayPlatform,land
from platformer.world import first_waypoint

def test_empty_route_has_no_next_waypoint():
    assert first_waypoint([]) is None

def test_one_way_platform_catches_from_above():
    body=Body("b",Vec2(1,1.5),Vec2(0,2),1,1,False)
    assert land(body,OneWayPlatform("p",(0,2,4,3)),1.5)
    assert body.on_ground and body.velocity.y==0
