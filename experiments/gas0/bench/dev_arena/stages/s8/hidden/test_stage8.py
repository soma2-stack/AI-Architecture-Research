# req: R8.1
import json
from arena import Arena
from arena.mapgen import bordered_world
from arena.save import dumps, loads

def test_old_save_defaults_to_zero_shield():
    g=Arena(1,bordered_world(7,7)); g.add_player().shield=4
    data=json.loads(dumps(g.world,g.bags))
    assert data['actors'][0]['shield']==4
    for actor in data['actors']:
        actor.pop('shield',None)
    world,_=loads(json.dumps(data))
    assert world.actors['hero'].shield==0

def test_shield_and_antidote_items_integrate():
    g=Arena(1,bordered_world(7,7)); a=g.add_player(); a.shield=3
    from arena.model import Item
    g.bags['hero'].add(Item('ant','antidote'))
    world,bags=loads(dumps(g.world,g.bags))
    assert world.actors['hero'].shield==3
    assert bags['hero'].find('antidote').item_id=='ant'
