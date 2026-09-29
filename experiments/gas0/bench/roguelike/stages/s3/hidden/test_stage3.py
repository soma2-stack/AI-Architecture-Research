from rogue.effects import StatusBook,tick_poison
from rogue.model import Player,Point

def test_poison_is_nonlethal_even_when_damage_exceeds_health():
    player=Player("p","Hero",Point(0,0),2,10); book=StatusBook(); book.apply_poison("p",1,50)
    tick_poison(player,book)
    assert player.hp==1 and player.alive

def test_status_book_round_trip_preserves_duration():
    book=StatusBook(); book.apply_poison("p",3,2)
    restored=StatusBook.from_payload(book.payload())
    assert restored.get("p").remaining==3 and restored.get("p").damage==2

def test_poison_for_another_actor_does_not_tick_player():
    player=Player("p","Hero",Point(0,0),8,10); book=StatusBook(); book.apply_poison("e",2,2)
    assert tick_poison(player,book)==0 and player.hp==8
