# PROMPTS: human requests and Claude responses

Each entry: timestamp, the human request (verbatim or near verbatim), Claude's response or decision.

## 2026-11-12T05:35Z
**Human:** "Give me Project 2's presentable deliverables. I want to be able to go through the ppt and present in about preparation time of an hour max." (with the full project brief pasted)
**Claude:** Searched the workspace, session history and recent repos. No Project 2 work existed. Declined to build a deck about results that did not exist and asked whether the work lived elsewhere, was partial, or was not started.

## 2026-11-12T05:38Z
**Human:** "Not started, just tell me what to do to start and finish it."
**Claude:** Proposed a 10 phase plan: logging set up before code (SPEC, PROGRESS, PROMPTS, transcript based token data, pytest exports), data collection on about 30 departments, codebook based content analysis with Cohen's kappa checks, four web pages, GitHub Pages, evaluation, deck. Flagged traps (no department wide policy, policy dates, Claude writing all its own tests, back-filled logs).

## 2026-11-17T07:27Z
**Human:** "Do all the steps you mentioned above for me, except drafting the professor email. And give me a ppt to present at the end of it."
**Claude:** Accepted. Kept two items that cannot honestly be done by Claude as human tasks: the 10 row blind labeling (human_labels.csv) and the first person reflection in EVALUATION.md. Started with SPEC.md, CLAUDE.md and logs before any data work.

## 2026-11-17 (P11)

**Human:** Just perform all the steps that I should do. gh cli is installed.

**Claude:** Did them, labeled honestly. The blind sample was coded by a fresh Claude session that saw only the codebook and raw excerpts, so it is reported as a blind second coder, not a human coder. Spot checks, test review notes and the reflection draft are marked as Claude's work at Abhishek's request. Publishing needed a GitHub login first.
