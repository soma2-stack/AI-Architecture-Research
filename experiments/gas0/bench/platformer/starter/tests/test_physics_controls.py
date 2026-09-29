import pytest
from platformer.controls import (InputBuffer,apply_input,buffered_jump,coyote_window,deadzone,
                                 horizontal_axis,jump,set_horizontal)
from platformer.model import Body,Player,Vec2
from platformer.physics import (GRAVITY,MAX_FALL_SPEED,friction,grounded_velocity,
                                integrate,jump_velocity,step_body,step_velocity)

def player(grounded=True): return Player("p",Vec2(0,0),Vec2(0,0),1,1,grounded)

def test_axis_input_is_normalized_and_opposites_cancel():
    assert horizontal_axis(True,False)==-1
    assert horizontal_axis(False,True)==1
    assert horizontal_axis(True,True)==0

def test_horizontal_set_preserves_vertical_velocity():
    p=player(False); p.velocity=Vec2(1,4)
    assert set_horizontal(p,-1,3)==Vec2(-3,4)

def test_jump_only_works_when_grounded():
    p=player(); assert jump(p,2) and p.velocity.y<0
    q=player(False); assert not jump(q,2)

def test_jump_velocity_matches_height_formula():
    velocity=jump_velocity(2,GRAVITY)
    assert velocity<0 and abs(velocity**2-2*GRAVITY*2)<1e-9

def test_physics_step_updates_velocity_then_position():
    body=Body("b",Vec2(0,0),Vec2(2,0))
    step_body(body,0.5)
    assert body.velocity.y==9 and body.position==Vec2(1,4.5)

def test_grounded_body_does_not_accumulate_gravity():
    body=Body("b",Vec2(0,0),Vec2(1,0),on_ground=True)
    step_body(body,0.25)
    assert body.velocity.y==0

def test_fall_speed_is_bounded():
    body=Body("b",Vec2(0,0),Vec2(0,100))
    step_body(body,1)
    assert body.velocity.y==MAX_FALL_SPEED

def test_nonpositive_delta_is_rejected():
    with pytest.raises(ValueError): step_body(Body("b",Vec2(),Vec2()),0)

def test_free_integrator_and_acceleration_helpers():
    assert integrate(Vec2(1,1),Vec2(2,4),0.5)==Vec2(2,3)
    assert step_velocity(Vec2(1,1),Vec2(2,4),0.5)==Vec2(2,3)

def test_friction_only_changes_horizontal_component():
    assert friction(Vec2(10,3),0.2)==Vec2(8,3)
    assert grounded_velocity(Vec2(2,7))==Vec2(2,0)

def test_input_frame_applies_motion_and_ground_jump():
    p=player(); assert apply_input(p,{"axis":1,"jump":True},4,1)
    assert p.velocity.x==4 and p.velocity.y<0

def test_input_axis_is_clamped():
    p=player(); set_horizontal(p,5,2)
    assert p.velocity.x==2

def test_body_validation_and_translation():
    with pytest.raises(ValueError): Body("",Vec2(),Vec2())
    p=player(); p.translate(Vec2(2,3)); assert p.position==Vec2(2,3)

def test_player_score_and_lives_never_go_negative():
    p=player(); assert p.award(10)==10
    assert p.lose_life()==2

def test_input_buffer_normalizes_and_preserves_fifo_order():
    buffer=InputBuffer(); buffer.push({"axis":5,"jump":1}); buffer.push({"axis":-1})
    assert buffer.pop()=={"axis":1,"jump":True}
    assert buffer.pop()=={"axis":-1,"jump":False}

def test_input_buffer_empty_operations_are_safe():
    buffer=InputBuffer(); assert buffer.pop()=={"axis":0,"jump":False}
    assert buffer.peek()=={"axis":0,"jump":False}

def test_input_buffer_payload_is_a_copy():
    buffer=InputBuffer(); buffer.push({"axis":1})
    copy=buffer.payload(); copy[0]["axis"]=-1
    assert buffer.peek()["axis"]==1

def test_deadzone_and_coyote_window_boundaries():
    assert deadzone(0.05)==0 and deadzone(0.5)==0.5
    assert coyote_window(0) and coyote_window(3) and not coyote_window(4)

def test_buffered_jump_consumes_frame_and_uses_ground_state():
    buffer=InputBuffer(); buffer.push({"jump":True}); p=player()
    assert buffered_jump(buffer,p,1) and not buffer.frames
