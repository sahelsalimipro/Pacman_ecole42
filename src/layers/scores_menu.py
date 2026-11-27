# scores_menu.py
from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from pygame import Event, Surface, font

from .layer import Layer
from .buttons import Button
from ..scores import load_scores
from .. import colors as c

if TYPE_CHECKING:
    from app import App


def _back(app: App) -> None:
    # This layer was pushed on top of the start menu: pop it to go back
    app.layers.pop()


class ScoresMenu(Layer):
    BTN_SIZE = (260, 60)
    ROW_H = 36
    BG = c.MENU_BG

    def __init__(self, app: App, screen_size: tuple[int, int],
                 filename: str = "highscores.json") -> None:
        self.font = font.Font(None, 40)
        self.title_font = font.Font(None, 72)

        # Read once when the screen opens
        self.scores = load_scores(filename)

        w, h = screen_size
        self.cx = w // 2
        self.title_pos = (self.cx, 60)
        self.table_top = 120
        self.back_button = Button(
            "Back", self.BTN_SIZE, (self.cx, h - self.BTN_SIZE[1] - 30), _back)

        super().__init__(app)

    def handle_event(self, e: Event, app: App) -> None:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self.back_button.click(e.pos, app)
        elif e.type == pygame.KEYDOWN and e.key in (
                pygame.K_ESCAPE, pygame.K_BACKSPACE):
            _back(app)

    def update(self, dt: float, app: App) -> None:
        pass

    def render(self, screen: Surface) -> None:
        screen.fill(self.BG)

        title = self.title_font.render("High scores", True, c.TITLE)
        screen.blit(title, title.get_rect(center=self.title_pos))

        if not self.scores:
            text = self.font.render("No scores yet", True, c.TEXT_MUTED)
            screen.blit(text, text.get_rect(
                center=(self.cx, self.table_top + 60)))
        else:
            # Three columns: rank (right-aligned), name, score (right-aligned)
            rank_x, name_x, score_x = self.cx - 170, self.cx - 140, self.cx + 190
            for i, (name, score) in enumerate(self.scores):
                y = self.table_top + i * self.ROW_H
                color = c.SCORE_FIRST if i == 0 else c.SCORE_ROW
                rank = self.font.render(f"{i + 1}.", True, color)
                screen.blit(rank, rank.get_rect(topright=(rank_x, y)))
                screen.blit(self.font.render(name, True, color), (name_x, y))
                pts = self.font.render(str(score), True, color)
                screen.blit(pts, pts.get_rect(topright=(score_x, y)))

        self.back_button.render(screen, self.font, pygame.mouse.get_pos())
