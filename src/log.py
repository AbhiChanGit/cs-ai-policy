"""Append one timestamped line to PROGRESS.md.

Usage: python src/log.py <phase> <Human|Claude> "<summary>"
The timestamp is taken from the clock at the moment of logging, so entries
cannot be back-dated by hand.
"""
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) != 4 or sys.argv[2] not in ("Human", "Claude"):
        sys.exit(__doc__)
    phase, actor, summary = sys.argv[1:]
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"- {ts} | {phase} | {actor} | {summary.strip()}\n"
    with open(os.path.join(ROOT, "PROGRESS.md"), "a", encoding="utf-8") as f:
        f.write(line)
    print(line, end="")


if __name__ == "__main__":
    main()
