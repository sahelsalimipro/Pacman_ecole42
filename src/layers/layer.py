from abc import ABC, abstractmethod
from pygame import Event

class Layer(ABC):


    @abstractmethod
    def handle_event(self, e: Event) -> None:
        ...
