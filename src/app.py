import pygame

from layers import Layer, StartMenu

FPS: float = 60

class App:

    def __init__(self) -> None:
        self.layers: list[Layer] = [StartMenu()]
        self.clock = pygame.Clock()
        return


    def launch(self) -> None:
        pygame.init()

        window = pygame.display.set_mode()
        dt = self.clock.tick(FPS)

        self._run(window, dt)

        pygame.quit()

    def _run(self, window: pygame.Surface, dt: float) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif self.layers:
                    self.layers[-1].handle_event(event)
            pygame.display.flip()
