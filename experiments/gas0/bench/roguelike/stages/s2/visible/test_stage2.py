from rogue.inventory import use_tonic
from rogue.model import Item,Player,Point

def test_tonic_raises_cap_and_heals_two():
    player=Player("p","Hero",Point(0,0),5,10,[Item("t","tonic")])
    assert use_tonic(player,"t")== (12,7)
    assert player.inventory==[]
