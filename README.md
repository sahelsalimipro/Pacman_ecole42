## Configuration

The game is started with one argument, a configuration file:

```console
python3 pac-man.py config.json
```

The file is standard JSON plus comments: any line whose first non-blank
characters are `#` or `//` is ignored. To check a file without starting
the game, run `python3 src/config.py my_config.json`.

| Key | Type | Default | Allowed range | Meaning |
|-----|------|---------|---------------|---------|
| `highscore_filename` | string | `"highscores.json"` | non-empty | File where the top 10 scores are saved |
| `lives` | int | 3 | 1 – 99 | Lives at the start of a game |
| `points_per_pacgum` | int | 10 | 0 – 10 000 | Points for a pacgum |
| `points_per_super_pacgum` | int | 50 | 0 – 10 000 | Points for a super-pacgum |
| `points_per_ghost` | int | 200 | 0 – 100 000 | Points for eating an edible ghost |
| `level_max_time` | int | 90 | 10 – 3600 | Time limit of a level, in seconds |
| `edible_duration` | int | 8 | 1 – 60 | How long ghosts stay edible, in seconds |
| `ghost_respawn_delay` | int | 5 | 1 – 60 | Delay before an eaten ghost comes back, in seconds |
| `edible_ghost_speed_ratio` | number | 0.5 | 0.1 – 1.0 | Edible ghosts move at `ghost_speed` × this ratio |
| `levels` | array | 10 levels, growing | 10 – 100 entries | One object per level (keys below) |
| `levels[i].name` | string | `"Level <i+1>"` | non-empty | Level title |
| `levels[i].seed` | int | 42 for level 1, 0 after | 0 – 2³¹−1 | Maze seed; 0 means a random maze |
| `levels[i].ghosts` | int | 1, 2, 3, then 4 | 1 – 4 | Number of ghosts |
| `levels[i].width` | int | 15, growing | 14 – 40 | Maze width, in cells |
| `levels[i].height` | int | 11, growing | 10 – 25 | Maze height, in cells |
| `levels[i].ghost_speed` | number | 4.0, +0.25 per level | 0.5 – 20 | Ghost speed, in cells per second |

A missing or invalid level key takes the value of the default level at
the same position (table above).

The minimum maze size is 14 x 10 because the maze package needs it to
draw its "42" pattern; smaller sizes print a warning, and a width of 0
makes the package crash.

### Error handling

- **Missing key, wrong type, or value out of range**: a warning is
  logged, the value is replaced by its default (wrong type) or the
  nearest allowed value (out of range), and the game continues.
  `true`/`false` are refused for numbers, decimals such as `3.5`
  are refused for integers, and `NaN`/`Infinity` are refused for
  decimal values.
- **Unknown key**: ignored, with an info message.
- **Fewer than 10 levels**: the list is completed with default levels.
  A level that is not an object is replaced by the default level.
  More than 100: only the first 100 are used.
- **File missing, unreadable, invalid JSON, or not a JSON object**:
  the game prints a clear error (with line and column for JSON errors)
  and exits. It never shows a Python traceback.


### Resources:
- https://www.geeksforgeeks.org/python/pygame-tutorial/
