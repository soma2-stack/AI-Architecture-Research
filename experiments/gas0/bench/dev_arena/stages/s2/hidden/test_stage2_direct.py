# req: R2.1
from arena.model import Actor, Point

def test_shield_direct_damage():
    a = Actor('a', Point(1,1), 5, 5, 1, 'p', '@', shield=1)
    assert a.receive(3, 'piercing') == 2
    assert (a.hp, a.shield) == (3, 0)
