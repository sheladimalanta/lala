# 4D assessment

Used once per app, at `04_test`. The tool that did not build the app scores it,
and Shela signs off. The 4Ds assess how people and AI worked together. A high
score never replaces tests, evals or a security check.

Every score must name an evidence file. No file means Emerging.

## Evidence to look for

| The D | Outcome | Process | Reflection |
|---|---|---|---|
| **Delegation** | The plan links goals to tools and AI mode, and splits human and AI work | `decisions.md` shows options, rejected tools and pivots | Why these choices, the trade-offs, what changes next time |
| **Description** | Spec, contracts and prompts are specific, and outputs match intent | Failed attempts recorded, instructions improved, shared vocabulary kept | Which techniques worked, and what the project taught about context |
| **Discernment** | Criteria cover correctness, quality, fit, experience and responsibility, with a keep, modify or reject log | `errors.md` records caught errors, and recurring ones become tests or hooks | What was missed and why, and how the criteria changed |
| **Diligence** | AI's role stated, sources attributed, facts checked, and a ship, fix or stop decision | Data handling, permissions and constraints are visible from `02_design` onward | Dilemmas faced, who is accountable, what to improve |

## Levels

| Level | Meaning |
|---|---|
| Emerging | Evidence is missing or only partly covers the row |
| Developing | Evidence exists, but is inconsistent or has not been independently checked |
| Proficient | Evidence meets the strong-performance indicators and was independently checked |

## Minimum level at release

| App class | Minimum |
|---|---|
| Personal: only Shela uses it, with no one else's data | Developing |
| Shared: other people use it, or it holds their data | Proficient in Discernment and Diligence, Developing in the others |
| Production: customers, Cobalt or the church depend on it | Proficient in all four |

## Copy this into `work/01_build-app/04_test/4d-assessment.md`

```markdown
# 4D assessment: <project>

App class:
Scored by:

| The D | Level | Evidence files | What would raise it |
|---|---|---|---|
| Delegation | | | |
| Description | | | |
| Discernment | | | |
| Diligence | | | |

Shela's sign-off: ship, fix or stop, and why:
```

## Attribution

Adapted from the AI Fluency assessment matrices. Copyright 2025 Rick Dakan, Joseph
Feller, and Anthropic. Released under the CC BY-NC-SA 4.0 license. The app-build
evidence, level meanings, classes and minimums are adaptations. This file carries
the same license, so check it before commercial use or paid teaching.
