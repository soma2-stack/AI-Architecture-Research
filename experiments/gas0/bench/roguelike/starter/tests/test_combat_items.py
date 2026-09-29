import pytest
from rogue.combat import attack,combat_log,damage_total,enemy_turn
from rogue.errors import InvalidAction
from rogue.inventory import Inventory,has_key,inventory_weight,use_potion
from rogue.model import Enemy,Item,Player,Point

def actors():
    return Player("p","Hero",Point(1,1),4,10),Enemy("e","Rat",Point(2,1),3,3,damage=2,reward=4)

def test_attack_reports_applied_damage_and_defeat():
    player,enemy=actors(); result=attack(player,enemy,3)
    assert result.applied==3 and result.defeated and not enemy.alive

def test_attack_rejects_dead_source_and_dead_target():
    player,enemy=actors(); player.hp=0
    with pytest.raises(InvalidAction): attack(player,enemy)
    player.hp=4; enemy.hp=0
    with pytest.raises(InvalidAction): attack(player,enemy)

def test_damage_is_clamped_to_health():
    player,enemy=actors(); result=attack(player,enemy,9)
    assert result.attempted==9 and result.applied==3 and enemy.hp==0

def test_combat_log_and_total_are_plain_values():
    player,enemy=actors(); result=attack(player,enemy,1)
    assert "hit" in combat_log(result) and damage_total([result])==1

def test_enemy_turn_uses_stable_actor_order():
    player=Player("p","Hero",Point(1,1),10,10)
    enemies=[Enemy("z","Z",Point(2,1),1,1,damage=3),Enemy("a","A",Point(1,2),1,1,damage=2)]
    assert enemy_turn(player,enemies)==5 and player.hp==5

def test_enemy_outside_melee_does_not_attack():
    player=Player("p","Hero",Point(1,1),10,10)
    enemy=Enemy("e","E",Point(4,4),1,1,damage=3)
    assert enemy_turn(player,[enemy])==0

def test_item_validation_and_inventory_order():
    inventory=Inventory([Item("p1","potion",3),Item("k1","key")])
    assert inventory.item_ids()==("p1","k1") and len(inventory)==2
    with pytest.raises(ValueError): inventory.add(Item("p1","weapon",2))

def test_inventory_find_remove_and_missing():
    inventory=Inventory([Item("k","key")])
    assert inventory.find("k").kind=="key"
    assert inventory.remove("k").item_id=="k"
    with pytest.raises(KeyError): inventory.remove("absent")

def test_potion_heals_only_missing_health_and_is_consumed():
    player=Player("p","Hero",Point(0,0),8,10,[Item("p","potion",5)])
    assert use_potion(player,"p")==2
    assert player.hp==10 and player.inventory==[]

def test_potion_wrong_kind_is_not_consumed():
    player=Player("p","Hero",Point(0,0),8,10,[Item("k","key")])
    with pytest.raises(InvalidAction): use_potion(player,"k")
    assert len(player.inventory)==1

def test_key_lookup_and_weight():
    items=[Item("k","key"),Item("w","weapon",6)]
    player=Player("p","Hero",Point(0,0),1,10,items)
    assert has_key(player) and has_key(player,"k") and not has_key(player,"missing")
    assert inventory_weight(items)==3

def test_experience_levels_up_repeatedly():
    player=Player("p","Hero",Point(0,0),5,10)
    assert player.add_experience(30)==3
    assert player.max_hp==14 and player.hp==9

def test_healing_and_damage_return_actual_delta():
    player=Player("p","Hero",Point(0,0),5,10)
    assert player.heal(20)==5 and player.take_damage(3)==3

def test_poison_tick_amount_is_nonnegative():
    from rogue.combat import poison_tick_amount
    assert poison_tick_amount(3)==3 and poison_tick_amount(-2)==0

def test_actor_ids_have_stable_order():
    from rogue.model import stable_actor_ids
    assert stable_actor_ids([actors()[1],actors()[0]])==("e","p")
