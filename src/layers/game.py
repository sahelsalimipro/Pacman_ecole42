from __future__ import annotations
from typing import TYPE_CHECKING
from pygame import Event, Surface, Rect, draw, font

from .layer import Layer
from .. import colors as c
from .. import style
from ..level import (Level, Board,
                     WALL_NORTH, WALL_EAST, WALL_SOUTH, WALL_WEST)

if TYPE_CHECKING:
    from app import App


class Game(Layer):

    score: int
    # ghosts: list[Ghosts]
    lvl_index: int      # index in app.config.levels, 0 = first level
    level: Level
    board: Board
    maze_img: Surface   # walls drawn once per level, blitted every frame

    def __init__(self, app: App, screen_size: tuple[int, int]) -> None:
        super().__init__(app)

        # Rendering areas
        w, h = screen_size
        self.topbar = Rect(0, 0, w, style.TOPBAR_HEIGHT)
        self.main_area = Rect(0, self.topbar.bottom,
                              w, h - self.topbar.height)
        self.hud_font = font.Font(None, style.HUD_FONT_SIZE)

        # Game rules
        self.score = 0  # tracked across levels
        self.ghosts = []
        self._start_level(0)

    def handle_event(self, e: Event, app: App) -> None:
        pass

    def update(self, dt: float, app: App) -> None:
        pass

    def render(self, screen: Surface) -> None:
        draw.rect(screen, c.GAME_TOPBAR, self.topbar)
        self._render_hud(screen)
        screen.blit(self.maze_img, self.main_area)
        # later: pacgums, player, ghosts (positions from self.board)

    # --- Levels ---------------------------------------------------------

    def _start_level(self, index: int) -> None:
        """Build level ``index``: maze, its place on screen, its image."""
        self.lvl_index = index
        self.level = Level(self.app.config.levels[index])
        self.board = Board(self.main_area, self.level.w, self.level.h)
        self.maze_img = self._draw_maze()

    def _nxt_level(self) -> None:
        if self.lvl_index + 1 < len(self.app.config.levels):
            self._start_level(self.lvl_index + 1)
        else:
            self._win()

    def _win(self) -> None:
        pass  # TODO

    # --- Drawing ----------------------------------------------------------

    def _render_hud(self, screen: Surface) -> None:
        text = style.HUD_LEVEL_FORMAT.format(
            num=self.lvl_index + 1,
            total=len(self.app.config.levels),
            name=self.level.name,
        )
        img = self.hud_font.render(text, True, c.HUD_TEXT)
        screen.blit(img, img.get_rect(
            midleft=(self.topbar.x + style.HUD_PADDING_X,
                     self.topbar.centery)))

    def _wall_thickness(self) -> int:
        t = round(self.board.cell * style.WALL_THICKNESS_RATIO)
        return max(style.WALL_MIN_THICKNESS,
                   min(t, style.WALL_MAX_THICKNESS))

    def _draw_maze(self) -> Surface:
        """Draw the whole maze on an image the size of the main area.

        Walls never change during a level, so this runs once per level
        instead of once per frame.
        """
        img = Surface(self.main_area.size)
        img.fill(c.GAME_BG)

        # Board rects are in screen coordinates, the image starts at
        # the main area's top-left corner: shift everything by that.
        dx, dy = -self.main_area.x, -self.main_area.y
        draw.rect(img, c.MAZE_BG, self.board.rect.move(dx, dy))

        t = self._wall_thickness()
        half = t // 2
        for y in range(self.level.h):
            for x in range(self.level.w):
                r = self.board.cell_rect(x, y).move(dx, dy)

                if self.level.is_solid(x, y):
                    inset = style.SOLID_BLOCK_INSET + half
                    draw.rect(img, c.MAZE_BLOCK, r.inflate(-2 * inset,
                                                           -2 * inset),
                              border_radius=style.SOLID_BLOCK_BORDER_RADIUS)

                # Each wall is a thin rect centred on the cell edge,
                # overlapping by half a thickness at both ends so the
                # corners join without gaps.
                walls = (
                    (WALL_NORTH, Rect(r.left - half, r.top - half,
                                      r.width + t, t)),
                    (WALL_SOUTH, Rect(r.left - half, r.bottom - half,
                                      r.width + t, t)),
                    (WALL_WEST, Rect(r.left - half, r.top - half,
                                     t, r.height + t)),
                    (WALL_EAST, Rect(r.right - half, r.top - half,
                                     t, r.height + t)),
                )
                for bit, wall in walls:
                    if self.level.has_wall(x, y, bit):
                        draw.rect(img, c.WALL, wall,
                                  border_radius=style.WALL_BORDER_RADIUS)
        return img
