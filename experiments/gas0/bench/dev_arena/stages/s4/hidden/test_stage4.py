# req: R4.1
from arena.mapgen import bordered_world
from arena.model import Point
from arena.path import shortest_path

def test_same_position_path_is_nonempty_and_deterministic():
    w=bordered_world(7,7); current=Point(3,4)
    assert shortest_path(w,current,current)==[current]
