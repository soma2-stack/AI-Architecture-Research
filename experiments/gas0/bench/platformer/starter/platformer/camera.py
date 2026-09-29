"""Deterministic camera framing for ASCII snapshots and debug output."""
from .model import Vec2,clamp

class Camera:
    def __init__(self,width,height): self.width=int(width); self.height=int(height); self.position=Vec2(0,0)
    def follow(self,target,world_width,world_height):
        x=target.x-self.width/2; y=target.y-self.height/2
        self.position=Vec2(clamp(x,0,max(0,world_width-self.width)),clamp(y,0,max(0,world_height-self.height)))
        return self.position
    def world_to_screen(self,point): return Vec2(point.x-self.position.x,point.y-self.position.y)
    def visible(self,point):
        p=self.world_to_screen(point)
        return 0<=p.x<self.width and 0<=p.y<self.height

def centered_view(target,width,height): return Vec2(max(0,target.x-width/2),max(0,target.y-height/2))
def clamp_camera(camera,world_width,world_height):
    camera.position=Vec2(clamp(camera.position.x,0,max(0,world_width-camera.width)),clamp(camera.position.y,0,max(0,world_height-camera.height)))
    return camera.position
