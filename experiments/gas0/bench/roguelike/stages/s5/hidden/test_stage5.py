from rogue.damage import DamagePacket,DamageType,ResistanceProfile,resolve_damage,weakness_bonus
from rogue.model import Enemy,Point

def test_resistance_cannot_absorb_more_than_attempted_damage():
    enemy=Enemy("e","Rat",Point(0,0),5,5)
    outcome=resolve_damage(enemy,DamagePacket(2,DamageType.FIRE,"p"),ResistanceProfile(fire=10))
    assert outcome.resisted==2 and outcome.applied==0 and enemy.hp==5

def test_weakness_bonus_is_typed_and_immutable():
    packet=DamagePacket(2,DamageType.FIRE,"p")
    assert weakness_bonus(packet,DamageType.FIRE).amount==3
    assert weakness_bonus(packet,DamageType.POISON) is packet and packet.amount==2
