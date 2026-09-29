import pytest
from platformer.errors import LevelError
from platformer.geometry import Rect,overlap,intersection,union,distance
from platformer.level import (Level,parse_level,goal_position,start_position,collectable_positions,
                              neighbors,reachable,level_bounds,count_solid,walkable,nearest_marker,collect_marker)
from platformer.model import Vec2,Platform

def test_level_rectangular_shape_and_start_requirement():
    level=parse_level("#####\n#S.G#\n#####")
    assert (level.width,level.height)==(5,3)
    with pytest.raises(LevelError): Level(["###","##"])
    with pytest.raises(LevelError): Level(["...","..."])

def test_level_finds_start_goal_and_coins():
    level=parse_level("#####\n#S.P#\n#..G#\n#####")
    assert start_position(level)==Vec2(1,1)
    assert goal_position(level)==Vec2(3,2)
    assert collectable_positions(level)==(Vec2(3,1),)

def test_out_of_bounds_level_reads_are_solid():
    level=parse_level("S.")
    assert level.tile(-1,0)=="#" and level.tile(1,0)=="."

def test_level_rejects_unknown_glyphs():
    with pytest.raises(LevelError): parse_level("Sx")

def test_rect_dimensions_area_and_move():
    rect=Rect(1,2,5,7)
    assert rect.width==4 and rect.height==5 and rect.area==20
    assert rect.moved(Vec2(2,-1))==Rect(3,1,7,6)

def test_rectangle_contains_edges_in_starter_geometry():
    assert Rect(0,0,2,2).contains(Vec2(2,2))

def test_intersection_and_union():
    a=Rect(0,0,2,2); b=Rect(1,1,3,3)
    assert intersection(a,b)==Rect(1,1,2,2)
    assert union(a,b)==Rect(0,0,3,3)

def test_separated_rectangles_have_no_intersection():
    assert intersection(Rect(0,0,1,1),Rect(2,2,3,3)) is None

def test_platform_requires_positive_area_and_id():
    with pytest.raises(ValueError): Platform("",(0,0,1,1))
    with pytest.raises(ValueError): Platform("p",(0,0,0,1))

def test_vector_arithmetic_and_length():
    a=Vec2(3,4); b=Vec2(1,2)
    assert a+b==Vec2(4,6) and a-b==Vec2(2,2)
    assert a.length_squared()==25

def test_distance_is_euclidean():
    assert distance(Vec2(0,0),Vec2(3,4))==5

def test_rect_union_contains_both_inputs():
    a=Rect(0,0,1,1); b=Rect(2,2,3,3); u=union(a,b)
    assert u.contains(Vec2(0,0)) and u.contains(Vec2(3,3))

def test_platform_marker_occupies_positive_rectangle():
    platform=Platform("p",(1,2,4,3))
    assert platform.rect[2]-platform.rect[0]==3

def test_neighbor_order_and_reachability_are_deterministic():
    level=parse_level("S..\n.#.\n..G")
    assert neighbors(level,Vec2(1,1))==(Vec2(1,0),Vec2(0,1),Vec2(2,1),Vec2(1,2))
    assert reachable(level,Vec2(0,0),Vec2(2,2))

def test_level_boundaries_and_solid_count():
    level=parse_level("S#G")
    assert level_bounds(level)==(0,0,3,1) and count_solid(level)==1

def test_nearest_marker_uses_coordinate_tie_breaker():
    level=parse_level("G.S.G")
    assert nearest_marker(level,Vec2(2,0),"G")==Vec2(0,0)

def test_collect_marker_mutates_only_the_requested_tile():
    level=parse_level("S.P")
    assert collect_marker(level,Vec2(2,0),"P")
    assert level.text()=="S.." and not collect_marker(level,Vec2(2,0),"P")
