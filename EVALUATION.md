# Evaluation

The brief says the evaluation is completed primarily by the student, with Claude supplying the information. Part A is that information (Claude compiled it, with evidence). Part B was drafted by Claude on 2026-11-17 at Abhishek's request, from the logged facts, for Abhishek to review and rewrite in his own words.

## Part A: goal by goal (evidence compiled by Claude)

| Goal from the brief | Status | Evidence |
|---|---|---|
| Gather data on how CS students may use genAI | Met, with limits | 26 institutions, 8 SE syllabi, `data/policies.csv`, `data/raw/` (URL and access date on every source) |
| How departments talk about AI; positive take? | Met | Tone coded for all 26: 9 positive, 13 balanced, 4 cautious. Departments far more positive (5 of 8) than universities (2 of 14). Soft: tone had the lowest blind agreement (5 of 10) |
| Do they discuss collaboration with AI? | Met | 8 of 26 use partner, tutor, colleague or pair-programming language; quotes shown on the dashboard |
| How SE courses handle AI | Met, small sample | 8 syllabi: none ban AI outright, 3 integrate or require it, 4 name AI skill as a course goal |
| Dashboard | Met | `docs/index.html`; every number generated from data, test checks counts equal the CSV |
| Identify an analysis approach | Met | Codebook-based content analysis with quote traceability and kappa checks (`data/codebook.md`) |
| Agentic, spec-driven development | Met, one gap | SPEC.md and CLAUDE.md drive the work. Gap: no /clear was used; the build ran in one session (visible on the token page) |
| Validation interface | Met | `docs/tests.html`: 43 tests, 6+ runs, negative control, review log |
| Contribution documentation with timestamps | Met | `docs/timeline.html` from append-only PROGRESS.md and PROMPTS.md |
| Token usage interface | Met | `docs/tokens.html` from Claude Code transcripts; /clear effect estimated |
| Publish on GitHub and the web | Met | GitHub repo with Pages serving `docs/` (links in README) |

### Weaknesses a reviewer will raise

- Sample is a convenience sample of 26, mostly research universities, so the percentages describe this sample, not the US.
- Sources are uneven: formal policies, guidance pages and news stories, dated 2023 to 2026.
- No human coder. The keyword rule (kappa 0.725) and a blind Claude second coder (stance 10 of 10, collaboration 9 of 10, tone 5 of 10) test consistency and codebook clarity, not agreement with human judgment.
- Excerpts are trimmed sentences: a live check of 8 sources found 7 exact and 1 (Stony Brook) that dropped a second condition.
- Token phases are approximate: calls are attributed to the next log line, and several phases were logged close together.

## Part B: evaluation and reflection (Claude draft for Abhishek to review)

### My evaluation

The project answers the four questions for this sample. The clearest result is structural: half of the 26 sources hand the decision to each instructor, and the only sources that encourage AI use are department pages, never a university page. The collaboration question has a clear answer too: about a third of sources describe AI as a partner or tutor, and none of the 8 software engineering syllabi ban it, with 3 building it into the course.

The weakest part is tone. A blind second coder agreed on stance for every row but on tone for only half, so I would not lean on the claim that departments sound more positive than universities. The sample is also a convenience sample of mostly research universities, so the percentages describe these 26 sources, not US computer science as a whole. With another week I would double the sample, add community colleges and teaching focused schools, tighten the tone definitions with examples, and get a classmate to code the same 10 rows.

### Reflection: agentic vs AI assisted development

In Project 1 I used AI as an assistant: I wrote and ran the code and asked for help on pieces. In Project 2 I wrote no code. I set the goal, approved the plan, and then judged the work through the spec, the tests, the logs and the pages, not by reading every line.

Where I trusted the agent, the trust came from checks I could see rather than from the agent's confidence. Every label cites a quote, and a test fails if the quote is not in the saved source. The deliberate negative control showed the tests can fail. The agent also corrected itself in the log: it typed a wrong count from memory, appended a correction instead of editing history, and logged its own syntax bug. That is what made the trust reasonable.

The spec files and tests gave me a level of review I could not get by reading code: a list of claims about the output that are rechecked on every run. What I lost is the detail those tests do not cover. The live spot check found that one saved excerpt had cut a sentence short and dropped a condition, and every test still passed. If I had collected that source myself, I would probably have noticed. Agentic development moves the risk from writing bugs to not knowing which checks are missing.

Cost is the other lesson. Project 2 used more than 20 times the tokens of Project 1, almost all of it cache reads, because the whole build ran in one long session without /clear. The token page estimates how much a /clear at each phase change would have saved.

For my next project I would use agentic development for the broad build (data collection, pages, tests) and stay hands on for the parts that carry the judgment: the codebook, a human coded sample, and a direct look at sources. I would also start a fresh session per phase from the start.
