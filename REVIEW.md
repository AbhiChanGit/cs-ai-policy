# Review log

How the code and data were checked, beyond "Claude wrote tests and they passed".

## Checks Claude ran (2026-11-17)

- **Negative control.** Corrupted one quote (University of Cincinnati) and one label (Stony Brook) on purpose and reran the suite. 4 tests failed, each in the place expected: label vocabulary, quote traceability, count equality and chart totals. Data restored, suite green. Both runs are in the run history below, so the failing run is visible, not hidden.
- **Kappa function checked against hand-computed values**: perfect agreement (1.0), chance agreement (0.0), and the standard 50 item example (0.4).
- **Keyword rule not tuned after seeing disagreements.** It agrees with Claude on 21 of 26 stance labels; the 5 disagreements are listed on the Findings page. Tuning it to agree would make the check meaningless.
- **Numbers on pages are computed.** A test recounts coded.csv directly and compares with what the dashboard shows. The findings text is generated from the same JSON, not typed.
- **A bug Claude introduced and caught.** A scripted edit put a literal newline inside a Python string in four builder scripts (SyntaxError). Fixed with exact edits; logged in PROGRESS.md.
- **Typed number corrected.** A PROGRESS line written from memory said 7/4/15 for the level split; a script count showed 8/4/14. A correction line was appended rather than editing history.

## Human review (Abhishek, pending)

Fill in when done. Suggested three tests to read line by line:

- `tests/test_analysis.py::test_stance_and_tone_quotes_appear_in_raw_text`: does it really prove each label is backed by real text?
- `tests/test_analysis.py::test_findings_counts_equal_csv`: does it recount independently of analyze.py?
- `tests/test_data.py::test_no_orphan_raw_files`: could a source be collected and silently dropped?

Spot check 5 sources: open the URL, find the quoted sentence, note match or mismatch here.
