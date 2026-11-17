"""Phase 4 and 8 checks: the static site is complete and self-contained."""
import json
import os
import re

PHASE = "P4"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
PAGES = ["index.html", "tests.html", "timeline.html", "tokens.html"]


def html(name):
    return open(os.path.join(DOCS, name), encoding="utf-8").read()


def test_all_four_pages_exist():
    """The four required pages exist: findings, validation, timeline, tokens."""
    for p in PAGES:
        assert os.path.exists(os.path.join(DOCS, p)), p


def test_local_references_resolve():
    """Every local src/href in every page points to a file that exists (no broken links)."""
    for p in PAGES:
        for ref in re.findall(r'(?:src|href)="([^"#]+)"', html(p)):
            if ref.startswith(("http", "mailto", "$")) or "${" in ref:
                continue
            assert os.path.exists(os.path.join(DOCS, ref)), (p, ref)


def test_no_external_scripts():
    """Pages load no third-party scripts, so they work offline and on GitHub Pages."""
    for p in PAGES:
        assert not re.search(r'<script[^>]+src="https?://', html(p)), p


def test_every_page_links_every_page():
    """Shared nav lists all four pages."""
    js = open(os.path.join(DOCS, "assets", "common.js"), encoding="utf-8").read()
    for p in PAGES:
        assert f'"{p}"' in js, p


def test_data_files_match_json():
    """Each docs/data/*.js twin holds exactly the same data as its .json file."""
    data = os.path.join(DOCS, "data")
    for name in ["findings", "tests", "timeline", "tokens"]:
        js = open(os.path.join(data, name + ".js"), encoding="utf-8").read()
        prefix = f"window.DATA_{name.upper()} = "
        assert js.startswith(prefix), name
        assert json.loads(js[len(prefix):].rstrip().rstrip(";")) == json.load(open(os.path.join(data, name + ".json"), encoding="utf-8")), name


def test_findings_page_has_no_typed_counts():
    """Key findings text on index.html is generated from data (no hard-coded 'N of M' numbers)."""
    body = html("index.html")
    findings_js = body[body.index('document.getElementById("findings")'):body.index('barList(')]
    assert not re.search(r"\b\d+ of \d+\b", findings_js)


def test_readme_links_pages():
    """README links all four published pages."""
    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    for p in PAGES:
        assert p in readme, p
