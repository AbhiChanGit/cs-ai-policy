# Evaluation

The brief says the evaluation is completed primarily by the student, with Claude supplying the information. Part A is that information (Claude compiled it, with evidence). Part B is for Abhishek to write.

## Part A: goal by goal (evidence compiled by Claude)

| Goal from the brief | Status | Evidence |
|---|---|---|
| Gather data on how CS students may use genAI | Met, with limits | 26 institutions, 8 SE syllabi, `data/policies.csv`, `data/raw/` (URL and access date on every source) |
| How departments talk about AI; positive take? | Met | Tone coded for all 26: 9 positive, 13 balanced, 4 cautious. Departments far more positive (5 of 8) than universities (2 of 14) |
| Do they discuss collaboration with AI? | Met | 8 of 26 use partner, tutor, colleague or pair-programming language; quotes shown on the dashboard |
| How SE courses handle AI | Met, small sample | 8 syllabi: none ban AI outright, 3 integrate or require it, 4 name AI skill as a course goal |
| Dashboard | Met | `docs/index.html`; every number generated from data, test checks counts equal the CSV |
| Identify an analysis approach | Met | Codebook-based content analysis with quote traceability and kappa checks (`data/codebook.md`) |
| Agentic, spec-driven development | Met, one gap | SPEC.md and CLAUDE.md drive the work. Gap: no /clear was used; the build ran in one session (visible on the token page) |
| Validation interface | Met | `docs/tests.html`: 43 tests, 6+ runs, negative control, review log |
| Contribution documentation with timestamps | Met | `docs/timeline.html` from append-only PROGRESS.md and PROMPTS.md |
| Token usage interface | Met | `docs/tokens.html` from Claude Code transcripts; /clear effect estimated |
| Publish on GitHub and the web | Pending | Repo committed locally; push and enable Pages (commands in the handoff) |

### Weaknesses a reviewer will raise

- Sample is a convenience sample of 26, mostly research universities, so the percentages describe this sample, not the US.
- Sources are uneven: formal policies, guidance pages and news stories, dated 2023 to 2026.
- One coder. Keyword-rule kappa (0.725) checks consistency, not independent judgment. The human blind sample is still empty.
- Excerpts came through a fetch tool; 5 URL spot checks are pending.
- Token phases are approximate: calls are attributed to the next log line, and several phases were logged close together.

## Part B: written by Abhishek

### My evaluation

(Your judgment: did the project answer the four questions well enough? What would you change with another week?)

### Reflection: agentic vs AI-assisted development

Facts you can draw on:
- Project 1 (Cincy311) session on disk: 14 calls, peak context 66k. Project 2: see the token page.
- In Project 2 you wrote no code. Your interventions are listed on the timeline page.
- Claude refused to fabricate a deck at the start, introduced and fixed its own bug, and corrected a number it typed from memory.

Questions to answer in your own words:
1. Where did you trust the agent, and what made that trust reasonable (or not)?
2. What did spec files and tests give you that reading the code would not?
3. What did you lose by not writing or reading the code?
4. Would you choose agentic or AI-assisted for your next project, and why?
