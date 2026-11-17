# Review log

How the code and data were checked, beyond "Claude wrote tests and they passed".

## Checks Claude ran (2026-11-17)

- **Negative control.** Corrupted one quote (University of Cincinnati) and one label (Stony Brook) on purpose and reran the suite. 4 tests failed, each in the place expected: label vocabulary, quote traceability, count equality and chart totals. Data restored, suite green. Both runs are in the run history below, so the failing run is visible, not hidden.
- **Kappa function checked against hand-computed values**: perfect agreement (1.0), chance agreement (0.0), and the standard 50 item example (0.4).
- **Keyword rule not tuned after seeing disagreements.** It agrees with Claude on 21 of 26 stance labels; the 5 disagreements are listed on the Findings page. Tuning it to agree would make the check meaningless.
- **Numbers on pages are computed.** A test recounts coded.csv directly and compares with what the dashboard shows. The findings text is generated from the same JSON, not typed.
- **A bug Claude introduced and caught.** A scripted edit put a literal newline inside a Python string in four builder scripts (SyntaxError). Fixed with exact edits; logged in PROGRESS.md.
- **Typed number corrected.** A PROGRESS line written from memory said 7/4/15 for the level split; a script count showed 8/4/14. A correction line was appended rather than editing history.

## Delegated review (done by Claude on 2026-11-17 at Abhishek's request)

Abhishek asked Claude to carry out the review steps originally planned for him. They are recorded here as Claude's work, not as human review.

### Live source spot check

Method: fetch each URL, strip HTML, normalize whitespace and quote marks, then test whether each cited quote appears in the live page.

| Source | Result |
|---|---|
| Stony Brook CS | Mismatch in form, not in label. The live sentence continues: "if and only if the instructor permits it in writing, and with prior written approval of the Undergraduate Program Director (UPD)." The saved excerpt cut it at "writing." and so dropped a second condition. The tone quote was trimmed the same way. The label (prohibited by default) still holds, and is if anything strengthened. |
| BYU Idaho CS | All quotes match |
| Stanford | All quotes match |
| Dartmouth | All quotes match |
| UIUC Grainger | All quotes match |
| Carnegie Mellon | All quotes match |
| University of Cincinnati | All quotes match |
| Georgia Tech CoC | All quotes match |

Lesson: the quote test proves a quote is in the saved excerpt, not that the excerpt is a faithful copy of the page. Excerpts were saved as trimmed sentences, so a qualifier can be lost. 7 of 8 sources matched word for word.

### Blind second coder

A fresh Claude session received only `data/codebook.md` and the 10 raw excerpt files and was told not to open the labels. Results are on the dashboard: stance agreed on every row, AI collaboration on 9 of 10, tone on only 5 of 10. Tone is the least reliable code: the boundary between "balanced" and "positive" or "cautious" is a judgment call the codebook does not pin down. Findings that rest on tone should be read as soft.

### Three tests read line by line

- `test_stance_and_tone_quotes_appear_in_raw_text`: checks a plain substring match against the saved excerpt. It proves no quote was invented relative to the excerpt. It does not prove the excerpt matches the live page (see the Stony Brook case above).
- `test_findings_counts_equal_csv`: recounts `coded.csv` with `collections.Counter`, independent of the `ordered_counts` helper in analyze.py. A label value missing from the allowed list would be dropped by analyze.py and make this test fail, which is the right behavior.
- `test_no_orphan_raw_files`: catches a source that was saved and then dropped from the CSV. It cannot catch a source that was fetched and never saved (UMich and Swarthmore were dropped that way); those drops are recorded only in PROGRESS.md.
