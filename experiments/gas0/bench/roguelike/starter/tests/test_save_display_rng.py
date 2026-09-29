import json
import pytest
from rogue.display import render_grid,health_bar,status_line,inventory_lines,event_log,point_text,world_status
from rogue.errors import SaveError
from rogue.grid import Grid
from rogue.model import Enemy,Item,Player,Point
from rogue.rng import SeededRNG,loot_roll,choose_spawn,deterministic_order,clamped_chance
from rogue.save import save_world,load_world,save_text,load_text
from rogue.world import World
from rogue.progression import (ExperienceLedger,RewardEvent,award_defeat,campaign_score,
                               level_for_experience,progress_to_next,rank_score)

def sample():
    return World(Grid(["#####","#...#","#...#","#####"]),
        Player("p","Hero",Point(1,1),7,10,[Item("p1","potion",4)]),
        [Enemy("e","Rat",Point(3,2),2,2,damage=1,reward=2)])

def test_save_load_round_trip_world_fields(tmp_path):
    path=tmp_path/"save.json"; world=sample(); save_world(path,world)
    loaded=load_world(path)
    assert loaded.player.hp==7 and loaded.turn==0
    assert loaded.enemies[0].actor_id=="e" and loaded.player.inventory[0].item_id=="p1"

def test_save_text_has_stable_key_order():
    text=save_text(sample())
    assert text.startswith('{"enemies"') and json.loads(text)["version"]==1

def test_load_text_matches_file_loader():
    source=sample(); restored=load_text(save_text(source))
    assert restored.player.position==source.player.position

def test_unsupported_save_version_is_rejected(tmp_path):
    path=tmp_path/"x.json"; path.write_text('{"version":9}')
    with pytest.raises(SaveError): load_world(path)

def test_invalid_json_is_wrapped_as_save_error(tmp_path):
    path=tmp_path/"x.json"; path.write_text("{")
    with pytest.raises(SaveError): load_world(path)

def test_render_is_deterministic_and_actor_aware():
    world=sample(); output=render_grid(world.grid,world.player,world.enemies)
    assert output.splitlines()[1][1]=="@" and output.splitlines()[2][3]=="g"

def test_render_does_not_mutate_grid():
    world=sample(); before=world.grid.to_text()
    render_grid(world.grid,world.player,world.enemies)
    assert world.grid.to_text()==before

def test_health_bar_bounds_and_status_text():
    player=sample().player
    assert health_bar(player,5)=="[####-]"
    assert status_line(player,2)=="Hero HP 7/10 L1 T2"

def test_inventory_and_log_rendering():
    world=sample()
    assert inventory_lines(world.player.inventory)==("p1: potion 4",)
    assert event_log(["a","b","c"],2)==("b","c")

def test_point_and_world_status_format():
    world=sample()
    assert point_text(Point(2,3))=="2,3"
    assert world_status(world)=={"state":"active","turn":0,"enemies":1}

def test_seeded_rng_repeats_draws():
    a=SeededRNG(7); b=SeededRNG(7)
    assert [a.randint(0,99) for _ in range(5)]==[b.randint(0,99) for _ in range(5)]

def test_seeded_choice_rejects_empty_input():
    with pytest.raises(ValueError): SeededRNG(1).choice([])

def test_rng_shuffle_does_not_mutate_input():
    values=[1,2,3]; result=SeededRNG(3).shuffle(values)
    assert values==[1,2,3] and sorted(result)==values

def test_loot_roll_and_chance_bounds_are_repeatable():
    assert loot_roll(SeededRNG(5),1.0)
    assert clamped_chance(2)==1 and clamped_chance(-1)==0

def test_spawn_selection_uses_passed_rng():
    assert choose_spawn(SeededRNG(3),["a","b"])==choose_spawn(SeededRNG(3),["a","b"])

def test_reward_event_is_validated_and_idempotent():
    ledger=ExperienceLedger(); event=RewardEvent("e1","p",5,"chest")
    assert ledger.record(event) and not ledger.record(event)
    assert ledger.total("p")==5 and ledger.event_count()==1

def test_reward_payload_round_trip_is_value_based():
    original=ExperienceLedger([RewardEvent("e1","p",5,"chest")])
    restored=ExperienceLedger.from_payload(original.payload())
    assert restored.total("p")==5 and restored.sources("p")==("chest",)

def test_reward_ledger_copy_is_independent():
    original=ExperienceLedger([RewardEvent("e1","p",5,"chest")])
    copied=original.copy(); copied.record(RewardEvent("e2","p",2,"enemy"))
    assert original.total("p")==5 and copied.total("p")==7

def test_experience_thresholds_are_cumulative():
    assert level_for_experience(0)==1
    assert level_for_experience(10)==2
    assert level_for_experience(30)==3
    assert progress_to_next(25)=={"level":2,"into_level":15,"needed":5}

def test_enemy_reward_event_uses_stable_identity():
    player=Player("p","Hero",Point(0,0),1,10)
    enemy=Enemy("e","Rat",Point(1,0),0,3,reward=4)
    ledger=ExperienceLedger()
    assert award_defeat(ledger,enemy,player)
    assert not award_defeat(ledger,enemy,player) and ledger.total("p")==4

def test_campaign_score_and_rank_are_deterministic():
    score=campaign_score(10,3,5)
    assert score==343 and rank_score(score)=="B"
    assert rank_score(1000)=="S" and rank_score(0)=="C"
