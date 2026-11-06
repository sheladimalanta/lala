---
name: icm-workspace
description: Build and govern a standalone ICM workspace, where entry files map and route, folders carry sequencing, each folder's CONTEXT.md carries local context, and files carry state instead of a status tracker. Use when Lala asks for an ICM workspace, an ICM folder pipeline, a map-router-workspace architecture, a new workspace stamped like va-resume-v3 or storytelling, task-specific load/skip rules, contextual skill or MCP wiring, a repeatable pipeline with per-stage human checks, or a drift check across duplicated rules.
---

# ICM workspace

ICM is the **Interpretable Context Methodology**: a small root entry layer, a
context file in every working folder, and one model that reads its way to the
right place instead of being told where to go.

An ICM workspace is a repo whose folder tree is its documentation. Folders
carry sequencing, hierarchy carries context, files carry state. Nothing is
remembered; everything is somewhere.

The published methodology covers navigation only: routing a prompt to the
right folder's rules. Lala's two workspaces extend it with the production
half: numbered stages, per-stage `output/`, a human check between stages, and
a drift checker. Keep both halves. Navigation without gates routes an agent
efficiently to work nobody has approved.

Five invariants. All five, or it is just folders.

1. **Folders carry sequencing.** Numbered stage directories are the pipeline.
   Order is filesystem order, never prose.
2. **Hierarchy carries context.** Every folder owns a `CONTEXT.md`, explaining
   only its own scope. The explanation lives where the work happens.
3. **Files carry state.** No status field. An empty stage `output/` means the
   stage has not run. `_index/log.md` is a catalog, not the record.
4. **Entry files map and route; they never carry procedure.** A compact
   workspace may keep *if this happened → read that `CONTEXT.md` → stop at this
   human check* in `CLAUDE.md`. A multi-workspace system may split the same job
   into `CLAUDE.md` as the always-loaded map and root `CONTEXT.md` as the task
   router. Procedure belongs in the destination folder's `CONTEXT.md`.
5. **A new unit is a copy of the stamp**, from `_templates/`, never a blank
   page.

Plus the rule that makes the rest worth anything: **nothing moves to the next
stage until a person has read the output of the last one.**

Two workspaces already run this way. Read
`references/worked-examples.md` before designing a third. It shows what each
one chose, and the drift incident that produced the checker.

## Choose the routing depth separately from the layout

The stage layout below answers **where stages live**. Routing depth answers
**how an agent reaches them**. Do not confuse the two decisions.

Use the compact entry pattern for one pipeline or a few closely related lanes:

- `CLAUDE.md` is the map and route table.
- Root `CONTEXT.md` explains the pipeline on one screen and owns shared-rule
  change protocol.
- Folder `CONTEXT.md` files own the work.

Use the split entry pattern when the root contains several genuinely different
workspaces:

- `CLAUDE.md` stays always-loaded and small: folder map, naming, global file
  placement, cross-workspace handoffs, and quick navigation.
- Root `CONTEXT.md` routes task → workspace and names only the extra file needed
  to enter safely.
- Each workspace `CONTEXT.md` routes within that workspace.

Workspaces should represent phases or modes of work that need different
context, not categories of file extensions. If two areas load the same rules,
use the same tools, and share one process, they are probably one workspace.

## Make context loading explicit

Every workspace or stage `CONTEXT.md` is a local contract. Include only what is
needed to answer these questions:

1. What work happens here, and what is upstream and downstream?
2. For this task, what exact files must be loaded?
3. What related files must be skipped?
4. What does the process read and write?
5. Which skill, MCP, or verifier activates at which exact moment?
6. What recurring mistake is forbidden here?

Use a `What to load` table with a `Skip these` column when task variants need
different references. The skip column is an instruction, not decoration: it
prevents thorough agents from loading adjacent but irrelevant context.

Keep stable knowledge in `docs/` and moving work in `workflows/`, stage
folders, record folders, or `output/`. When a `CONTEXT.md` becomes an
encyclopedia, move the stable detail to a named reference and leave the route.

## Wire capabilities where they become necessary

Do not treat a list of installed skills or MCPs as workflow integration. Give
each capability a trigger and a reason at the point of use:

- **Pipeline gate:** must pass before a file moves to the next stage.
- **Stage specialist:** activates only while one stage is running.
- **Format trigger:** activates because the requested output is a PDF, deck,
  social post, or another specific form.
- **Always-on reference:** appears in every relevant row of `What to load`.
- **Cross-workspace capability:** appears in the root map, then receives its
  exact local trigger inside each workspace that uses it.

Add capabilities after a real need appears. Repeated mistakes become reference
docs or gates; missing external reach becomes a tool route. Avoid filling a
workspace with speculative integrations.

## Make handoffs physical

Cross-workspace flow happens through files, not shared mental context. Name the
source path, destination path, acceptance gate, and whether the handoff is a
copy, move, reference, or generated derivative. Prefer one-way flow. If a
downstream change must alter upstream work, make that an explicit re-trigger
instead of silent backtracking.

## Choose the layout first

This is the only architectural decision, and it is hard to reverse.

