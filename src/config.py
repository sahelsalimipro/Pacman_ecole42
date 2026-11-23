"""Load and validate the Pac-Man configuration file.

The file is JSON with one extension: lines whose first non-blank
characters are ``#`` or ``//`` are comments and are ignored.

Policy (subject, section 5.3):
    * missing or invalid value -> log a warning, use a safe value, continue;
    * unknown key -> log an info message and ignore it;
    * file-level problem (unreadable file, broken JSON, root not an
      object) -> raise ``ConfigError`` with a clear message. The caller
      prints it and exits without a traceback.
"""

import json
import logging
import sys
from dataclasses import dataclass, field
from typing import Any

log = logging.getLogger("config")

# Limits for the maze size, in cells. Below 14x10 the maze package
# cannot draw its '42' pattern and prints a warning; width 1 or 0
# breaks it. The maximum keeps the maze inside the window.
MIN_WIDTH, MAX_WIDTH = 14, 40
MIN_HEIGHT, MAX_HEIGHT = 10, 25

MIN_LEVELS = 10   # the subject asks for at least 10 levels
MAX_LEVELS = 100

MAX_GHOSTS = 4    # one per maze corner
# Seed given to the maze package. 0 means "random maze" for the package.
MAX_SEED = 2**31 - 1
# Ghost speed, in cells per second.
MIN_GHOST_SPEED, MAX_GHOST_SPEED = 0.5, 20.0


@dataclass
class LevelConfig:
    """Parameters of one level.

    Attributes:
        name: Title shown to the player.
        ghosts: Number of ghosts, 1 to MAX_GHOSTS.
        seed: Maze seed; 0 asks the maze package for a random maze.
        width: Maze width, in cells.
        height: Maze height, in cells.
        ghost_speed: Ghost speed when chasing, in cells per second.
    """

    name: str = "Level"
    ghosts: int = MAX_GHOSTS
    seed: int = 0
    width: int = 15
    height: int = 11
    ghost_speed: float = 4.0


