from rogue.effects import StatusBook,use_cleansing_charm
from rogue.model import Item,Player,Point
from rogue.world import World
from rogue.grid import Grid

def test_empty_world_summary_is_safe_after_final_defeat():
    world=World(Grid(["..." ]),Player("p","Hero",Point(0,0),1,1),[])
    assert world.last_enemy_name() is None

def test_charm_preserves_unrelated_statuses_and_cannot_be_reused():
    player=Player("p","Hero",Point(0,0),1,10,[Item("c","charm")]); book=StatusBook()
    book.apply_poison("other",2,1); book.apply_poison("p",1,1)
    use_cleansing_charm(player,book,"c")
    assert book.get("other").remaining==2 and book.get("p") is None
