"""Phase 7: token usage from Claude Code transcripts -> docs/data/tokens.json.

Claude Code writes every API response, with its `usage` block, to
~/.claude/projects/<project-folder>/<session-id>.jsonl. One response can appear
on several lines (one per content block) with the same message id, so we
de-duplicate by message id.

Token kinds per call:
  input        fresh, uncached input tokens
  cache_write  tokens written to the prompt cache this call
  cache_read   tokens re-read from cache (the whole conversation so far)
  output       tokens the model wrote (includes thinking)
Context size of a call = input + cache_write + cache_read.

Phases come from PROGRESS.md: a call belongs to the phase of the first
PROGRESS entry logged at or after it (work happens, then gets logged).

Usage: python src/tokens.py
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "data", "tokens.json")
PROJECTS = os.path.join(os.path.expanduser("~"), ".claude", "projects")

# Sessions to include: (label, project folder, session id). The Project 1
# session is included only as a comparison point.
SESSIONS = [
    ("Project 2 (this project)", "C--Abhishek-01-UC", "eac7ade5-a20b-4124-ac06-23f4bd080fa7"),
    ("Project 1 (Cincy311), comparison", "c--Abhishek-01-UC-Special-Topics-CompSci", "ba5bacd2-7bcf-4885-a2cf-1e589e93f324"),
]

PROGRESS_RE = re.compile(r"^- (\S+Z) \| (\S+) \| (\w+) \| (.*)$")


def read_progress():
    entries = []
    with open(os.path.join(ROOT, "PROGRESS.md"), encoding="utf-8") as f:
        for line in f:
            m = PROGRESS_RE.match(line.strip())
            if m:
                entries.append({"ts": m.group(1), "phase": m.group(2), "actor": m.group(3), "text": m.group(4)})
    return entries


def phase_for(ts, entries):
    for e in entries:
        if e["ts"] >= ts[:19] + "Z":
            return e["phase"]
    return "P10+"  # after the last log line (deck, wrap-up)


def parse_session(path):
    """Return (calls, events) from one transcript file."""
    calls, seen, events = [], set(), []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = d.get("type")
            if t == "system" and d.get("subtype") in ("compact_boundary", "microcompact_boundary"):
                events.append({"ts": d.get("timestamp"), "kind": "compact"})
            if d.get("isCompactSummary"):
                events.append({"ts": d.get("timestamp"), "kind": "compact"})
            if t == "user" and isinstance(d.get("message", {}).get("content"), str):
                c = d["message"]["content"]
                if c.startswith("<command-name>/clear") or c.startswith("<command-name>/compact"):
                    events.append({"ts": d.get("timestamp"), "kind": c[15:22].strip("<>/ ")})
            if t != "assistant":
                continue
            m = d.get("message", {})
            mid, u = m.get("id"), m.get("usage")
            if not u or mid in seen:
                continue
            seen.add(mid)
            calls.append({
                "ts": d.get("timestamp"),
                "sidechain": bool(d.get("isSidechain")),
                "input": u.get("input_tokens", 0),
                "cache_write": u.get("cache_creation_input_tokens", 0),
                "cache_read": u.get("cache_read_input_tokens", 0),
                "output": u.get("output_tokens", 0),
            })
    calls.sort(key=lambda c: c["ts"])
    for c in calls:
        c["context"] = c["input"] + c["cache_write"] + c["cache_read"]
    return calls, events


def totals(calls):
    keys = ["input", "cache_write", "cache_read", "output"]
    t = {k: sum(c[k] for c in calls) for k in keys}
    t["calls"] = len(calls)
    t["all"] = sum(t[k] for k in keys)
    t["peak_context"] = max((c["context"] for c in calls), default=0)
    return t


def clear_estimate(calls):
    """Estimate cache_read saved if context had been cleared at every phase change.

    Model: after a /clear, a call's context restarts at the size of the first call
    of that phase (system prompt + CLAUDE.md + SPEC.md re-read). Everything above
    that baseline is history that a /clear would have dropped. This is an
    estimate, not a measurement: a fresh session also re-reads files it needs.
    """
    saved, base, last_phase = 0, None, None
    for c in calls:
        if c["phase"] != last_phase:
            base, last_phase = c["context"], c["phase"]
        saved += max(0, c["context"] - base)
    return saved


def build():
    entries = read_progress()
    sessions = []
    for label, folder, sid in SESSIONS:
        path = os.path.join(PROJECTS, folder, sid + ".jsonl")
        if not os.path.exists(path):
            continue
        calls, events = parse_session(path)
        main = label.startswith("Project 2")
        for c in calls:
            c["phase"] = phase_for(c["ts"], entries) if main else "P1-project"
        by_phase = {}
        for c in calls:
            by_phase.setdefault(c["phase"], []).append(c)
        sessions.append({
            "label": label, "session_id": sid, "main": main,
            "totals": totals(calls),
            "by_phase": [{"phase": p, **totals(cs)} for p, cs in by_phase.items()],
            "events": events,
            "clear_estimate_saved_cache_read": clear_estimate(calls) if main else None,
            "calls": calls,
        })
    data = {"generated_by": "src/tokens.py", "sessions": sessions,
            "phase_names": {"P0": "Kickoff and planning", "P1": "Setup and specs", "P2": "Data collection",
                            "P3": "Coding and analysis", "P4": "Findings dashboard", "P5": "Validation explorer",
                            "P6": "Timeline page", "P7": "Token page", "P8": "Publish", "P9": "Evaluation",
                            "P10": "Presentation", "P10+": "After last log line"}}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f)
    # .js twin so the page also works when opened straight from disk (file://)
    with open(OUT[:-5] + ".js", "w", encoding="utf-8") as f:
        f.write("window.DATA_TOKENS = " + json.dumps(data, ensure_ascii=False) + ";\n")
    return data


if __name__ == "__main__":
    d = build()
    for s in d["sessions"]:
        t = s["totals"]
        print(f"{s['label']}: {t['calls']} calls, input {t['input']:,}, cache_write {t['cache_write']:,}, "
              f"cache_read {t['cache_read']:,}, output {t['output']:,}, peak context {t['peak_context']:,}")
        for p in s["by_phase"]:
            print(f"   {p['phase']}: {p['calls']} calls, all {p['all']:,}, output {p['output']:,}")
        if s["clear_estimate_saved_cache_read"] is not None:
            print(f"   est. cache_read avoidable with /clear at phase changes: {s['clear_estimate_saved_cache_read']:,}")
