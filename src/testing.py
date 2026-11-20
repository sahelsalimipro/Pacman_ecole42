import pygame
from mazegenerator import MazeGenerator

pygame.init()

screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Hello World")

color = (200, 0, 0)
screen.fill(color)

pygame.draw.circle(screen, (0, 0, 0), (250, 200), 175)
# so apparently, we draw a shape on a surface. What about undefined shape then ? Idk

pygame.display.flip()  # TODO What does this do precisely ? Updates the changed values ? Idk, flip is a weird name for an "apply function"
# Confirmed: it is the function that tells to update, but what precisely, I still don't know how this works internally.

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()


maze = MazeGenerator(
    size = (15,15),
    perfect = False,
    entry_cell = (0, 7),
    exit_cell = (14, 7),
    seed = 42
)
