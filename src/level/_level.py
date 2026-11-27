import random

from mazegenerator import MazeGenerator

from ..config import LevelConfig

Direction = tuple[int, int]

# Wall bits of a maze cell, as encoded by the maze package.
WALL_NORTH = 1
WALL_EAST = 2
WALL_SOUTH = 4
WALL_WEST = 8

# Wall bit for each direction of controls.py: (dx, dy), y grows downwards.
WALL_BIT: dict[Direction, int] = {
    (0, -1): WALL_NORTH,
    (1, 0): WALL_EAST,
    (0, 1): WALL_SOUTH,
    (-1, 0): WALL_WEST,
}

# All four walls: the cells of the '42' pattern. Nobody can enter them.
SOLID = WALL_NORTH | WALL_EAST | WALL_SOUTH | WALL_WEST

# Perfect maze = one single path between two cells, so dead ends.
# Pac-Man needs loops to escape ghosts.
PERFECT_MAZE = False


class Level:
    """One level: its settings and its maze.

    The grid is indexed ``grid[y][x]``. Each cell is an int whose bits
    are its walls (WALL_NORTH, ...). The maze package guarantees both
    sides of a wall agree, so a cell alone tells where one can go.
    """

    def __init__(self, cfg: LevelConfig) -> None:
        self.cfg = cfg
        self.name = cfg.name
        self.w = cfg.width
        self.h = cfg.height

        # The maze package calls random.seed() on Python's global
        # generator. Save and restore it, so a fixed maze seed does not
        # make the rest of the game (ghosts, bonuses) predictable.
        state = random.getstate()
        try:
            maze = MazeGenerator((self.w, self.h), PERFECT_MAZE,
                                 seed=cfg.seed)
        finally:
            random.setstate(state)
        self.grid: list[list[int]] = maze.maze

    def __str__(self) -> str:
        return self.name

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h

    def is_solid(self, x: int, y: int) -> bool:
        """True for the closed '42' cells."""
        return self.grid[y][x] == SOLID

    def has_wall(self, x: int, y: int, wall: int) -> bool:
        """``wall`` is one of WALL_NORTH, WALL_EAST, ..."""
        return bool(self.grid[y][x] & wall)

    def can_move(self, x: int, y: int, d: Direction) -> bool:
        """Can an entity in cell (x, y) step in direction ``d``?"""
        return not self.has_wall(x, y, WALL_BIT[d])

    def open_cells(self) -> list[tuple[int, int]]:
        """Every cell an entity can stand on (for pacgums, spawns...)."""
        return [(x, y) for y in range(self.h) for x in range(self.w)
                if not self.is_solid(x, y)]
