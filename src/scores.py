"""Read the high score file.

File format (JSON list):
    [{"name": "Alice", "score": 1200}, {"name": "Bob", "score": 800}]

A missing, unreadable or malformed file never crashes the game:
it just means "no scores yet". Bad entries are skipped.
"""

import json
import logging

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
