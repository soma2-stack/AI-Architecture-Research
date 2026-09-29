from rogue.combat import attack
from rogue.damage import DamageType,ResistanceProfile
from rogue.model import Enemy,Player,Point

def test_default_attack_is_typed_physical():
    p=Player("p","Hero",Point(0,0),5,5); e=Enemy("e","Rat",Point(1,0),5,5)
    result=attack(p,e,2)
    assert result.damage_type=="physical" and e.hp==3

def test_matching_resistance_reduces_only_that_damage_type():
    p=Player("p","Hero",Point(0,0),5,5); e=Enemy("e","Rat",Point(1,0),5,5)
    result=attack(p,e,4,DamageType.FIRE,ResistanceProfile(fire=3))
    assert result.applied==1 and result.damage_type=="fire"
