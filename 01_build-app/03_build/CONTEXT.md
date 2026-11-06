# 03_build

Runs after Shela has approved `SPEC.md`.

## One job

Build one ticket at a time, with its test written first.

## What it reads

`SPEC.md`, the tests from `02_design`, and `docs/agents/sdk-build-state.json`.
Start from a fresh session so the build begins from the written spec.

## Required skills

Open each by path from the project's `.agents/skills/`:
`to-tickets`, `tdd`, `implement`, `diagnosing-bugs`.

## What it does

1. Split the spec into a feature list where every feature starts as failing.
2. Pass the implementation gate:
   `python3 scripts/verify_sdk_project_gates.py --stage implementation`
3. For each ticket, plan first, write the failing test, then build it. Never remove
   or weaken a test to make it pass.
4. Leave a clean, committed state at the end of each session, with a short progress
   note in `work/01_build-app/03_build/progress.md`.
5. Add the human path for cases the app cannot handle, if `intent.md` lists any.
6. After two failed fixes, stop and restart the diagnosis. Record it in `errors.md`.

## What it writes

Code, tests, `errors.md`, and `progress.md`, which ends with Skills used.

## Standard

`~/lala/_shared/standards/SOURCES.md`, row `03_build`.

## The human check before anything moves on

Does every ticket pass, and does the result still match the spec? A stubbed feature
counts as a failed ticket.
