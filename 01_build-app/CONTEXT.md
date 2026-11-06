# Build an app

Shela arrives with an app, tool, agent or integration to build. She leaves with a
working app, its evidence and an owner.

A project walks these stages in order. Its files stay in
`areas/<area>/projects/<id>/`. This folder holds contracts, never project files.

| # | Stage | One job | Human check |
|---|---|---|---|
| 01 | `01_plan/` | Write `intent.md` from the real workflow | What result proves this worked, and which exception did the request not mention? |
| 02 | `02_design/` | Write a spec Shela can approve | Is this what you want built, whose data does it touch, and what is the worst action it can take? |
| 03 | `03_build/` | Build one ticket at a time, tests first | Does every ticket pass, and does the result still match the spec? |
| 04 | `04_test/` | Prove it with independent evidence | Ship, fix or stop? |
| 05 | `05_deploy/` | Release it safely | Can it roll back, and do you approve this release? |
| 06 | `06_maintain/` | Hand it to an owner, with monitoring | Who owns it, and which signal reopens the work? |

## Which stage carries the most weight

`01_plan`. A wrong problem wastes everything after it and is cheapest to correct
there, so do not rush past its human check.

## Size to the app

`01_plan` records the app class from `_shared/standards/4d-assessment.md`.

| Class | May skip, with the reason recorded in `notes.md` |
|---|---|
| Personal | `05_deploy` if it never leaves this Mac, and `06_maintain` |
| Shared | Nothing |
| Production | Nothing |

Tests, the security check and the 4D assessment are never skipped.

## Handoffs

Each stage's output is committed, so either tool can continue from files alone.
What the project learns goes into a file, then starts a new project or a rule
change. It never silently edits an earlier stage.
