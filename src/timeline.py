"""Phase 6: PROGRESS.md + PROMPTS.md -> docs/data/timeline.json.

Usage: python src/timeline.py
"""
import json
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "data", "timeline.json")
PROGRESS_RE = re.compile(r"^- (\S+Z) \| (\S+) \| (\w+) \| (.*)$")


def read_progress():
    out = []
    with open(os.path.join(ROOT, "PROGRESS.md"), encoding="utf-8") as f:
        for line in f:
            m = PROGRESS_RE.match(line.strip())
            if m:
                out.append({"ts": m.group(1), "phase": m.group(2), "actor": m.group(3), "text": m.group(4)})
    return out


def read_prompts():
    text = open(os.path.join(ROOT, "PROMPTS.md"), encoding="utf-8").read()
    out = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        human = re.search(r"\*\*Human:\*\*\s*(.*?)(?=\n\*\*Claude:\*\*|\Z)", body, re.S)
        claude = re.search(r"\*\*Claude:\*\*\s*(.*)", body, re.S)
        out.append({"ts": head.strip(), "human": human.group(1).strip() if human else "",
                    "claude": claude.group(1).strip() if claude else ""})
    return out


def build():
    progress = read_progress()
    data = {
        "generated_by": "src/timeline.py",
        "progress": progress,
        "prompts": read_prompts(),
        "by_actor": dict(Counter(e["actor"] for e in progress)),
        "by_phase_actor": [{"phase": p, "actor": a, "n": n}
                           for (p, a), n in sorted(Counter((e["phase"], e["actor"]) for e in progress).items())],
        "human_tasks": [
            {"task": "Fill the 10-row blind sample in data/human_labels.csv, then rerun src/run_tests.py",
             "why": "Gives a human-vs-Claude kappa: the strongest evidence the labels are valid"},
            {"task": "Spot-check 5 source URLs against data/raw excerpts",
             "why": "Excerpts were pulled by a fetch tool; a human check confirms they are faithful"},
            {"task": "Read 3 tests yourself and add notes to REVIEW.md",
             "why": "The brief asks for documented direct review, not only Claude-written tests"},
            {"task": "Write the reflection in EVALUATION.md",
             "why": "The brief says the evaluation and reflection are completed primarily by the student"},
        ],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    # .js twin so the page also works when opened straight from disk (file://)
    with open(OUT[:-5] + ".js", "w", encoding="utf-8") as f:
        f.write("window.DATA_TIMELINE = " + json.dumps(data, ensure_ascii=False) + ";\n")
    return data


if __name__ == "__main__":
    d = build()
    print(len(d["progress"]), "progress entries,", len(d["prompts"]), "prompts; by actor:", d["by_actor"])
