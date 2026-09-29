"""Small deterministic room and corridor map constructors."""
from .grid import FLOOR,WALL,Grid
from .model import Point

def bordered_room(width,height):
    if width<3 or height<3: raise ValueError("room must have an interior")
    return Grid([WALL*width if y in {0,height-1} else WALL+FLOOR*(width-2)+WALL
                 for y in range(height)])

def room_with_exit(width,height):
    rows=[list(row) for row in bordered_room(width,height).rows]
    rows[height-2][width-2]=">"
    return Grid(["".join(row) for row in rows])

def room_center(grid): return Point(grid.width//2,grid.height//2)
def corners(grid): return (Point(1,1),Point(grid.width-2,1),Point(1,grid.height-2),Point(grid.width-2,grid.height-2))

def connect_rooms(left,right):
    """Return a predictable Manhattan corridor between room centers."""
    points=[left]
    x,y=left.x,left.y
    while x!=right.x: x+=1 if right.x>x else -1; points.append(Point(x,y))
    while y!=right.y: y+=1 if right.y>y else -1; points.append(Point(x,y))
    return tuple(points)

def open_floor_count(grid): return sum(grid.tile(point)!=WALL for point in grid.points())
