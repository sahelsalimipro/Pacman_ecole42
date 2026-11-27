"""All keyboard controls of the game, in one place.

Layers never test ``pygame.K_...`` constants directly: they check
whether ``event.key`` is in one of the tables below. To change a
control, edit only this file.
"""
import pygame

# Directions, as (dx, dy) in cells. y grows downwards on screen.
UP: tuple[int, int] = (0, -1)
DOWN: tuple[int, int] = (0, 1)
LEFT: tuple[int, int] = (-1, 0)
RIGHT: tuple[int, int] = (1, 0)

# Movement: key -> direction.
# Arrows, plus WASD (QWERTY) and ZQSD (AZERTY) so both keyboard
# layouts work. None of these letters is used twice.
MOVE_KEYS: dict[int, tuple[int, int]] = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_w: UP,
    pygame.K_z: UP,
    pygame.K_s: DOWN,
    pygame.K_a: LEFT,
    pygame.K_q: LEFT,
    pygame.K_d: RIGHT,
}

# Menus: move the highlighted option up or down.
MENU_UP_KEYS = {pygame.K_UP, pygame.K_w, pygame.K_z}
MENU_DOWN_KEYS = {pygame.K_DOWN, pygame.K_s}

# Enter on the main keyboard and on the numeric keypad.
CONFIRM_KEYS = {pygame.K_RETURN, pygame.K_KP_ENTER}
# Open / close the pause menu, or go back from a sub-screen.
PAUSE_KEYS = {pygame.K_ESCAPE, pygame.K_p}
BACK_KEYS = {pygame.K_ESCAPE}

# Name entry (end of game): letters come from TEXTINPUT events,
# this key removes the last one.
ERASE_KEYS = {pygame.K_BACKSPACE}

# Cheats: key -> name of the cheat (only active in cheat mode).
CHEAT_INVINCIBLE = "invincible"
CHEAT_SKIP_LEVEL = "skip_level"
CHEAT_FREEZE_GHOSTS = "freeze_ghosts"
CHEAT_EXTRA_LIFE = "extra_life"

CHEAT_KEYS: dict[int, str] = {
    pygame.K_F1: CHEAT_INVINCIBLE,
    pygame.K_F2: CHEAT_SKIP_LEVEL,
    pygame.K_F3: CHEAT_FREEZE_GHOSTS,
    pygame.K_F4: CHEAT_EXTRA_LIFE,
}

# Text for the instructions screen (M5): (keys, action).
HELP_LINES: list[tuple[str, str]] = [
    ("Arrows / WASD / ZQSD", "Move"),
    ("Enter", "Confirm"),
    ("Esc / P", "Pause"),
    ("F1", "Cheat: invincible"),
    ("F2", "Cheat: skip level"),
    ("F3", "Cheat: freeze ghosts"),
    ("F4", "Cheat: extra life"),
]