def _default_level(i: int) -> LevelConfig:
    """Return the default level at index ``i`` (0-based).

    Mazes and ghost speed slowly grow. As the subject asks, the first
    maze uses the fixed seed 42 and the next ones are random (seed 0).
    """
    return LevelConfig(
        name=f"Level {i + 1}",
        ghosts=min(i + 1, MAX_GHOSTS),
        seed=42 if i == 0 else 0,
        width=min(15 + 2 * (i // 3), MAX_WIDTH),
        height=min(11 + 2 * (i // 4), MAX_HEIGHT),
        ghost_speed=min(4.0 + 0.25 * i, MAX_GHOST_SPEED),
    )


def _default_levels() -> list[LevelConfig]:
    """Return the MIN_LEVELS default levels."""
    return [_default_level(i) for i in range(MIN_LEVELS)]


@dataclass
class GameConfig:
    """All game parameters, always valid once built by ``load_config``."""

    highscore_filename: str = "highscores.json"
    lives: int = 3
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    level_max_time: int = 90
    edible_duration: int = 8
    ghost_respawn_delay: int = 5
    edible_ghost_speed_ratio: float = 0.5
    levels: list[LevelConfig] = field(default_factory=_default_levels)


class ConfigError(Exception):
    """The configuration file cannot be used at all."""


# key: (default, minimum, maximum)
INT_KEYS: dict[str, tuple[int, int, int]] = {
    "lives": (3, 1, 99),
    "points_per_pacgum": (10, 0, 10_000),
    "points_per_super_pacgum": (50, 0, 10_000),
    "points_per_ghost": (200, 0, 100_000),
    "level_max_time": (90, 10, 3600),
    "edible_duration": (8, 1, 60),
    "ghost_respawn_delay": (5, 1, 60),
}
# key: (default, minimum, maximum)
FLOAT_KEYS: dict[str, tuple[float, float, float]] = {
    # Edible ghosts move at ghost_speed * this ratio
    "edible_ghost_speed_ratio": (0.5, 0.1, 1.0),
}
KNOWN_KEYS = set(INT_KEYS) | set(FLOAT_KEYS) | {"highscore_filename",
                                                "levels"}
LEVEL_KEYS = {"name", "ghosts", "seed", "width", "height", "ghost_speed"}


def strip_comments(text: str) -> str:
    """Blank out comment lines, keeping line numbers for error messages.

    Args:
        text: Raw content of the configuration file.

    Returns:
        The same text where every comment line is now empty.
    """
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#") or stripped.startswith("//"):
            lines.append("")
        else:
            lines.append(line)
    return "\n".join(lines)


def read_int(data: dict[str, Any], key: str, default: int,
             low: int, high: int, where: str = "") -> int:
    """Read an integer and force it into [low, high].

    Args:
        data: Parsed JSON object.
        key: Key to read.
        default: Value used when the key is missing or not an integer.
        low: Smallest accepted value.
        high: Largest accepted value.
        where: Prefix for log messages, e.g. "levels[2].".

    Returns:
        A valid integer.
    """
    name = where + key
    if key not in data:
        log.warning("'%s' is missing, using default %d", name, default)
        return default
    value = data[key]
    # bool is a subclass of int in Python: true would be read as 1
    if isinstance(value, bool) or not isinstance(value, int):
        log.warning("'%s' must be an integer (got %r), using default %d",
                    name, value, default)
        return default
    if value < low or value > high:
        clamped = min(max(value, low), high)
        log.warning("'%s' = %d is out of range [%d, %d], clamped to %d",
                    name, value, low, high, clamped)
        return clamped
    return value


def read_float(data: dict[str, Any], key: str, default: float,
               low: float, high: float, where: str = "") -> float:
    """Read a number (integer or decimal) and force it into [low, high].

    Args:
        data: Parsed JSON object.
        key: Key to read.
        default: Value used when the key is missing or not a number.
        low: Smallest accepted value.
        high: Largest accepted value.
        where: Prefix for log messages, e.g. "levels[2].".

    Returns:
        A valid float.
    """
    name = where + key
    if key not in data:
        log.warning("'%s' is missing, using default %g", name, default)
        return default
    value = data[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        log.warning("'%s' must be a number (got %r), using default %g",
                    name, value, default)
        return default
    # json accepts NaN and Infinity, which would break the game loop
    if value != value or value in (float("inf"), float("-inf")):
        log.warning("'%s' must be a finite number, using default %g",
                    name, default)
        return default
    if value < low or value > high:
        clamped = min(max(float(value), low), high)
        log.warning("'%s' = %g is out of range [%g, %g], clamped to %g",
                    name, value, low, high, clamped)
        return clamped
    return float(value)


def read_filename(data: dict[str, Any], key: str, default: str) -> str:
    """Read a non-empty file name string.

    Args:
        data: Parsed JSON object.
        key: Key to read.
        default: Value used when the key is missing or invalid.

    Returns:
        A non-empty string.
    """
    if key not in data:
        log.warning("'%s' is missing, using default '%s'", key, default)
        return default
    value = data[key]
    if not isinstance(value, str) or not value.strip():
        log.warning("'%s' must be a non-empty string (got %r), "
                    "using default '%s'", key, value, default)
        return default
    return value.strip()


def read_level(item: dict[str, Any], i: int,
               default: LevelConfig) -> LevelConfig:
    """Read one entry of the "levels" array.

    Args:
        item: The level's JSON object.
        i: Index of the level, for log messages.
        default: Level whose values replace missing or invalid ones.

    Returns:
        A valid level.
    """
    where = f"levels[{i}]."
    for key in sorted(item.keys() - LEVEL_KEYS):
        log.info("Unknown key '%s%s' ignored", where, key)
    name = default.name
    if "name" in item:
        if isinstance(item["name"], str) and item["name"].strip():
            name = item["name"].strip()
        else:
            log.warning("'%sname' must be a non-empty string (got %r), "
                        "using '%s'", where, item["name"], name)
    return LevelConfig(
        name=name,
        ghosts=read_int(item, "ghosts", default.ghosts, 1, MAX_GHOSTS,
                        where),
        seed=read_int(item, "seed", default.seed, 0, MAX_SEED, where),
        width=read_int(item, "width", default.width, MIN_WIDTH, MAX_WIDTH,
                       where),
        height=read_int(item, "height", default.height, MIN_HEIGHT,
                        MAX_HEIGHT, where),
        ghost_speed=read_float(item, "ghost_speed", default.ghost_speed,
                               MIN_GHOST_SPEED, MAX_GHOST_SPEED, where),
    )


def read_levels(data: dict[str, Any]) -> list[LevelConfig]:
    """Read the "levels" array, fixing each level and the level count.

    Args:
        data: Parsed JSON object.

    Returns:
        Between MIN_LEVELS and MAX_LEVELS valid levels.
    """
    if "levels" not in data:
        log.warning("'levels' is missing, using %d default levels",
                    MIN_LEVELS)
        return _default_levels()
    raw = data["levels"]
    if not isinstance(raw, list):
        log.warning("'levels' must be an array, using %d default levels",
                    MIN_LEVELS)
        return _default_levels()

    levels: list[LevelConfig] = []
    for i, item in enumerate(raw[:MAX_LEVELS]):
        default = _default_level(i)
        if not isinstance(item, dict):
            log.warning("'levels[%d]' must be an object, using default "
                        "level", i)
            levels.append(default)
            continue
        levels.append(read_level(item, i, default))
    if len(raw) > MAX_LEVELS:
        log.warning("Only the first %d levels are used", MAX_LEVELS)

    if len(levels) < MIN_LEVELS:
        defaults = _default_levels()
        log.warning("Only %d level(s) given, %d needed: adding default "
                    "levels", len(levels), MIN_LEVELS)
        levels.extend(defaults[len(levels):])
    return levels


def parse_config(data: dict[str, Any]) -> GameConfig:
    """Build a valid GameConfig from an already parsed JSON object.

    Args:
        data: Parsed JSON object (any content).

    Returns:
        A configuration where every value is valid.
    """
    for key in sorted(data.keys() - KNOWN_KEYS):
        log.info("Unknown key '%s' ignored", key)

    cfg = GameConfig()
    cfg.highscore_filename = read_filename(
        data, "highscore_filename", cfg.highscore_filename)
    for key, (default, low, high) in INT_KEYS.items():
        setattr(cfg, key, read_int(data, key, default, low, high))
    for key, (fdefault, flow, fhigh) in FLOAT_KEYS.items():
        setattr(cfg, key, read_float(data, key, fdefault, flow, fhigh))
    cfg.levels = read_levels(data)
    return cfg


def load_config(path: str) -> GameConfig:
    """Read, parse and validate a configuration file.

    Args:
        path: Path of the JSON (with comments) file.

    Returns:
        A configuration where every value is valid.

    Raises:
        ConfigError: The file cannot be read or is not a JSON object.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        raise ConfigError(f"config file '{path}' not found") from None
    except IsADirectoryError:
        raise ConfigError(f"'{path}' is a directory, not a file") from None
    except PermissionError:
        raise ConfigError(f"no permission to read '{path}'") from None
    except UnicodeDecodeError:
        raise ConfigError(f"'{path}' is not a UTF-8 text file") from None
    except OSError as exc:
        raise ConfigError(f"cannot read '{path}': {exc.strerror}") from None

    try:
        data = json.loads(strip_comments(text))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"invalid JSON in '{path}', line {exc.lineno} "
                          f"column {exc.colno}: {exc.msg}") from None

    if not isinstance(data, dict):
        raise ConfigError(f"'{path}' must contain a JSON object "
                          "({ ... }) at the top level")
    return parse_config(data)


def main() -> int:
    """Check a config file from the command line and print the result."""
    logging.basicConfig(level=logging.INFO,
                        format="[config] %(levelname)s: %(message)s")
    if len(sys.argv) != 2:
        print("Usage: python3 src/config.py <config.json>", file=sys.stderr)
        return 1
    try:
        cfg = load_config(sys.argv[1])
    except ConfigError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    for name, value in vars(cfg).items():
        if name != "levels":
            print(f"{name:24} {value}")
    for level in cfg.levels:
        seed = level.seed if level.seed else "random"
        print(f"{level.name:<40} {level.width}x{level.height} | "
              f"ghosts: {level.ghosts} | speed: {level.ghost_speed:g} | "
              f"seed: {seed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
