# Codebook

Unit of analysis: one official source per institution (the most specific level available for CS students: department, then college, then university). Labels describe what the source text says, not what individual courses do.

Each label in `coded.csv` cites a quote that appears word for word in `data/raw/<id>.txt`.

## stance (RQ1): the default for student use of genAI in coursework

| Value | Decision rule |
|---|---|
| `prohibited_by_default` | Text says use is not allowed unless an instructor explicitly permits it. |
| `instructor_decides` | Text gives no default; it hands the decision to each instructor (often with templates or tiers). |
| `permitted_with_conditions` | Text allows some student use by default, with limits (disclosure, no full deliverables, level of course). |
| `encouraged` | Text explicitly encourages students to use or learn genAI, or says it is integrated into the curriculum. |

Tie-break: if text has both a default and instructor override, code the default.

## tone (RQ2): how the source talks about AI

| Value | Decision rule |
|---|---|
| `positive` | Benefits, opportunity or career need dominate; risks appear only as caveats. |
| `balanced` | Benefits and risks both stated with similar weight, or the text is procedural and neutral. |
| `cautious` | Risks, integrity or limits dominate; benefits absent or minor. |

## ai_collaboration (RQ3): does the source frame AI as a collaborator?

| Value | Decision rule |
|---|---|
| `yes` | AI is described, approvingly, with a partner word: partner, collaborator, colleague, coach, tutor, pair programming, assistant (as a role). |
| `no` | AI is described only as a tool, resource or risk, or a partner word is used only to forbid (for example, "AI tutors are not allowed"). |

## disclosure (RQ1 detail)

| Value | Decision rule |
|---|---|
| `required` | Text states, as a general rule, that students must disclose, cite or attribute AI use. |
| `instructor_sets` | Disclosure appears only as an option, tier or sample syllabus statement. |
| `not_stated` | The source does not address disclosure. |

## SE course codes (RQ4, `se_coded.csv`)

| Field | Values |
|---|---|
| `stance` | `prohibited`, `limited` (reference only or marked parts only), `permitted` (allowed with conditions), `integrated` (required or taught as a course skill) |
| `disclosure` | `required`, `not_stated` |
| `ai_as_learning_goal` | `yes` if the syllabus names learning to use AI well as a course goal, else `no` |

## Keyword rule (validity check, `src/analyze.py`)

A transparent regex classifier labels `stance` from the raw text with no judgment. Order matters; first match wins:
1. `prohibited_by_default`: "if and only if", "unless expressly permitted", "disallowed by default", "only with the explicit permission", "only allowed when expressly permitted", "when course policies explicitly permit"
2. `encouraged`: "encouraged to learn", "explore and use", "integrate generative ai into the curriculum", "teaching students how to program with large language models"
3. `instructor_decides`: "no single", "no institute-wide", "vary from course to course", "varies from course to course", "authority over courses", "full agency", "instructors may determine", "have the ability to determine", "define what is", "faculty members can provide"
4. otherwise `permitted_with_conditions`

Agreement between the keyword rule and Claude's labels is reported as Cohen's kappa. Disagreements are listed, not hidden: they show where judgment was needed.
