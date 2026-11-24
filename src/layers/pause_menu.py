from __future__ import annotations
from typing import TYPE_CHECKING
from pygame import Event, Surface

from .layer import Layer

if TYPE_CHECKING:
    from app import App


class PauseMenu(Layer):
    def handle_event(self, e: Event, app: App) -> None:
        pass

    def update(self, dt: float, app: App) -> None:
        pass

    def render(self, screen: Surface) -> None:
        pass