| | **per-record** | **per-lane** |
|---|---|---|
| Stages live | inside each record | at the root, as lanes |
| Fits | many units, one fixed path | few units, several paths |
| A unit | walks the path once | may re-enter a lane |
| Records hold | their own stage outputs | only their own material |
| Example | `~/va-resume-v3` | `~/storytelling` |

Decide by asking whether two units ever need *different* paths. If no, it is
per-record. If the paths are really stages of one longer path, it is still
per-record. Say so in `CONTEXT.md` rather than inventing lanes.

## Stamp it

```bash
# per-record
python3 ~/lala/_skills/system/icm-workspace/scripts/new_icm_workspace.py \
    --path ~/my-workspace --title "My Workspace" \
    --layout per-record --records applicants \
    --stages intake,profile,target-role,gap,draft,package \
    --gitignore-records

# per-lane
python3 ~/lala/_skills/system/icm-workspace/scripts/new_icm_workspace.py \
    --path ~/my-workspace --title "My Workspace" \
    --layout per-lane --records pieces \
    --lane openers=locate,candidates,test \
    --lane character=prewrite,revelatory,reveal,sketch
```

`--gitignore-records` when records hold real people's data. `--dry-run` prints
the tree and writes nothing. Stage and lane names are slugged and numbered in
the order given.

## Then author it, in this order

The stamp writes the skeleton and the router, never the rules. Every generated
file carries `TODO` markers where a person has to decide something; `grep -rn
TODO <workspace>` is the worklist. Authoring out of order produces a router that
promises stages that do not exist yet.

1. **Root `CONTEXT.md`:** what goes in, what comes out, and **which stage carries
   the most weight**. Every ICM workspace has one stage where a wrong answer
   wastes everything downstream. Naming it is what makes the human checks worth
   their cost.
2. **`_shared/`:** the rules. Each rule gets exactly one home file. Keep them
   few; three is a healthy number.
3. **Each stage `CONTEXT.md`:** one job, what it reads, what it writes, and the
   human check. If a stage needs "and" to describe its job, it is two stages.
4. **Workspace routers:** for a split entry pattern, write each workspace
   `CONTEXT.md` from its completed stages and references.
5. **Root entry files:** fill route destinations and stop conditions last,
   reading them off the local contracts. Keep the compact pattern in
   `CLAUDE.md`; keep the split pattern's task routing in root `CONTEXT.md`.

Stop conditions are the product. A route table whose "Then stop at" column says
anything vaguer than a question a person can answer by reading `output/` is
steering, not a gate.

## The drift check

Duplication is allowed here, and often correct. A stage checklist that restates
the rule it enforces is what makes the rule land at the moment of use. The bias
is **keep the duplicate and track it**. Delete only when the copy teaches
nothing the original does not.

What is not allowed is untracked duplication. Every workspace ships with
`_shared/check-rules.py` and `_shared/rule-map.json`:

```bash
cd <workspace> && python3 _shared/check-rules.py
```

| | Meaning | Fix |
|---|---|---|
| **STALE** | a file derives from a rule whose content changed since anyone last compared the pair | open it, then update **or** bless |
| **UNREGISTERED** | a factory file nothing tracks, so its drift would be invisible | `--register <file> --derives-from a.md,b.md` or `--independent` |
| **MISSING** | the map points at a file that is gone | repoint or unregister |

A blessing is a recorded decision that a person looked and found nothing to
change, so `--reason` is mandatory. A blessing without one is
indistinguishable from a miss. `--bless-all` exists for when one reason honestly
covers every stale file; if it does not, bless in groups.

A fresh stamp reports every factory file UNREGISTERED and exits 1. That is
correct: nothing is authored yet, so nothing is tracked yet.

The map only knows what has been declared. A new file that quietly restates a
rule shows up as UNREGISTERED, which is the prompt to think, but the script
cannot read it and work out what it duplicates. That judgment stays a person's,
at the moment the file is written.

`~/va-resume-v3/_shared/check-rules.py` is this checker's ancestor and is
deliberately left alone. `scripts/check_rules.py` here is the source for new
workspaces; it takes its scan scope from `_scan` in the workspace's
`rule-map.json` instead of hardcoding it.

## Done gates

A workspace is not delivered until all five hold:

1. `grep -rn TODO <workspace>` returns nothing in `CLAUDE.md`, `CONTEXT.md`, or
   any stage `CONTEXT.md`.
2. `python3 _shared/check-rules.py` reports clean.
3. A cold read follows the declared entry chain to the right stage without
   guessing: `CLAUDE.md` alone for the compact pattern, or `CLAUDE.md` → root
   `CONTEXT.md` → workspace `CONTEXT.md` for the split pattern.
4. Every route's stop condition names a question a person answers by reading
   that stage's `output/`.
5. Each task loads only its declared references, skips its declared exclusions,
   invokes capabilities at their recorded trigger, and writes to the recorded
   destination.

For a change to this skill, run `python3 ~/lala/_shared/verify_lala.py`, and
re-stamp both layouts into a scratch path to confirm the templates still render.
