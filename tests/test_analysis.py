"""Phase 3 checks: labels follow the codebook, cite real text, and the
aggregates on the dashboard equal the CSV."""
import csv
import json
import os
import re
from collections import Counter

import pytest

import analyze

PHASE = "P3"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def rows(name):
    with open(os.path.join(DATA, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def raw(id_):
    return re.sub(r"\s+", " ", open(os.path.join(DATA, "raw", id_ + ".txt"), encoding="utf-8").read())


@pytest.fixture(scope="module")
def findings():
    return analyze.build()


def test_every_institution_is_coded():
    """coded.csv covers exactly the institutions in policies.csv."""
    assert {r["id"] for r in rows("coded.csv")} == {r["id"] for r in rows("policies.csv")}


def test_every_se_course_is_coded():
    """se_coded.csv covers exactly the courses in se_courses.csv."""
    assert {r["id"] for r in rows("se_coded.csv")} == {r["id"] for r in rows("se_courses.csv")}


def test_label_values_in_codebook():
    """Every label value is one the codebook defines (no invented categories)."""
    for r in rows("coded.csv"):
        assert r["stance"] in analyze.STANCES, r["id"]
        assert r["tone"] in analyze.TONES, r["id"]
        assert r["ai_collaboration"] in {"yes", "no"}, r["id"]
        assert r["disclosure"] in {"required", "instructor_sets", "not_stated"}, r["id"]
    for r in rows("se_coded.csv"):
        assert r["stance"] in analyze.SE_STANCES, r["id"]
        assert r["ai_as_learning_goal"] in {"yes", "no"}, r["id"]


def test_codebook_documents_every_value():
    """Every label value used in the code appears in codebook.md."""
    book = open(os.path.join(DATA, "codebook.md"), encoding="utf-8").read()
    for v in analyze.STANCES + analyze.TONES + analyze.SE_STANCES + ["instructor_sets", "not_stated"]:
        assert f"`{v}`" in book, v


def test_stance_and_tone_quotes_appear_in_raw_text():
    """Each stance and tone quote is found word for word in that institution's raw excerpt."""
    for r in rows("coded.csv"):
        text = raw(r["id"])
        for col in ["stance_quote", "tone_quote"]:
            assert r[col] and r[col] in text, (r["id"], col)


def test_collab_yes_has_quote_in_raw_text():
    """Every ai_collaboration = yes label cites a partner-style quote found in the raw text."""
    for r in rows("coded.csv"):
        if r["ai_collaboration"] == "yes":
            assert r["collab_quote"] and r["collab_quote"] in raw(r["id"]), r["id"]


def test_se_quotes_appear_in_raw_text():
    """Each SE course stance quote is found word for word in that course's raw excerpt."""
    for r in rows("se_coded.csv"):
        assert r["stance_quote"] in raw(r["id"]), r["id"]


def test_findings_counts_equal_csv(findings):
    """Dashboard stance, tone and collaboration counts equal a direct count of coded.csv."""
    coded = rows("coded.csv")
    for key, col in [("stance", "stance"), ("tone", "tone"), ("collaboration", "ai_collaboration")]:
        got = {d["label"]: d["n"] for d in findings[key]}
        want = Counter(r[col] for r in coded)
        assert {k: v for k, v in got.items() if v} == dict(want), key


def test_findings_totals_equal_sample(findings):
    """Every chart's bars add up to the sample size (nothing dropped or double counted)."""
    n = findings["n_institutions"]
    for key in ["stance", "tone", "collaboration", "disclosure", "level", "inst_type"]:
        assert sum(d["n"] for d in findings[key]) == n, key
    assert sum(d["n"] for d in findings["se_stance"]) == findings["n_se_courses"]


def test_stance_by_level_adds_up(findings):
    """Stance-by-level cross tab sums back to the overall stance counts."""
    for i, s in enumerate(findings["stance"]):
        assert sum(findings["stance_by_level"][lv][i]["n"] for lv in findings["stance_by_level"]) == s["n"]


def test_kappa_perfect_agreement():
    """cohen_kappa returns 1.0 when two coders agree on everything."""
    assert analyze.cohen_kappa(["a", "b", "a"], ["a", "b", "a"]) == 1.0


def test_kappa_known_value():
    """cohen_kappa matches a hand-computed example (po=0.5, pe=0.5 gives kappa 0)."""
    assert analyze.cohen_kappa(["a", "a", "b", "b"], ["a", "b", "a", "b"]) == pytest.approx(0.0)


def test_kappa_textbook_example():
    """cohen_kappa matches the standard 50-item example (20+15 agree, kappa = 0.4)."""
    a = ["y"] * 25 + ["n"] * 25
    b = ["y"] * 20 + ["n"] * 5 + ["y"] * 10 + ["n"] * 15
    assert analyze.cohen_kappa(a, b) == pytest.approx(0.4)


def test_keyword_rule_ignores_header():
    """Keyword rule reads only excerpt lines, so words in a URL or title cannot trigger it."""
    text = "URL: https://x.edu/no-single-policy\nEXCERPTS:\n- Students may use it.\n"
    assert analyze.keyword_stance(text) == "permitted_with_conditions"


def test_keyword_kappa_reported(findings):
    """Keyword-vs-Claude agreement is computed and every disagreement is listed."""
    v = findings["validity"]["keyword_vs_claude"]
    assert v["kappa"] is not None
    assert v["n"] - v["agree"] == len(v["disagreements"])


def test_human_sample_status(findings):
    """Human blind-label check: 10 rows exist; if filled, kappa is computed (pending is reported, not faked)."""
    h = findings["validity"]["human_vs_claude"]
    assert h["sample_size"] == 10
    assert h["status"] in {"pending", "partial", "complete"}
    if h["status"] == "pending":
        pytest.skip("human_labels.csv not filled yet: Abhishek's 10-row blind labeling is pending")
    assert h["stance"]["kappa"] is not None
