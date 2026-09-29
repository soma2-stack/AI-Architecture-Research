from rogue.effects import StatusBook,use_cleansing_charm
from rogue.model import Item,Player,Point

def test_cleansing_charm_removes_poison_heals_and_consumes():
    player=Player("p","Hero",Point(0,0),5,10,[Item("c","charm")]); book=StatusBook()
    book.apply_poison("p",3,2)
    assert use_cleansing_charm(player,book,"c")==6
    assert book.get("p") is None and player.inventory==[]
