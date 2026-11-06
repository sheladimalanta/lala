# 04_test

Runs after Shela has read the `03_build` result.

## One job

Prove the app works with evidence from something other than the session that built it.

## What it reads

`intent.md`, `SPEC.md`, the code, `decisions.md`, `errors.md`,
`~/lala/_shared/standards/4d-assessment.md`.

## Required skills

- `senior-dev-review`, a system skill
- The project's `.agents/skills/code-review/SKILL.md`

## What it does

The tool that did not build the app does the review, security check and scoring,
read-only except for this stage's output folder.

1. Review the code against `SPEC.md`.
2. Run the tests. AI apps also run evals on the held-out set and sample transcripts.
3. Use the app as a user would, along one real happy path and the listed exceptions.
4. Check security: secrets, access control, injection, dependencies and logging. If
   it uses AI, also check prompt injection, sensitive data, excessive agency and
   unbounded consumption.
5. Run the done gate:
   `python3 scripts/verify_sdk_project_gates.py --stage done`
6. Score the 4Ds, naming an evidence file for each score.

## What it writes

Into `work/01_build-app/04_test/`: `review.md`, `security.md`, `happy-path.md`,
`4d-assessment.md`. End `review.md` with Skills used.

## Standard

`~/lala/_shared/standards/SOURCES.md`, row `04_test`.

## The human check before anything moves on

Ship, fix or stop? Shela records the decision in `4d-assessment.md`. Scores below the
app class send the work back to the stage that owns the missing evidence.
