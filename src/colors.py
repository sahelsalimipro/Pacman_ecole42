"""All the game's colors, in one place.

Change a value here and every screen using it follows.

Two levels:
  * base colors: the raw RGB values (the "paint pots");
  * roles: what each color is used for (background, button, ...).
Screens only use the roles, so restyling a screen = editing a role,
and changing a shade everywhere = editing a base color.
"""

Color = tuple[int, int, int]

# --- Base colors -------------------------------------------------------
WHITE: Color = (255, 255, 255)
BLACK: Color = (0, 0, 0)
LIGHT_GREY: Color = (230, 230, 230)
GREY: Color = (110, 110, 130)

NIGHT: Color = (20, 20, 28)
NAVY: Color = (30, 30, 40)
SLATE: Color = (45, 45, 60)
DUSK: Color = (90, 90, 120)
INDIGO: Color = (60, 60, 100)
INDIGO_LIGHT: Color = (90, 90, 140)
LAVENDER: Color = (140, 140, 220)

GOLD: Color = (255, 215, 0)
RED: Color = (200, 0, 0)
ROYAL_BLUE: Color = (40, 60, 220)
DEEP_BLUE: Color = (25, 30, 110)

# --- Roles: menus --------------------------------------------------------
MENU_BG = NAVY
TITLE = WHITE
TEXT = WHITE
TEXT_MUTED = GREY            # placeholders, "No scores yet"

# --- Roles: text input ---------------------------------------------------
INPUT_BG = NIGHT
INPUT_BORDER = DUSK
INPUT_BORDER_ACTIVE = LAVENDER

# --- Roles: buttons ------------------------------------------------------
BUTTON = INDIGO
BUTTON_HOVER = INDIGO_LIGHT
BUTTON_TEXT = WHITE
BUTTON_DISABLED = SLATE
BUTTON_DISABLED_TEXT = GREY

# --- Roles: scores -------------------------------------------------------
SCORE_FIRST = GOLD
SCORE_ROW = LIGHT_GREY

# --- Roles: game ---------------------------------------------------------
GAME_TOPBAR = BLACK
GAME_BG = BLACK              # around the maze
HUD_TEXT = WHITE             # level name in the top bar

# --- Roles: maze ---------------------------------------------------------
MAZE_BG = BLACK              # the corridors
WALL = ROYAL_BLUE
MAZE_BLOCK = DEEP_BLUE       # the solid '42' cells
