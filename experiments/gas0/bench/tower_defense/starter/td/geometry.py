"""Grid and range helpers for the compact single-lane game."""

from math import hypot


BOARD_WIDTH = 20
BOARD_HEIGHT = 8


def distance(ax, ay, bx, by):
    """Euclidean distance between grid-cell centers."""
    return hypot(float(ax) - float(bx), float(ay) - float(by))


def in_range(ax, ay, bx, by, radius):
    """Range includes a target exactly on the radius boundary."""
    return distance(ax, ay, bx, by) <= max(0.0, float(radius))


def clamp(value, low, high):
    """Clamp a scalar into a closed interval."""
    return max(low, min(high, value))


def manhattan(ax, ay, bx, by):
    """Return taxicab distance for grid-oriented diagnostics."""
    return abs(int(ax) - int(bx)) + abs(int(ay) - int(by))


def inside_board(x, y, width=BOARD_WIDTH, height=BOARD_HEIGHT):
    """Test board membership without rounding floating coordinates."""
    return 0 <= int(x) < int(width) and 0 <= int(y) < int(height)


def validate_position(x, y):
    """Return a normalized integer cell or reject the position."""
    if not inside_board(x, y):
        raise ValueError("position outside board")
    return int(x), int(y)


def grid_distance(first, second):
    """Distance between two (x,y) cells."""
    return manhattan(first[0], first[1], second[0], second[1])


def cells_in_row(y, width=BOARD_WIDTH):
    """List lane cells from left to right."""
    return tuple((x, int(y)) for x in range(max(0, int(width))))


def is_lane_cell(x, y):
    """The path is the horizontal row zero."""
    return int(y) == 0 and 0 <= int(x) <= BOARD_WIDTH
