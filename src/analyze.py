"""Phase 3: turn the coded data into docs/data/findings.json for the dashboard.

Reads data/policies.csv, data/coded.csv, data/se_courses.csv, data/se_coded.csv,
data/blind_labels.csv and the raw excerpts. Computes counts, cross tabs, a
keyword-rule stance classifier, and Cohen's kappa for (a) keyword rule vs Claude
and (b) a blind second coder (fresh Claude session that never saw coded.csv) vs the main labels.

Usage: python src/analyze.py
"""
import csv
import json
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "docs", "data", "findings.json")

STANCES = ["prohibited_by_default", "instructor_decides", "permitted_with_conditions", "encouraged"]
TONES = ["positive", "balanced", "cautious"]
SE_STANCES = ["prohibited", "limited", "permitted", "integrated"]

# First matching group wins (order is part of the rule, see codebook.md).
KEYWORD_RULES = [
    ("prohibited_by_default", ["if and only if", "unless expressly permitted", "disallowed by default",
                               "only with the explicit permission", "only allowed when expressly permitted",
                               "when course policies explicitly permit"]),
    ("encouraged", ["encouraged to learn", "explore and use", "integrate generative ai into the curriculum",
                    "teaching students how to program with large language models"]),
    ("instructor_decides", ["no single", "no institute-wide", "vary from course to course",
                            "varies from course to course", "authority over courses", "full agency",
                            "instructors may determine", "have the ability to determine", "define what is",
                            "faculty members can provide"]),
]


def read_csv(name):
    with open(os.path.join(DATA, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def raw_text(id_):
    with open(os.path.join(DATA, "raw", id_ + ".txt"), encoding="utf-8") as f:
        return f.read()


def excerpts(text):
    """Only the excerpt lines, not the header (so URLs never trigger a rule)."""
    return text.split("EXCERPTS:", 1)[1] if "EXCERPTS:" in text else text


def keyword_stance(text):
    t = re.sub(r"\s+", " ", excerpts(text).lower())
    for label, phrases in KEYWORD_RULES:
        if any(p in t for p in phrases):
            return label
    return "permitted_with_conditions"


def cohen_kappa(a, b):
    """Cohen's kappa for two equal-length label lists. Returns None if undefined."""
    if not a or len(a) != len(b):
        return None
    n = len(a)
    labels = sorted(set(a) | set(b))
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[l] / n) * (cb[l] / n) for l in labels)
    if pe == 1:
        return 1.0 if po == 1 else None
    return (po - pe) / (1 - pe)


def ordered_counts(values, order):
    c = Counter(values)
    return [{"label": k, "n": c.get(k, 0)} for k in order]


def build():
    pol = {r["id"]: r for r in read_csv("policies.csv")}
    coded = read_csv("coded.csv")
    se = {r["id"]: r for r in read_csv("se_courses.csv")}
    se_coded = read_csv("se_coded.csv")
    blind = read_csv("blind_labels.csv")

    rows = []
    for c in coded:
        p = pol[c["id"]]
        rows.append({**p, **c, "keyword_stance": keyword_stance(raw_text(c["id"]))})

    # Keyword rule vs Claude
    kw_kappa = cohen_kappa([r["stance"] for r in rows], [r["keyword_stance"] for r in rows])
    kw_agree = sum(r["stance"] == r["keyword_stance"] for r in rows)
    disagreements = [{"id": r["id"], "institution": r["institution"], "claude": r["stance"],
                      "keyword": r["keyword_stance"]} for r in rows if r["stance"] != r["keyword_stance"]]

    # Blind second coder vs main labels (only rows that are filled)
    by_id = {r["id"]: r for r in rows}
    blind_result = {}
    for field in ["stance", "tone", "ai_collaboration"]:
        pairs = [(by_id[h["id"]][field], h[field].strip()) for h in blind if h[field].strip()]
        blind_result[field] = {
            "n": len(pairs),
            "agree": sum(a == b for a, b in pairs),
            "kappa": cohen_kappa([a for a, _ in pairs], [b for _, b in pairs]) if pairs else None,
        }
    blind_status = "complete" if all(v["n"] == len(blind) for v in blind_result.values()) else (
        "pending" if all(v["n"] == 0 for v in blind_result.values()) else "partial")
    blind_disagreements = [{"id": h["id"], "field": f, "main": by_id[h["id"]][f], "blind": h[f]}
                           for h in blind for f in ["stance", "tone", "ai_collaboration"]
                           if h[f].strip() and h[f] != by_id[h["id"]][f]]

    se_rows = [{**se[s["id"]], **s} for s in se_coded]

    findings = {
        "generated_by": "src/analyze.py",
        "n_institutions": len(rows),
        "n_se_courses": len(se_rows),
        "stance": ordered_counts([r["stance"] for r in rows], STANCES),
        "tone": ordered_counts([r["tone"] for r in rows], TONES),
        "collaboration": ordered_counts([r["ai_collaboration"] for r in rows], ["yes", "no"]),
        "disclosure": ordered_counts([r["disclosure"] for r in rows], ["required", "instructor_sets", "not_stated"]),
        "level": ordered_counts([r["level"] for r in rows], ["department", "college", "university"]),
        "inst_type": ordered_counts([r["inst_type"] for r in rows], ["private_r1", "public_r1", "other"]),
        "stance_by_level": {lv: ordered_counts([r["stance"] for r in rows if r["level"] == lv], STANCES)
                            for lv in ["department", "college", "university"]},
        "tone_by_level": {lv: ordered_counts([r["tone"] for r in rows if r["level"] == lv], TONES)
                          for lv in ["department", "college", "university"]},
        "se_stance": ordered_counts([s["stance"] for s in se_rows], SE_STANCES),
        "se_learning_goal": ordered_counts([s["ai_as_learning_goal"] for s in se_rows], ["yes", "no"]),
        "validity": {
            "keyword_vs_claude": {"n": len(rows), "agree": kw_agree, "kappa": kw_kappa,
                                  "disagreements": disagreements},
            "blind_vs_claude": {"status": blind_status, "sample_size": len(blind),
                                "coder": sorted({h["coder"] for h in blind}),
                                "disagreements": blind_disagreements, **blind_result},
        },
        "institutions": rows,
        "se_courses": se_rows,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=1, ensure_ascii=False)
    # .js twin so the page also works when opened straight from disk (file://)
    with open(OUT[:-5] + ".js", "w", encoding="utf-8") as f:
        f.write("window.DATA_FINDINGS = " + json.dumps(findings, ensure_ascii=False) + ";\n")
    return findings


if __name__ == "__main__":
    f = build()
    v = f["validity"]["keyword_vs_claude"]
    print(f"{f['n_institutions']} institutions, {f['n_se_courses']} SE courses")
    print("stance:", {d['label']: d['n'] for d in f["stance"]})
    print("tone:", {d['label']: d['n'] for d in f["tone"]})
    print("collaboration:", {d['label']: d['n'] for d in f["collaboration"]})
    print(f"keyword vs Claude: {v['agree']}/{v['n']} agree, kappa={v['kappa']:.3f}")
    b = f["validity"]["blind_vs_claude"]
    print("blind coder vs Claude:", b["status"], {k: (b[k]["agree"], b[k]["n"], b[k]["kappa"]) for k in ["stance", "tone", "ai_collaboration"]})
