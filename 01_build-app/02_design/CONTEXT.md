# 02_design

Runs after Shela has read and approved `intent.md`.

## One job

Write a spec Shela can approve before any product code exists.

## What it reads

`work/01_build-app/01_plan/intent.md` and official docs for every service used.

## Required skills

Open each by path. Do not rebuild a skill from memory.

- `~/lala/_skills/lanes/build-app/sdk-project-builder/SKILL.md`
- After setup, the project's `.agents/skills/research/SKILL.md`
- The project's `.agents/skills/grill-with-docs/SKILL.md`
- The project's `.agents/skills/to-spec/SKILL.md`

## What it does

1. Set up the project with the builder skill. Use provider `claude`, `openai`,
   `both`, or `none` for a non-AI app. Run its setup gate.
2. Map the data, APIs and integrations, with an official source for each material
   claim. AI apps record these in `docs/agents/sdk-facts.md`.
3. Write down whose data it touches, the permissions it needs, and the worst action
   it could take. Use least privilege, and keep credentials out of the repo.
4. Grill until the key decisions and vocabulary are settled.
5. Write the spec with a small architecture diagram.
6. Write acceptance tests from the success criteria, including edge cases. AI apps
   add evals in `evals/` from real failures, with a held-out set.

## What it writes

- `SPEC.md` at the project root
- Acceptance tests and any evals
- `work/01_build-app/02_design/risks.md`, ending with Skills used

## Standard

`~/lala/_shared/standards/SOURCES.md`, row `02_design`.

## The human check before anything moves on

Is this what you want built, whose data does it touch, and what is the worst action
it can take? Shela's approval is recorded as `approved_by_lala` in
`docs/agents/sdk-build-state.json`.
