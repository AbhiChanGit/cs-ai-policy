"""Phase 6 and 7 checks: the timeline and token parsers are correct on known inputs."""
import json
import os
import re

import tokens
import timeline

PHASE = "P7"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _write_jsonl(tmp_path, lines):
    p = tmp_path / "s.jsonl"
    p.write_text("\n".join(json.dumps(l) for l in lines), encoding="utf-8")
    return str(p)


def _asst(mid, ts, i=1, cw=10, cr=100, out=5):
    return {"type": "assistant", "timestamp": ts, "message": {"id": mid, "usage": {
        "input_tokens": i, "cache_creation_input_tokens": cw, "cache_read_input_tokens": cr, "output_tokens": out}}}


def test_duplicate_message_ids_counted_once(tmp_path):
    """One API response logged on several lines (same message id) is counted once, not per line."""
    path = _write_jsonl(tmp_path, [_asst("m1", "2026-01-01T00:00:01Z"), _asst("m1", "2026-01-01T00:00:01Z"),
                                   _asst("m2", "2026-01-01T00:00:02Z")])
    calls, _ = tokens.parse_session(path)
    assert len(calls) == 2


def test_context_is_sum_of_input_kinds(tmp_path):
    """Context size = fresh input + cache write + cache read (output excluded)."""
    path = _write_jsonl(tmp_path, [_asst("m1", "2026-01-01T00:00:01Z", i=3, cw=40, cr=500, out=99)])
    calls, _ = tokens.parse_session(path)
    assert calls[0]["context"] == 543


def test_compact_and_clear_events_detected(tmp_path):
    """Compaction boundaries and /clear commands in a transcript are reported as events."""
    path = _write_jsonl(tmp_path, [
        {"type": "system", "subtype": "compact_boundary", "timestamp": "2026-01-01T00:00:03Z"},
        {"type": "user", "timestamp": "2026-01-01T00:00:04Z", "message": {"content": "<command-name>/clear</command-name>"}},
    ])
    _, events = tokens.parse_session(path)
    assert [e["kind"] for e in events] == ["compact", "clear"]


def test_phase_assigned_to_next_log_entry():
    """A call is assigned to the phase of the first PROGRESS entry at or after it."""
    entries = [{"ts": "2026-01-01T00:10:00Z", "phase": "P1"}, {"ts": "2026-01-01T00:20:00Z", "phase": "P2"}]
    assert tokens.phase_for("2026-01-01T00:05:00.123Z", entries) == "P1"
    assert tokens.phase_for("2026-01-01T00:15:00.000Z", entries) == "P2"
    assert tokens.phase_for("2026-01-01T00:25:00.000Z", entries) == "P10+"


def test_clear_estimate_toy_example():
    """/clear estimate: within a phase, only context above the phase's first call counts as avoidable."""
    calls = [{"phase": "P1", "context": 100}, {"phase": "P1", "context": 150},
             {"phase": "P2", "context": 300}, {"phase": "P2", "context": 320}]
    assert tokens.clear_estimate(calls) == 50 + 20


def test_tokens_json_phase_totals_add_up():
    """Published token totals equal the sum over phases and the sum over calls."""
    d = tokens.build()
    s = next(x for x in d["sessions"] if x["main"])
    for k in ["input", "cache_write", "cache_read", "output", "calls"]:
        assert sum(p[k] for p in s["by_phase"]) == s["totals"][k], k
    assert sum(c["output"] for c in s["calls"]) == s["totals"]["output"]


def test_progress_lines_all_parse():
    """Every bullet line in PROGRESS.md matches the log format (nothing malformed or hand-mangled)."""
    lines = [l for l in open(os.path.join(ROOT, "PROGRESS.md"), encoding="utf-8") if l.startswith("- ")]
    assert lines and all(timeline.PROGRESS_RE.match(l.strip()) for l in lines)


def test_progress_timestamps_in_order():
    """PROGRESS.md never goes backwards: each line's write time (its timestamp, or the 'Backfilled at' time for a line that records an earlier event) is in order."""
    import re
    written = []
    for e in timeline.read_progress():
        m = re.search(r"Backfilled at (\S+Z)", e["text"])
        written.append(m.group(1) if m else e["ts"])
        if m:
            assert e["ts"] <= m.group(1), "a backfilled event cannot be later than when it was logged"
    assert written == sorted(written)


def test_progress_actors_valid():
    """Every log entry names its actor as Human or Claude."""
    assert {e["actor"] for e in timeline.read_progress()} <= {"Human", "Claude"}


def test_prompts_all_parsed():
    """Every '## ' entry in PROMPTS.md is parsed with both a human request and a Claude response."""
    text = open(os.path.join(ROOT, "PROMPTS.md"), encoding="utf-8").read()
    prompts = timeline.read_prompts()
    assert len(prompts) == len(re.findall(r"^## ", text, flags=re.M))
    assert all(p["human"] and p["claude"] for p in prompts)
