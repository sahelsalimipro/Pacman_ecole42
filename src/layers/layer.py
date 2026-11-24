from abc import ABC, abstractmethod
from pygame import Event, Surface

class Layer(ABC):


    @abstractmethod
    def handle_event(self, e: Event) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def render(self, screen: Surface) -> None:
        ...
