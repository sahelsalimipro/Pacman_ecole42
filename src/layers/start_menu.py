# start_menu.py
from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from pygame import Event, Surface, Rect, font

from .layer import Layer
from .buttons import Button

if TYPE_CHECKING:
    from app import App


def _fake_func() -> None:
    return


class StartMenu(Layer):
    BTN_SIZE = (260, 60)
    BTN_GAP = 20
    INPUT_SIZE = (260, 50)
    MAX_NAME_LEN = 16
    BG = (30, 30, 40)

    def __init__(self, app: App, screen_size: tuple[int, int]) -> None:
        self.font = font.Font(None, 40)
        self.title_font = font.Font(None, 72)

        self.name = ""
        self.input_active = True
        self.cursor_timer = 0.0

        # Layout
        w, h = screen_size
        cx = w // 2
        self.title_pos = (cx, h // 2 - 190)

        self.input_rect = Rect((0, 0), self.INPUT_SIZE)
        self.input_rect.center = (cx, h // 2 - 100)

        specs = [
            ("Play", _fake_func, self._has_name),
            ("View scores", _fake_func, lambda: True),
            ("Quit", _fake_func, lambda: True),
        ]
        y = self.input_rect.bottom + 40
        self.buttons: list[Button] = []
        for label, action, enabled in specs:
            self.buttons.append(
                Button(label, self.BTN_SIZE, (cx, y), action, enabled))
            y += self.BTN_SIZE[1] + self.BTN_GAP

        self.play_button = self.buttons[0]
        return super().__init__(app)

    def _has_name(self) -> bool:
        return bool(self.name.strip())

    def handle_event(self, e: Event, app: App) -> None:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self.input_active = self.input_rect.collidepoint(e.pos)
            for b in self.buttons:
                if b.rect.collidepoint(e.pos):
                    self._press(b, app)
                    break

        elif e.type == pygame.KEYDOWN and self.input_active:
            if e.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._press(self.play_button, app)
            elif e.unicode and e.unicode.isprintable() and len(self.name) < self.MAX_NAME_LEN:
                self.name += e.unicode

    def _press(self, button: Button, app: App) -> None:
        if button.enabled():
            if button is self.play_button:
                app.player_name = self.name    # store before the action runs
            button.action(app)

    def update(self, dt: float, app: App) -> None:
        self.cursor_timer = (self.cursor_timer + dt) % 1.0
        return

    def render(self, screen: Surface) -> None:
        screen.fill(self.BG)

        title = self.title_font.render("My Game", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=self.title_pos))

        border = (140, 140, 220) if self.input_active else (90, 90, 120)
        pygame.draw.rect(screen, (20, 20, 28),
                         self.input_rect, border_radius=8)
        pygame.draw.rect(screen, border, self.input_rect,
                         width=2, border_radius=8)

        if self.name or self.input_active:
            shown = self.name + \
                ("|" if self.input_active and self.cursor_timer < 0.5 else "")
            text = self.font.render(shown, True, (255, 255, 255))
        else:
            text = self.font.render("Enter your name", True, (110, 110, 130))
        screen.blit(text, text.get_rect(
            midleft=(self.input_rect.x + 12, self.input_rect.centery)))

        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.render(screen, self.font, mouse)
