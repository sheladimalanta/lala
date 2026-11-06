# Two workspaces that already run this way

Read before designing a third. Both are the source of the
pattern; this file describes them rather than restating their rules, which live
in their own repos.

| | `~/va-resume-v3` | `~/storytelling` |
|---|---|---|
| Started | 2026-08-08 | 2026-08-09 |
| In → out | one applicant's resume + intake answers → one role-targeted resume package + an honest gap read | true material → a story, sketch, or opening worth reading |
| Layout | per-record | per-lane |
| Records | `applicants/` (gitignored because it contains real people's data) | `pieces/` (tracked) |
| Stages | 01 intake → 02 profile → 03 target-role → 04 gap → 05 draft → 06 package, inside each applicant | three lanes at the root: `01_openers`, `02_character`, `03_story` |
| Authority | its own `_shared/` rules, built from a 48-resume corpus and 60 intake answers | external: Daniel Taylor, *Creating a Spiritual Legacy* |
| Drift check | `_shared/check-rules.py` + `rule-map.json` | none because little internal duplication can drift |
| Ends at | a delivered package; the candidate finishes alone | an approved draft; publishing is a separate step |

## What each one teaches

**va-resume-v3: name the stage that carries the weight.** Its `CONTEXT.md`
argues that stage 03 (choose one target role) matters most, with the evidence:
across 60 intake submissions the median applicant ticks three roles, and only 11
of 60 tick exactly one. For four applicants in five the role is a real decision,
and everything after it is built on that choice. A wrong role wastes the gap
read, the draft, and the package: the expensive-late-failure the structure
exists to prevent. Correction is cheapest at 03, so that is where the loudest
human check goes.

**va-resume-v3: know where the pipeline stops, and let it shape upstream.**
There is deliberately no stage 07 because the candidate finishes the resume
alone. Three consequences run backwards through the whole workspace: every
marker in the draft is an instruction rather than a question, because the
person the question implies does not exist; the answer patterns are the only
guidance she gets, so they must correct a weak answer before it is written; and
the last honest read happens at stage 06.

**storytelling: an external authority beats an internal rulebook.** The craft
law is Taylor's, not the model's, and `_shared/source/CONTEXT.md` exists to
check whether a claim is really his. This is why the workspace needs no drift
checker. Its rules point outward at a book instead of restating each other.

**storytelling: lanes must be genuinely different paths.** Openers, character,
and story are not three stages of one pipeline. A piece enters one lane at a
time and can re-enter later, which is exactly the condition that makes per-lane
correct. Openers additionally runs on existing text only.

**Both: one rule that overrides convenience, stated once.** Each has a section
naming a small number of rules, such as never invent, never save sensitive PII,
and never claim readiness without run and success counts, with a table that
points at the file and says *"Read the file, not this table."*

## The incident that produced the checker

On **2026-08-08**, in va-resume-v3, `_shared/output-format.md` was revised four
times in ninety minutes. The General Admin VA role playbook carried its own copy
of the resume shape and sat stale for nine hours, teaching a format that had
already been ruled out.

Nothing failed. Nothing complained. It was found by accident.

The response was not to delete the duplicate. The playbooks' reference resumes
are the standard a draft gets measured against, so deleting them to save
maintenance would have traded product quality for tidiness. The response was to
declare the duplication in `rule-map.json` and let `check-rules.py` complain
when a dependency moves.

Two dependencies there are deliberately absent and must stay absent:
`_shared/raters/client.md` and `_shared/raters/skeptic.md` derive from nothing. A
rater that tracked the output format would grade against the format and find
nothing. Their blindness is the feature.

## Where the pattern came from

ICM is the Interpretable Context Methodology. As published it is a navigation
scheme: a `Router.md` at the workspace root maps unfamiliar terms to folders,
an `Agents.md` inside each folder carries that folder's rules and persona, and
one model walks the tree adopting whichever context it lands in. Lala's
workspaces rename those to `CLAUDE.md` and `CONTEXT.md` and add what the
published version has no answer for: sequencing, stage outputs, human gates
between stages, and drift tracking.

The per-folder contract and the one-home-per-fact invariant are adapted from
RinDig's `icm-architect` skill. Its restructure mode, which moves and renames
directories, is not used here.

## What the Acme DevRel teaching blueprint adds

The `workspace-blueprint` teaching example uses three heterogeneous workspaces:
writing, production, and community. It is not another production workspace to
copy literally. It demonstrates routing choices that apply before the
per-record or per-lane stage layout is selected.

- `CLAUDE.md` is the always-loaded map: folder tree, global naming and placement
  rules, cross-workspace flow, and quick navigation.
- Root `CONTEXT.md` is the task router. It points at one workspace and names any
  cross-workspace reference needed to enter safely.
- Each workspace `CONTEXT.md` includes an explicit task-level load budget. The
  `Skip these` column is part of the contract because adjacent context can be as
  harmful as missing context.
- Stable knowledge lives in `docs/`; moving work lives in stage, record,
  workflow, or output folders.
- Skills and MCPs are wired as gates, stage specialists, format triggers,
  always-on references, or cross-workspace capabilities. A generic installed
  tools list is only an inventory.
- Handoffs are physical and normally one-way. Writing output becomes production
  input; production output becomes community source material. Downstream work
  does not silently edit upstream stages.

The important reconciliation is that routing depth and stage layout are
separate choices. `va-resume-v3` and `storytelling` can keep the compact entry
pattern, while a larger umbrella workspace may use the split map/router pattern
without changing the ICM invariants about local context, file state, human
checks, or drift tracking.
