from pygame import Event

from .layer import Layer


class Game(Layer):

    def handle_event(self, e: Event) -> None:
        pass

    def update(dt: float) -> None:
        pass
