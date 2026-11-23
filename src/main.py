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

        while self._run():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break




        pygame.quit()

    def _run(self) -> bool:
        pygame.display.flip()
        return True
