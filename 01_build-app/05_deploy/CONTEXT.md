# 05_deploy

Runs after Shela chooses ship in `4d-assessment.md`.

## One job

Release the app safely, using the simplest host that fits.

## What it reads

`intent.md`, `SPEC.md`, `work/01_build-app/04_test/`.

## What it does

1. Confirm no secrets are in the repo, and that the host stores them.
2. Choose the host. Use containers only if the app needs them. Agent SDK apps follow
   the hosting guide, including session limits and isolation.
3. Write how to deploy it again and how to roll it back, then test the rollback.
4. Run the human fallback once, if the app has one.
5. Production class: pilot it beside the current process and compare results against
   the success criteria before replacing that process.
6. Write `DILIGENCE.md`: AI's role, sources, permissions and what was verified.

Deploying, publishing and pushing all stop for Shela's approval.

## What it writes

`work/01_build-app/05_deploy/release.md`, ending with Skills used, and `DILIGENCE.md`.

## Standard

`~/lala/_shared/standards/SOURCES.md`, row `05_deploy`. The rollback step is a proposal
from the build discipline Shela shared, not from a named Anthropic source.

## The human check before anything moves on

Can it roll back, and do you approve this release?
