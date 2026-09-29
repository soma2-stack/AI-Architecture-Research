"""Input normalization independent of a graphics or event-loop library."""
from .model import Vec2,clamp
from .physics import jump_velocity

def horizontal_axis(left,right): return int(bool(right))-int(bool(left))
def set_horizontal(player,axis,speed):
    player.velocity=Vec2(clamp(axis,-1,1)*speed,player.velocity.y); return player.velocity
def jump(player,height):
    if not player.on_ground: return False
    player.velocity=Vec2(player.velocity.x,jump_velocity(height)); player.on_ground=False; return True
def neutral_input(player): player.velocity=Vec2(0,player.velocity.y)
def input_frame(left=False,right=False,jump_pressed=False):
    return {"axis":horizontal_axis(left,right),"jump":bool(jump_pressed)}
def apply_input(player,frame,speed,jump_height):
    set_horizontal(player,frame["axis"],speed)
    return jump(player,jump_height) if frame["jump"] else False

class InputBuffer:
    """Store the latest normalized input frame for deterministic replay."""
    def __init__(self): self.frames=[]
    def push(self,frame):
        normalized={"axis":max(-1,min(1,int(frame.get("axis",0)))),"jump":bool(frame.get("jump",False))}
        self.frames.append(normalized); return normalized
    def pop(self): return self.frames.pop(0) if self.frames else {"axis":0,"jump":False}
    def peek(self): return dict(self.frames[0]) if self.frames else {"axis":0,"jump":False}
    def clear(self): self.frames.clear()
    def payload(self): return [dict(row) for row in self.frames]

def deadzone(value,threshold=0.1):
    value=float(value)
    return 0.0 if abs(value)<threshold else max(-1.0,min(1.0,value))

def coyote_window(ticks_since_grounded,grace=4):
    return 0<=ticks_since_grounded<grace

def buffered_jump(buffer,player,height):
    frame=buffer.pop()
    return jump(player,height) if frame["jump"] else False
