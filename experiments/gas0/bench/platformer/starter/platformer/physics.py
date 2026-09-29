"""Simple semi-implicit Euler integration for a small fixed-step game."""
from .model import Vec2,clamp

GRAVITY=18.0
MAX_FALL_SPEED=24.0

def step_velocity(velocity,acceleration,dt):
    return Vec2(velocity.x+acceleration.x*dt,velocity.y+acceleration.y*dt)

def integrate(position,velocity,dt):
    return Vec2(position.x+velocity.x*dt,position.y+velocity.y*dt)

def step_body(body,dt,gravity=GRAVITY):
    if dt<=0: raise ValueError("dt must be positive")
    acceleration=Vec2(0,0 if body.on_ground else gravity)
    body.velocity=step_velocity(body.velocity,acceleration,dt)
    body.velocity=Vec2(body.velocity.x,clamp(body.velocity.y,-MAX_FALL_SPEED,MAX_FALL_SPEED))
    body.position=integrate(body.position,body.velocity,dt)
    return body.position

def jump_velocity(height,gravity=GRAVITY):
    if height<0 or gravity<=0: raise ValueError("invalid jump parameters")
    return -(2*gravity*height)**0.5

def horizontal_input(axis,speed): return Vec2(clamp(float(axis),-1,1)*speed,0)
def grounded_velocity(velocity): return Vec2(velocity.x,0)
def friction(velocity,amount): return Vec2(velocity.x*max(0,1-amount),velocity.y)
