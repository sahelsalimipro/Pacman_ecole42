from pygame import Event, Surface

from .layer import Layer

class EndMenu(Layer):

    def handle_event(self, e: Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def render(self, screen: Surface) -> None:
        pass
