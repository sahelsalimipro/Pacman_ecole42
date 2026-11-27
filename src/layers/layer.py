from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abc import ABC, abstractmethod
    from pygame import Event, Surface
    from app import App


class Layer(ABC):
    def __init__(self, app: "App") -> None:
        self.app = app
    ...

    @abstractmethod
    def handle_event(self, e: Event, app: App) -> None:
        ...

    @abstractmethod
    def update(self, dt: float, app: App) -> None:
        ...

    @abstractmethod
    def render(self, screen: Surface) -> None:
        ...
