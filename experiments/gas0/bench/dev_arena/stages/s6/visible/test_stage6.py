# req: R6.1
from arena.mapgen import bordered_world
from arena.model import Event

def test_event_sequence():
    w = bordered_world(7,7)
    w.emit(Event('a','hero')); w.emit(Event('b','hero'))
    assert [e.seq for e in w.events] == [1,2]
