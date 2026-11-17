"""Records every test result (id, phase, docstring, outcome, duration) to
reports/last_run.json so src/run_tests.py can publish it to the validation page.

Each test module sets PHASE = "P2" (etc.). The test docstring is the plain
English statement of what the test proves; it is shown on the page.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

_results = []


def pytest_runtest_makereport(item, call):
    if call.when != "call" and not (call.when == "setup" and call.excinfo is not None):
        return
    doc = (item.function.__doc__ or "").strip()
    outcome = "passed"
    message = ""
    if call.excinfo is not None:
        if call.excinfo.errisinstance(__import__("_pytest").outcomes.Skipped):
            outcome = "skipped"
            message = str(call.excinfo.value)
        else:
            outcome = "failed"
            message = call.excinfo.exconly()[:600]
    _results.append({
        "id": item.nodeid,
        "name": item.name,
        "file": os.path.basename(str(item.fspath)),
        "phase": getattr(item.module, "PHASE", "?"),
        "doc": " ".join(doc.split()),
        "outcome": outcome,
        "duration_s": round(call.duration, 4),
        "message": message,
    })


def pytest_sessionfinish(session, exitstatus):
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    with open(os.path.join(ROOT, "reports", "last_run.json"), "w", encoding="utf-8") as f:
        json.dump(_results, f, indent=1)
