# SPEC: How US CS departments talk about generative AI

Course: Generative AI for Software Development (Dr. Jillian Aurisano), Project 2.
Development mode: agentic. Claude Code writes the code; Abhishek sets goals, reviews specs, tests and outputs.

## Research questions

- RQ1. How are students permitted (or encouraged) to use genAI in CS courses?
- RQ2. How do CS departments talk about AI in official publications? Is the tone positive?
- RQ3. Do they discuss collaboration with AI (AI as a partner, pair programmer, tutor)?
- RQ4. How are software engineering courses handling AI?

## Approach (analysis method)

Qualitative content analysis with a fixed codebook (`data/codebook.md`).
1. Sample: 25 to 30 US institutions, mixed by type (private R1, public R1, other). For each, the most official AI statement that applies to CS students (department page first, then college, then university), plus SE course policies where a public syllabus exists.
2. Each source is saved as an excerpt with URL and access date (`data/raw/*.txt`), so every label can be traced to text.
3. Claude labels each source against the codebook (`data/coded.csv`), quoting the sentence that justified each label.
4. Validity checks: (a) a transparent keyword rule labels stance independently and agreement with Claude is reported as Cohen's kappa; (b) Abhishek labels a 10 row blind sample (`data/human_labels.csv`) and kappa is reported when filled.
5. Aggregates feed the dashboard. No number on any page is typed by hand.

## Phases and acceptance criteria

### P1 Setup
- [x] Repo, CLAUDE.md, SPEC.md, PROGRESS.md, PROMPTS.md exist.
- [x] Every later phase appends a timestamped PROGRESS entry.

### P2 Data collection
- [ ] >= 25 institutions in `data/policies.csv`, >= 8 SE courses in `data/se_courses.csv`.
- [ ] Every row has a URL, access date, level (department / college / university / course) and an excerpt file that exists and is non empty.

### P3 Analysis
- [ ] `data/codebook.md` defines every label with a decision rule.
- [ ] `data/coded.csv` labels every institution; every label value is in the codebook.
- [ ] `src/analyze.py` writes `docs/data/findings.json`; keyword rule vs Claude kappa computed; human kappa computed when `human_labels.csv` is filled, otherwise reported as pending.

### P4 Findings dashboard (`docs/index.html`)
- [ ] Charts for stance, tone, collaboration framing, policy level, SE course handling; searchable source table with quotes and links.
- [ ] Every chart reads `findings.json`; test proves chart totals equal CSV counts.

### P5 Validation explorer (`docs/tests.html`)
- [ ] pytest results exported to `docs/data/tests.json` with id, phase, file, docstring (what it checks), status, duration.
- [ ] Search box, filters by phase and status, run history.
- [ ] Manual review log (`REVIEW.md`) shown on the page.

### P6 Timeline and contributions (`docs/timeline.html`)
- [ ] Built from PROGRESS.md and PROMPTS.md. Each entry shows timestamp, phase, actor (human / Claude), summary.

### P7 Token usage (`docs/tokens.html`)
- [ ] Parsed from Claude Code transcripts (`~/.claude/projects/*/*.jsonl`): input, cache write, cache read, output per message.
- [ ] Totals per phase (phase windows from PROGRESS.md) and per session; compaction events marked.

### P8 Publish
- [ ] `docs/` works as a static site (GitHub Pages, `/docs` folder). README links every page.

### P9 Evaluation
- [ ] `EVALUATION.md`: goal by goal check with evidence. Reflection section written by Abhishek.

### P10 Presentation
- [ ] 8 to 10 slide deck with speaker notes.
