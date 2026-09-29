from rogue.effects import StatusBook,use_cleansing_charm
from rogue.model import Item,Player,Point

def test_deferred_cleansing_charm_removes_poison_and_consumes_item():
    player=Player("p","Hero",Point(0,0),4,10,[Item("c","charm")]); book=StatusBook()
    book.apply_poison("p",2,2); use_cleansing_charm(player,book,"c")
    assert book.get("p") is None and player.hp==5 and player.inventory==[]
