from __future__ import annotations
from typing import TYPE_CHECKING
from pygame import Event, Surface, Rect, draw

from .layer import Layer

if TYPE_CHECKING:
    from app import App


class Game(Layer):

    score: int
    # ghosts: list[Ghosts]
    # lvls: list[Levels]

    def __init__(self, screen_size: tuple[int, int]) -> None:

        # Game rules
        self.score = 0  # tracked accross levels
        self.ghosts = []
        self.lvls = []  # curr lvl is lvls[-1]

        # Rendering
        w, h = screen_size
        topbar = Rect(0, 0, w, 60)
        main_area = Rect(
            0,
            topbar.height,
            w,
            h - topbar.height
        )
        self.topbar = topbar
        self.main_area = main_area

        return

    def handle_event(self, e: Event, app: App) -> None:
        pass

    def update(self, dt: float, app: App) -> None:
        pass

    def render(self, screen: Surface) -> None:
        draw.rect(screen, (0, 0, 0), self.topbar)
        draw.rect(screen, (200, 0, 0), self.main_area)
