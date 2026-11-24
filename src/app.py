import pygame

from .layers import Layer, StartMenu

FPS: float = 60

class App:

    def __init__(self, screen_size: tuple[int, int]) -> None:
        self.layers: list[Layer] = [StartMenu()]
        self.clock = pygame.Clock()
        self.screen_size = screen_size
        return


    def launch(self) -> None:
        pygame.init()

        window = pygame.display.set_mode()

        self._run(window)

        pygame.quit()

    def _run(self, window: pygame.Surface) -> None:
        dt = self.clock.tick(FPS)
        while True:
            dt = self.clock.tick(FPS)
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif self.layers:
                    self.layers[-1].handle_event(event)
            # Updates
            for lay in self.layers:
                lay.update(dt)

            # Render
            for lay in sef.layers:
                lay.render(window)

            pygame.display.flip()
