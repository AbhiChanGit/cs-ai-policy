"""Phase 2 checks: the collected data is complete and traceable."""
import csv
import os
import re

PHASE = "P2"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def rows(name):
    with open(os.path.join(DATA, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_at_least_25_institutions():
    """SPEC P2: policies.csv has at least 25 institutions."""
    assert len(rows("policies.csv")) >= 25


def test_at_least_8_se_courses():
    """SPEC P2: se_courses.csv has at least 8 software engineering courses."""
    assert len(rows("se_courses.csv")) >= 8


def test_ids_unique():
    """No institution or course appears twice (duplicates would inflate counts)."""
    ids = [r["id"] for r in rows("policies.csv")] + [r["id"] for r in rows("se_courses.csv")]
    assert len(ids) == len(set(ids))


def test_institution_names_unique():
    """Each institution is sampled once in policies.csv (one source per school)."""
    names = [r["institution"] for r in rows("policies.csv")]
    assert len(names) == len(set(names))


def test_every_row_has_url_and_access_date():
    """Every source row has an http(s) URL and a YYYY-MM-DD access date."""
    for r in rows("policies.csv") + rows("se_courses.csv"):
        assert r["url"].startswith("http"), r["id"]
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["accessed"]), r["id"]


def test_level_values_valid():
    """Source level is one of department / college / university."""
    for r in rows("policies.csv"):
        assert r["level"] in {"department", "college", "university"}, r["id"]


def test_raw_excerpt_exists_for_every_row():
    """Every source has a non-empty raw excerpt file with at least 2 excerpt lines."""
    for r in rows("policies.csv") + rows("se_courses.csv"):
        path = os.path.join(DATA, "raw", r["id"] + ".txt")
        assert os.path.exists(path), r["id"]
        text = open(path, encoding="utf-8").read()
        assert text.count("\n- ") >= 2, r["id"]


def test_raw_header_url_matches_csv():
    """The URL inside each raw file matches the CSV row (no mixed-up files)."""
    for r in rows("policies.csv") + rows("se_courses.csv"):
        text = open(os.path.join(DATA, "raw", r["id"] + ".txt"), encoding="utf-8").read()
        assert r["url"].split(" ;")[0] in text, r["id"]


def test_no_orphan_raw_files():
    """Every raw file belongs to a CSV row (nothing collected and silently dropped)."""
    ids = {r["id"] for r in rows("policies.csv")} | {r["id"] for r in rows("se_courses.csv")}
    files = {f[:-4] for f in os.listdir(os.path.join(DATA, "raw")) if f.endswith(".txt")}
    assert files == ids


def test_us_institutions_only():
    """Sample is US only (state column is a 2-letter US code)."""
    for r in rows("policies.csv"):
        assert re.fullmatch(r"[A-Z]{2}", r["state"]), r["id"]
