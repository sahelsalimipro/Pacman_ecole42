from __future__ import annotations
from typing import TYPE_CHECKING
from pygame import Event, Surface
import pygame

from .layer import Layer

if TYPE_CHECKING:
    from app import App


class StartMenu(Layer):

    def __init__(self) -> None:
        pass

    def handle_event(self, e: Event, app: App) -> None:
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
            self.app.replace(Game(self.app))

    def update(self, dt: float, app: App) -> None:
        pass

    def render(self, screen: Surface) -> None:
        pass
