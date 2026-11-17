# CLAUDE.md for cs-ai-policy

Read SPEC.md first. It is the source of truth for scope and acceptance criteria.

Rules for every session:
- Work one phase at a time. Before finishing a phase: run `python src/run_tests.py`, tick SPEC.md boxes, append a PROGRESS.md entry.
- PROGRESS.md entry format (one line, appended, never edited):
  `- <ISO timestamp> | <phase> | <actor: Human or Claude> | <summary>`
- PROMPTS.md: append the human's request and a one or two line summary of Claude's answer or decision.
- Before `/clear` or `/compact`, add a PROGRESS line with `context:` and the action, so the token page can mark it.
- No hand typed numbers on any page. Pages read JSON in `docs/data/` produced by scripts in `src/`.
- Standard library Python only (csv, json, re, xml). No pandas.
- Every label in `data/coded.csv` must cite a quote from the matching `data/raw/<id>.txt`.
