"""All keyboard controls of the game, in one place."""
import pygame

# Movement: key -> (dx, dy) in cells
MOVE_KEYS: dict[int, tuple[int, int]] = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    # ... finish with LEFT, RIGHT, and maybe WASD
}

PAUSE_KEYS = {pygame.K_ESCAPE}
CONFIRM_KEYS = {pygame.K_RETURN}

# Cheats: key -> name of the cheat
CHEAT_KEYS: dict[int, str] = {
    pygame.K_F1: "invincible",
    # ...
}
