from rogue.effects import StatusBook,tick_poison
from rogue.model import Player,Point

def test_poison_ticks_and_expires():
    player=Player("p","Hero",Point(0,0),8,10); book=StatusBook()
    book.apply_poison("p",2,2)
    assert tick_poison(player,book)>0
    assert tick_poison(player,book)>0 and book.get("p") is None
