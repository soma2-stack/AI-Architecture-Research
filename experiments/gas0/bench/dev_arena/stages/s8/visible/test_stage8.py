# req: R8.1
from arena import Arena
from arena.mapgen import bordered_world
from arena.save import dumps, loads

def test_save_shield_roundtrip():
    g=Arena(1,bordered_world(7,7)); a=g.add_player(); a.shield=4
    world,_=loads(dumps(g.world,g.bags))
    assert world.actors['hero'].shield==4
