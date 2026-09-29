from platformer.model import Body,Vec2
from platformer.one_way import OneWayPlatform,blocks_from_below,can_land,land
from platformer.world import first_waypoint

def test_waypoint_selector_is_safe_for_empty_and_nonempty_routes():
    assert first_waypoint([]) is None
    assert first_waypoint([Vec2(1,2)])==Vec2(1,2)

def test_one_way_platform_allows_ascending_body_to_pass_through():
    body=Body("b",Vec2(1,2.2),Vec2(0,-3),1,1,False)
    platform=OneWayPlatform("p",(0,2,4,3))
    assert not can_land(body,platform,3.2) and not blocks_from_below(body,platform)

def test_one_way_requires_horizontal_overlap_and_downward_motion():
    platform=OneWayPlatform("p",(0,2,4,3))
    body=Body("b",Vec2(5,1),Vec2(0,2),1,1,False)
    assert not land(body,platform,1.5)
