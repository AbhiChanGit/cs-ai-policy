# PROGRESS log

Format: `- <UTC timestamp> | <phase> | <actor> | <summary>`. Appended by `src/log.py`, never edited.
The first four lines were reconstructed from the Claude Code transcript timestamps (session eac7ade5) because logging started after them.

- 2026-11-12T05:35:09Z | P0 | Human | Asked for presentable Project 2 deliverables (deck preparable in 1 hour).
- 2026-11-12T05:36:32Z | P0 | Claude | Searched disk and session history; found no Project 2 work; refused to fabricate results and asked where the work was.
- 2026-11-12T05:38:08Z | P0 | Human | Confirmed project not started; asked for a start to finish plan.
- 2026-11-12T05:38:49Z | P0 | Claude | Wrote 10 phase plan (spec, logs, data, coding with kappa, 4 web pages, publish, evaluation, deck) and saved it to course memory.
- 2026-11-17T07:27:00Z | P0 | Human | Delegated all phases to Claude (except professor email) and asked for a final deck.
- 2026-11-17T07:28:39Z | P1 | Claude | Created repo, SPEC.md (RQs, method, phase acceptance criteria), CLAUDE.md (session rules), PROGRESS.md, PROMPTS.md, src/log.py. Installed pytest 9.2.0.
- 2026-11-17T07:37:40Z | P2 | Claude | Collected 26 institutional sources (7 department, 4 college, 15 university level) and 8 SE course syllabi via WebSearch+WebFetch; 4 fetches failed (403/404: UIUC VPAA, UMich x2, Swarthmore) and were replaced or dropped. Excerpts in data/raw, tables in data/policies.csv and data/se_courses.csv.
- 2026-11-17T07:37:46Z | P2 | Claude | Correction to previous line: level split is 8 department, 4 college, 14 university (counted from policies.csv; earlier line was typed from memory, which is why numbers must come from scripts).
- 2026-11-17T07:38:59Z | P3 | Claude | Wrote codebook (4 fields + SE fields + keyword rule), labeled 26 institutions and 8 SE courses with a cited quote per label, wrote src/analyze.py. Keyword rule vs Claude stance: 21/26 agree, kappa 0.725 (5 disagreements kept and shown). Human 10-row blind sample template created (data/human_labels.csv), status pending.
- 2026-11-17T07:38:59Z | P3 | Claude | Decision: did NOT tune the keyword rule after seeing disagreements, because tuning it to match would make the agreement check meaningless.
- 2026-11-17T07:40:12Z | P5 | Claude | Negative control: corrupted one quote (UC) and one label (Stony Brook) on purpose; 4 tests failed exactly where expected (label vocabulary, quote traceability, count equality, totals). Restored data; suite back to 25 pass, 1 skip (human labels pending). Both runs kept in reports/history.json.
- 2026-11-17T07:41:51Z | P5 | Claude | Built src/run_tests.py (pytest -> reports/history.json -> docs/data/tests.json), src/tokens.py, src/timeline.py. Bug found and fixed: my scripted edit wrote a literal newline into a Python string in 4 builders (SyntaxError); fixed with exact edits, suite green again.
- 2026-11-17T07:45:24Z | P4 | Claude | Built docs/index.html findings dashboard (tiles, generated key findings, 8 charts, searchable source table, validity panel).
- 2026-11-17T07:45:24Z | P6 | Claude | Built docs/timeline.html from PROGRESS.md and PROMPTS.md, with human-vs-Claude split and the open human task list.
- 2026-11-17T07:45:24Z | P7 | Claude | Built docs/tokens.html: context-per-call line, tokens by phase, /clear estimate, session comparison. Added 17 page/token/timeline tests; a README test failed as expected until README.md was written, then 42 pass.
- 2026-11-17T07:46:17Z | P4 | Claude | Rendered all 4 pages in headless Chrome and inspected screenshots. Bug found: findings bars were empty (inline span ignores width); fixed with display:block in style.css.
- 2026-11-17T07:46:17Z | P9 | Claude | Wrote EVALUATION.md Part A (goal-by-goal evidence table and known weaknesses). Part B (evaluation and reflection) left for Abhishek with facts and guiding questions.
- 2026-11-17T07:46:20Z | P8 | Claude | Initial git commit of the full repo (local). Push to GitHub and Pages setup left to Abhishek (gh CLI not installed; needs his account).
- 2026-11-17T07:48:57Z | P10 | Claude | Built Project2_Presentation.pptx (13 slides, speaker notes with a full script and Q&A prep) from the generated JSON, so slide numbers match the pages.
- 2026-11-17T16:34:04Z | P11 | Human | Asked Claude to perform the remaining human tasks (blind sample, spot checks, test review, reflection, publishing).
- 2026-11-17T16:34:04Z | P11 | Claude | Blind second coder (fresh Claude session, codebook and 10 raw files only): stance 10/10, kappa 1.00; collaboration 9/10, kappa 0.80; tone 5/10, kappa 0.26. Renamed human_labels.csv to blind_labels.csv with a coder column; SPEC amended.
- 2026-11-17T16:34:04Z | P11 | Claude | Live spot check of 8 source URLs: 7 match word for word; Stony Brook excerpt trimmed a sentence and dropped a second condition (UPD approval). Label unchanged. Recorded in REVIEW.md with notes on 3 tests.
- 2026-11-17T16:34:04Z | P11 | Claude | Drafted EVALUATION.md Part B for Abhishek to review; timeline tasks now show who did each delegated step.
- 2026-11-17T16:34:11Z | P11 | Claude | Bug: scripted edit of timeline.py dropped the closing bracket of human_tasks (SyntaxError); fixed with Edit.
- 2026-11-17T16:47:34Z | P11 | Claude | Published: public GitHub repo AbhiChanGit/cs-ai-policy, GitHub Pages from main /docs; commit author set to the GitHub noreply address.
