# Ponytail Gates

Use these before adding files, scripts, dependencies, workflows, or new repo
surface area. The Ponytail plugin applies its own ladder to code. This file
governs the workspace.

## Mandatory triggers

Run this gate before:

- Creating or updating any Codex, Claude, Cobalt, personal, or Bible skill.
- Adding or editing reusable scripts.
- Starting a long multi-step process that may cross context compaction.
- Adding a workflow, lane, protocol, checklist, or new output surface.
- Introducing any dependency, connector, plugin, browser path, or external tool route.

For skill creation, this gate is separate from `skill-creator` validation. Both
must pass before handoff.

## Senior Dev Ladder

1. Does this need to exist?
2. Does it already exist?
3. Can the standard library or platform handle it?
4. Can an installed dependency handle it?
5. Can this be smaller?
6. What verifier proves it works?

## ICM ownership gate

Before adding or changing a workflow, check the area's `CONTEXT.md` and the
target repository for an existing ICM workspace. ICM is the default architecture
for every new operational workflow. If no workspace exists, load
`~/lala/_skills/system/icm-workspace/SKILL.md` and design the work as an ICM
workspace before proposing another architecture.

When an ICM workspace already owns the work:

- it remains the sole operational home;
- extend that workspace instead of creating a sibling process or repository;
- keep sequencing in its numbered folders, local procedure in each folder's
  `CONTEXT.md`, and state in its stage outputs;
- wire schedulers, connectors, launchers, and deterministic scripts as
  capabilities invoked at the stage that needs them; and
- never use a wrapper prompt, queue status, copied workspace, SDK project, or
  external script to override an ICM route, stop condition, human gate, or
  content contract.

Stop and obtain Lala's explicit approval before creating a non-ICM workflow or
making any exception. The proposal must identify the canonical ICM owner, the
boundary that would move, why an in-workspace capability cannot solve it, and
the verifier that would detect drift. Convenience, concurrency, scheduling, or
SDK requirements are not exceptions by themselves.

## Stop conditions

Stop before copying any generated archive, customer data, `.env`, `.claude`,
`memory`, session logs, PDFs, screenshots, images, PPTX files, caches, or build
artifacts into the `~/lala` root repo.

## Verifier

```bash
python3 ~/lala/_shared/verify_lala.py
```
