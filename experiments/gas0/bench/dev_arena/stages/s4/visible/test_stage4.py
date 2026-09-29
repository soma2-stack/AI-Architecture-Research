# req: R4.1
from arena.mapgen import bordered_world
from arena.model import Point
from arena.path import shortest_path

def test_path_to_current_tile_contains_that_tile():
    w=bordered_world(7,7); current=Point(2,2)
    assert shortest_path(w,current,current)==[current]
