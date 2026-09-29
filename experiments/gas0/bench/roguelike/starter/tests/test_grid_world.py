import pytest
from rogue.grid import Grid,parse_map
from rogue.errors import InvalidMap,InvalidAction
from rogue.model import Enemy,Player,Point
from rogue.world import World,advance_turn,move_player,remove_defeated
from rogue.mapgen import bordered_room,room_with_exit,room_center,corners,connect_rooms

def make_world():
    grid=parse_map("#####\n#...#\n#...#\n#####")
    player=Player("p","Hero",Point(1,1),8,10)
    enemy=Enemy("e","Rat",Point(3,2),3,3,damage=2)
    return World(grid,player,[enemy])

def test_grid_dimensions_and_bounds():
    grid=Grid(["####","#..#","####"])
    assert (grid.width,grid.height)==(4,3)
    assert grid.contains(Point(1,1)) and not grid.contains(Point(4,1))

def test_ragged_or_empty_map_rejected():
    with pytest.raises(InvalidMap): Grid([])
    with pytest.raises(InvalidMap): Grid(["###","##"])

def test_grid_walkability_and_neighbors_are_ordered():
    grid=Grid(["###","#.#","###"])
    assert grid.walkable(Point(1,1))
    assert grid.neighbors(Point(1,1))==()

def test_map_rejects_unknown_glyph():
    with pytest.raises(InvalidMap): Grid(["#x#"])

def test_distance_map_and_reachability():
    grid=Grid(["#####","#...#","###.#","#...#","#####"])
    distances=grid.distance_map(Point(1,1))
    assert distances[Point(3,3)]==4
    assert grid.reachable(Point(1,1),Point(3,3))

def test_nearest_target_ties_are_coordinate_stable():
    grid=Grid(["....."])
    assert grid.nearest_reachable(Point(2,0),[Point(3,0),Point(1,0)])==Point(1,0)

def test_bordered_room_has_wall_boundary():
    grid=bordered_room(7,5)
    assert grid.rows[0]=="#######" and grid.rows[-1]=="#######"

def test_room_exit_and_center():
    grid=room_with_exit(7,5)
    assert grid.tile(Point(5,3))==">"
    assert room_center(grid)==Point(3,2)

def test_map_markers_and_floor_count():
    grid=room_with_exit(7,5)
    assert grid.markers(">")== (Point(5,3),)
    assert grid.nearest_reachable(Point(1,1),grid.markers(">"))==Point(5,3)

def test_corner_and_corridor_helpers():
    grid=bordered_room(7,5)
    assert corners(grid)[0]==Point(1,1)
    assert connect_rooms(Point(1,1),Point(3,2))==(Point(1,1),Point(2,1),Point(3,1),Point(3,2))

def test_move_rejects_wall_and_accepts_floor():
    world=make_world()
    assert not move_player(world,-1,0)
    assert move_player(world,1,0)
    assert world.player.position==Point(2,1)

def test_enemy_blocks_player_movement():
    world=make_world()
    assert not move_player(world,2,1)

def test_turn_advances_and_enemies_attack_adjacent_player():
    world=make_world(); result=advance_turn(world)
    assert result["turn"]==1 and world.player.hp==8

def test_dead_player_cannot_take_turn():
    world=make_world(); world.player.hp=0
    with pytest.raises(InvalidAction): advance_turn(world)

def test_remove_defeated_enemies_only():
    world=make_world(); world.enemies.append(Enemy("x","Gone",Point(1,2),0,3))
    assert remove_defeated(world)==1
    assert [e.actor_id for e in world.enemies]==["e"]
