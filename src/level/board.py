from pygame import Rect

from .. import style


class Board:
    """Where a w x h grid of square cells sits on the screen.

    Converts cells to pixels for everything drawn on the maze (walls,
    pacgums, player, ghosts), so they all line up. Coordinates are
    screen coordinates.
    """

    def __init__(self, area: Rect, w: int, h: int) -> None:
        usable = area.inflate(-2 * style.MAZE_MARGIN, -2 * style.MAZE_MARGIN)
        cell = min(usable.width // w, usable.height // h)
        self.cell = max(style.MAZE_MIN_CELL_SIZE,
                        min(cell, style.MAZE_MAX_CELL_SIZE))
        self.rect = Rect(0, 0, self.cell * w, self.cell * h)
        self.rect.center = area.center

    def cell_rect(self, x: int, y: int) -> Rect:
        return Rect(self.rect.x + x * self.cell,
                    self.rect.y + y * self.cell,
                    self.cell, self.cell)

    def cell_center(self, x: float, y: float) -> tuple[int, int]:
        """Pixel center of a cell. Floats allow positions between
        two cells, for smooth movement."""
        return (round(self.rect.x + (x + 0.5) * self.cell),
                round(self.rect.y + (y + 0.5) * self.cell))
