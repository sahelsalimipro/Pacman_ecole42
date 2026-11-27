import pygame

# from .layers import Layer, StartMenu
from .config import load_config, GameConfig
from .layers import Layer, Game

FPS: float = 60


class App:

    config: GameConfig
    _player_name: str
    layers: list[Layer]
    clock: pygame.Clock

    def __init__(self, config_file: str, screen_size: tuple[int, int]) -> None:

        self.config = load_config(config_file)
        pygame.init()

        self._player_name = ""
        # self.layers: list[Layer] = [StartMenu(self, screen_size)]
        self.layers: list[Layer] = [Game(self, screen_size)]
        self.clock = pygame.Clock()
        self.screen_size = screen_size
        return

    @property
    def player_name(self) -> str:
        return self._player_name

    @player_name.setter
    def player_name(self, new: str) -> str:
        try:
            new = new.strip()
            if not new.isalnum():
                raise ValueError("Invalid characters in player name")
            self._player_name = new
        except ValueError, AttributeError:
            ...
        return self._player_name

    def launch(self) -> None:
        window = pygame.display.set_mode(self.screen_size)

        self._run(window)

        pygame.quit()

    def _run(self, window: pygame.Surface) -> None:
        while True:
            dt = self.clock.tick(FPS)
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif self.layers:
                    self.layers[-1].handle_event(event, self)
            # Updates
            for lay in self.layers:
                lay.update(dt, self)

            # Render
            for lay in self.layers:
                lay.render(window)

            pygame.display.flip()
