"""Print the next unfinished task of a team member, read from PLANNING.md.

Usage:
    python dev/next_task.py A      # next task for member A
    python dev/next_task.py        # next task for everyone

A task is considered finished when its row in the "Real progress" table
of PLANNING.md has the ✅ status. Tasks shared by "A+B" count for both.
"""

import io
import re
import sys
from pathlib import Path

PLANNING = Path(__file__).resolve().parent.parent / "project" / "PLANNING.md"

STATUS_LABELS = {
    "⬜": "not started",
    "🟦": "in progress",
    "✅": "done",
    "⚠️": "late",
    "❌": "blocked",
}


def split_row(line: str) -> list[str]:
    """Split a Markdown table row into stripped cells."""
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse(text: str) -> tuple[dict[str, list[str]], list[list[str]]]:
    """Return (task details by ID, progress rows in planning order).

    Breakdown rows have 6 columns: ID | Task | Owner | Diff. | Est. | Deps.
    Progress rows have 7 columns: ID | Owner | Planned | Actual | Status ...
    """
    tasks: dict[str, list[str]] = {}
    progress: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = split_row(line)
        if cells[0] == "ID":
            continue
        if not re.fullmatch(r"[A-Z][A-Za-z0-9]*", cells[0]):
            continue
        if len(cells) == 6:
            tasks[cells[0]] = cells
        elif len(cells) == 7:
            progress.append(cells)
    return tasks, progress


def owners_of(row: list[str]) -> list[str]:
    """Return the members owning a progress row ("A+B" -> ["A", "B"])."""
    return row[1].replace(" ", "").upper().split("+")


def is_done(row: list[str]) -> bool:
    """Tell whether a progress row is marked as finished."""
    return "✅" in row[4]


def status_label(row: list[str]) -> str:
    """Translate the status emoji into words."""
    for emoji, label in STATUS_LABELS.items():
        if emoji in row[4]:
            return label
    return row[4]


def describe(who: str, tasks: dict[str, list[str]],
             progress: list[list[str]]) -> None:
    """Print the next task (and the one after) for one member."""
    todo = [r for r in progress if who in owners_of(r) and not is_done(r)]
    total = sum(1 for r in progress if who in owners_of(r))
    if not todo:
        print(f"[{who}] Nothing left to do, all {total} tasks are done.")
        return

    row = todo[0]
    details = tasks.get(row[0], [row[0], "(no description)", "", "", "", ""])
    print(f"[{who}] Next task ({total - len(todo) + 1}/{total}):")
    print(f"  {row[0]} - {details[1]}")
    print(f"  Estimate : {details[4]}")
    print(f"  Planned  : {row[2]}")
    print(f"  Status   : {status_label(row)}")
    print(f"  Needs    : {details[5]}")
    if len(todo) > 1:
        after = todo[1]
        name = tasks.get(after[0], ["", "(no description)"])[1]
        print(f"  Then     : {after[0]} - {name}")


def main() -> int:
    """Entry point."""
    if not PLANNING.exists():
        print(f"Cannot find {PLANNING}", file=sys.stderr)
        return 1
    # Avoid encoding errors with emoji on Windows consoles
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")

    tasks, progress = parse(PLANNING.read_text(encoding="utf-8"))
    members = sorted({m for row in progress for m in owners_of(row)})

    if len(sys.argv) > 1:
        who = sys.argv[1].upper()
        if who not in members:
            print(f"Unknown member '{who}'. Known: {', '.join(members)}",
                  file=sys.stderr)
            return 1
        members = [who]

    for i, who in enumerate(members):
        if i:
            print()
        describe(who, tasks, progress)
    return 0


if __name__ == "__main__":
    sys.exit(main())
