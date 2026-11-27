"""Every size, thickness and shape of the game's graphics, in one place.

Colors live in ``colors.py``; this file holds everything else that is
a matter of taste. Change a value here and the screens follow: no
other file contains these numbers.

Sizes are in pixels unless the name says otherwise.
"""

# --- Game screen layout -------------------------------------------------
# Height of the bar above the maze (level name, later score and lives).
TOPBAR_HEIGHT = 60

# Empty space kept between the maze and the edges of its area.
# Keep it >= half the wall thickness, or the outer walls get clipped.
MAZE_MARGIN = 12

# Largest size of one maze cell. Stops small mazes from looking huge
# on a big window. Set it very high (e.g. 10_000) to always fill the area.
MAZE_MAX_CELL_SIZE = 48

# Smallest size of one maze cell, whatever the window size.
MAZE_MIN_CELL_SIZE = 4

# --- Maze walls -----------------------------------------------------------
# Wall thickness = cell size x this ratio, kept between MIN and MAX.
WALL_THICKNESS_RATIO = 0.15
WALL_MIN_THICKNESS = 2
WALL_MAX_THICKNESS = 8

# Rounded wall ends (0 = square ends). Half the thickness or more
# gives fully round ends.
WALL_BORDER_RADIUS = 2

# --- The solid '42' cells -------------------------------------------------
# Space between a solid block and the walls around it (0 = touches them).
SOLID_BLOCK_INSET = 3
# Rounded corners of the solid blocks (0 = square).
SOLID_BLOCK_BORDER_RADIUS = 4

# --- Top bar (HUD) --------------------------------------------------------
HUD_FONT_SIZE = 32
# Space between the window's left edge and the HUD text.
HUD_PADDING_X = 16
# Text shown in the top bar. {num}: level number, {total}: number of
# levels, {name}: level name from the config.
HUD_LEVEL_FORMAT = "Level {num}/{total}  {name}"
