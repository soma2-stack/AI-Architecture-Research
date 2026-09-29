from rogue.inventory import use_tonic
from rogue.model import Item,Player,Point

def test_tonic_at_full_health_keeps_new_capacity_available():
    player=Player("p","Hero",Point(0,0),10,10,[Item("t","tonic")])
    use_tonic(player,"t")
    assert player.max_hp==12 and player.hp==12

def test_tonic_consumption_cannot_be_repeated():
    import pytest
    player=Player("p","Hero",Point(0,0),5,10,[Item("t","tonic")])
    use_tonic(player,"t")
    with pytest.raises(KeyError): use_tonic(player,"t")
