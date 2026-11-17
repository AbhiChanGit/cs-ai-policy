# How US CS departments talk about generative AI

Project 2 for Generative AI for Software Development (Dr. Jillian Aurisano), University of Cincinnati.
Built with **agentic development** in Claude Code: the agent wrote the code; the human set goals and reviewed specs, tests and outputs.

## Pages

| Page | What it shows |
|---|---|
| [Findings dashboard](docs/index.html) | Stance, tone, AI-as-collaborator framing and disclosure across 26 institutions; 8 software engineering syllabi; searchable sources with the quote behind every label |
| [Validation explorer](docs/tests.html) | Every test run (including a deliberate negative control), searchable and filterable, with what each test proves |
| [Timeline and contributions](docs/timeline.html) | Timestamped log of every step, who did it (Human or Claude), and every human request with Claude's response |
| [Token usage](docs/tokens.html) | Tokens per call and per phase from Claude Code transcripts, context growth, and the estimated effect of /clear |

On GitHub Pages: Settings, Pages, deploy from branch `main`, folder `/docs`. Locally: open `docs/index.html` directly (data ships as `.js` files, so no server is needed).

## Repository map

```
SPEC.md          goals, research questions, method, phase acceptance criteria (source of truth)
CLAUDE.md        rules every Claude session follows
PROGRESS.md      append-only timestamped log (src/log.py)
PROMPTS.md       human requests and Claude responses
REVIEW.md        how the work was checked; human review section
EVALUATION.md    goal-by-goal evaluation; reflection (written by the student)
data/            sources (policies.csv, se_courses.csv), raw excerpts, codebook, labels
src/             analyze.py, run_tests.py, tokens.py, timeline.py, log.py
tests/           pytest suite; conftest.py records each result with its docstring
docs/            the static site and its generated data
```

## Rebuild everything

```
python src/analyze.py
python src/timeline.py
python src/tokens.py
python src/run_tests.py "label for this run"
```

Requires Python 3.10+ and pytest. Standard library only otherwise.
