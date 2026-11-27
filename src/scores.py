"""Read and write the high score file.

File format (JSON list):
    [{"name": "Alice", "score": 1200}, {"name": "Bob", "score": 800}]

A missing, unreadable or malformed file never crashes the game:
it just means "no scores yet". Bad entries are skipped.
A failed write is logged and the game goes on.
"""

import json
import logging
import os

log = logging.getLogger("scores")

MAX_SCORES = 10


def load_scores(path: str) -> list[tuple[str, int]]:
    """Return the best scores as (name, score), highest first."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except (OSError, ValueError) as err:
        log.warning("cannot read %s: %s", path, err)
        return []

    if not isinstance(data, list):
        log.warning("%s: expected a list of scores", path)
        return []

    scores: list[tuple[str, int]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        score = item.get("score")
        # bool is a subclass of int: reject true/false explicitly
        if (isinstance(name, str) and isinstance(score, int)
                and not isinstance(score, bool) and score >= 0):
            scores.append((name, score))

    scores.sort(key=lambda s: s[1], reverse=True)
    return scores[:MAX_SCORES]


def is_high_score(path: str, score: int) -> bool:
    """True if ``score`` would enter the top list (ask for a name only then)."""
    scores = load_scores(path)
    return len(scores) < MAX_SCORES or score > scores[-1][1]


def save_score(path: str, name: str, score: int) -> bool:
    """Add a score, keep the best MAX_SCORES, write the file.

    Returns True if the score made it into the saved list.
    On a tie, the older score stays ahead of the new one.
    """
    scores = load_scores(path)
    scores.append((name, score))
    scores.sort(key=lambda s: s[1], reverse=True)  # stable: ties keep order
    scores = scores[:MAX_SCORES]
    if (name, score) not in scores:
        return False

    data = [{"name": n, "score": s} for n, s in scores]
    # Write to a temporary file, then swap it in: if the game crashes
    # mid-write, the old file is still intact.
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        os.replace(tmp, path)
    except OSError as err:
        log.warning("cannot save scores to %s: %s", path, err)
        return False
    return True
