from platformer.fixed import Fixed
from platformer.model import Player,Vec2
from platformer.world import World,tick_many

def test_world_updates_quantize_to_same_fixed_state_each_run():
    def simulate():
        world=World(Player("p",Vec2(),Vec2(1,0)),[])
        tick_many(world,60,1/60)
        return (world.player.position,world.player.velocity,world.fixed_updates)
    assert simulate()==simulate() and simulate()[2]==60

def test_fixed_division_by_zero_is_explicit():
    import pytest
    with pytest.raises(ZeroDivisionError): Fixed.from_number(1)/Fixed(0)
