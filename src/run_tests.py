"""Run the test suite and publish the results to docs/data/tests.json.

Usage: python src/run_tests.py "<label for this run>"

Each run is appended to reports/history.json (kept forever), so the validation
page can show how the suite grew phase by phase, including failing runs.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")
OUT = os.path.join(ROOT, "docs", "data", "tests.json")


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "manual run"
    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests"],
                          cwd=ROOT, capture_output=True, text=True)
    print(proc.stdout[-1500:])
    with open(os.path.join(REPORTS, "last_run.json"), encoding="utf-8") as f:
        results = json.load(f)

    totals = {k: sum(r["outcome"] == k for r in results) for k in ["passed", "failed", "skipped"]}
    run = {"timestamp": started, "label": label, "total": len(results), **totals,
           "pytest_exit_code": proc.returncode, "results": results}

    hist_path = os.path.join(REPORTS, "history.json")
    history = json.load(open(hist_path, encoding="utf-8")) if os.path.exists(hist_path) else []
    history.append(run)
    with open(hist_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=1)

    review_path = os.path.join(ROOT, "REVIEW.md")
    review = open(review_path, encoding="utf-8").read() if os.path.exists(review_path) else ""
    page = {
        "generated_by": "src/run_tests.py",
        "latest": run,
        "history": [{k: v for k, v in r.items() if k != "results"} for r in history],
        "runs_full": [r["results"] for r in history],  # lets the page open any past run, failing ones included
        "review_md": review,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(page, f, indent=1)
    # .js twin so the page also works when opened straight from disk (file://)
    with open(OUT[:-5] + ".js", "w", encoding="utf-8") as f:
        f.write("window.DATA_TESTS = " + json.dumps(page, ensure_ascii=False) + ";\n")
    print(f"run '{label}': {totals} -> docs/data/tests.json")
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
