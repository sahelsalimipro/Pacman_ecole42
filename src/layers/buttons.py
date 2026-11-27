# buttons.py
from __future__ import annotations
from typing import Callable, TYPE_CHECKING
import pygame
from pygame import Rect, Surface
from pygame.font import Font

from .. import colors as c

if TYPE_CHECKING:
    from app import App


class Button:
    def __init__(
        self,
        label: str,
        size: tuple[int, int],
        midtop: tuple[int, int],
        action: Callable[[App], None],
        enabled: Callable[[], bool] = lambda: True,
    ) -> None:
        self.label = label
        self.rect = Rect((0, 0), size)
        self.rect.midtop = midtop      # anchor by center-x, so no manual x calculation
        self.action = action
        self.enabled = enabled         # e.g. Play disabled while the name is empty

    def click(self, pos: tuple[int, int], app: App) -> None:
        if self.enabled() and self.rect.collidepoint(pos):
            self.action(app)

    def render(self, screen: Surface, font: Font, mouse: tuple[int, int]) -> None:
        if not self.enabled():
            color, fg = c.BUTTON_DISABLED, c.BUTTON_DISABLED_TEXT
        else:
            color = c.BUTTON_HOVER if self.rect.collidepoint(mouse) else c.BUTTON
            fg = c.BUTTON_TEXT
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text = font.render(self.label, True, fg)
        screen.blit(text, text.get_rect(center=self.rect.center))
