# req: R2.1
from arena.model import Actor, Point

def test_shield_absorbs_direct_hit():
    a = Actor('a', Point(1,1), 5, 5, 1, 'p', '@', shield=2)
    assert a.receive(2) == 0
    assert (a.hp, a.shield) == (5, 0)
