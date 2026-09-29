from rogue.combat import attack
from rogue.model import Enemy,Player,Point

def test_flat_attack_has_no_damage_type_field_yet():
    p=Player("p","Hero",Point(0,0),5,5); e=Enemy("e","Rat",Point(1,0),3,3)
    assert not hasattr(attack(p,e,1),"damage_type")
