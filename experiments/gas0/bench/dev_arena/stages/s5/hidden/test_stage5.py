# req: R5.1
from arena.combat import strike
from arena.mapgen import bordered_world
from arena.model import Actor, Point
from arena.rng import Dice

def test_piercing_event_and_dependents():
    w = bordered_world(7,7)
    a = Actor('a', Point(1,1), 5, 5, 2, 'p', '@')
    b = Actor('b', Point(2,1), 5, 5, 1, 'e', 'e', shield=5)
    w.add_actor(a); w.add_actor(b)
    assert strike(w,a,b,Dice(1), 'piercing') > 0
    assert b.shield == 5 and w.events[-1].detail == 'piercing'
