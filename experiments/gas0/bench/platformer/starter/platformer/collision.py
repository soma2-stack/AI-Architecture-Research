"""Solid-platform resolution and stable platform carry calculations."""
from .geometry import Rect,overlap
from .model import Vec2

def platform_delta(previous,current):
    """Return one frame of carrier motion from two platform positions."""
    return current-previous

def carry_body(body,previous,current):
    delta=platform_delta(previous,current)
    body.position=body.position+delta
    return delta

def landing(body,platform,previous_bottom):
    left,top,right,bottom=body.bounds(); pl,pt,pr,pb=platform.rect
    crosses=previous_bottom<=pt and bottom>=pt
    horizontal=right>pl and left<pr
    return crosses and horizontal and body.velocity.y>=0

def resolve_landing(body,platform,previous_bottom):
    if not landing(body,platform,previous_bottom): return False
    body.position=Vec2(body.position.x,platform.rect[1]-body.height)
    body.velocity=Vec2(body.velocity.x,0); body.on_ground=True
    return True

def colliding_platforms(body,platforms):
    box=Rect(*body.bounds())
    return [p for p in sorted(platforms,key=lambda x:x.platform_id) if overlap(box,Rect(*p.rect))]

def separate_x(body,platform):
    left,top,right,bottom=body.bounds(); pl,pt,pr,pb=platform.rect
    if right>pl and left<pr and bottom>pt and top<pb:
        body.position=Vec2(pl-body.width if body.velocity.x>0 else pr,body.position.y)
        body.velocity=Vec2(0,body.velocity.y); return True
    return False

def platform_center(platform):
    left,top,right,bottom=platform.rect; return Vec2((left+right)/2,(top+bottom)/2)
