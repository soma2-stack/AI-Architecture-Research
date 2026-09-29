# req: R6.1
from arena import Arena
from arena.mapgen import bordered_world
from arena.model import Event, Point

def test_generated_events_monotone():
    g = Arena(1,bordered_world(7,7))
    g.add_player(); g.add_enemy('rat', Point(2,1), hp=1)
    g.player_move('hero',1,0)
    assert [e.seq for e in g.world.events] == list(range(1,len(g.world.events)+1))

def test_sequence_persists_after_event_clear():
    w=bordered_world(7,7)
    w.emit(Event('a','hero')); w.clear_events(); w.emit(Event('b','hero'))
    assert w.events[-1].seq == 2
