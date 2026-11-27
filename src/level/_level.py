from mazegenerator import MazeGenerator

class Level():

    def __init__(
            self,
            name: str,
            seed: int,
            ghosts_nbr: int,
            width: int,
            height: int,
            ghost_speed: float
        ) -> None:

        self.name = name
        self.seed = seed
        self.ghosts_nbr = ghosts_nbr
        self.w = width
        self.h = height
        self.dimensions = (width, height)
        self.ghost_speed = ghost_speed

        # Maze
        self.maze = MazeGenerator(self.dimensions, False, seed=self.seed)

        return

    def __str__(self) -> str:
        return self.name
