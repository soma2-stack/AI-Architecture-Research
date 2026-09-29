# req: R5.1
from arena.model import Actor, Point

def test_piercing_bypasses_shield():
    a = Actor('a', Point(1,1), 4, 4, 1, 'p', '@', shield=3)
    assert a.receive(2, 'piercing') == 2
    assert a.hp == 2 and a.shield == 3
