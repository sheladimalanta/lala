#!/usr/bin/env python3
"""Stamp a new ICM workspace: folders carry sequencing, hierarchy carries
context, files carry state.

Two layouts, described in SKILL.md:

  per-record   stages live inside each record. Many units walk one fixed
               path, each needing its own audit trail. (~/va-resume-v3)

  per-lane     stages live at the root as lanes. Few units, several paths,
               a unit may re-enter a lane. (~/storytelling)

  python3 new_icm_workspace.py --path ~/thing --title "Thing" \\
      --layout per-record --records applicants \\
      --stages intake,profile,target-role,gap,draft,package

  python3 new_icm_workspace.py --path ~/thing --title "Thing" \\
      --layout per-lane --records pieces \\
      --lane openers=locate,candidates,test \\
      --lane character=prewrite,revelatory,reveal,sketch

The scaffold writes the skeleton and the router, not the rules. Every
generated file carries TODO markers where a person has to decide something.
A workspace whose TODOs are still in place is not configured, it is stamped.

--dry-run prints the tree it would write and touches nothing.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER_SRC = HERE / "check_rules.py"

ICM_PREAMBLE = (
    "Built on ICM: folders carry sequencing, hierarchy carries context, files "
    "carry state. The structure is the documentation. If something needs "
    "explaining, the explanation goes in that folder's `CONTEXT.md`, not in "
    "your head."
)


def slug(text: str) -> str:
    return text.strip().strip("/").replace(" ", "-").lower()


def numbered(names) -> list:
    return [(f"{i:02d}_{slug(n)}", slug(n)) for i, n in enumerate(names, start=1)]


def check_destination(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if resolved.exists() and any(resolved.iterdir()):
        sys.exit(f"{resolved} exists and is not empty. Pick an empty or new path.")
    return resolved


def stage_context(stage: str, position: str, writes: str = "`output/`") -> str:
    return f"""# {stage}

{position}

## One job

TODO: the single thing this stage does. If you need "and" to describe it,
it is two stages.

## What it reads

TODO: the inputs, by path. A stage that reads the whole workspace is not a
stage.

## What it writes

Into {writes}. TODO: name the files and what each one is for.

## The human check before anything moves on

TODO: the question a person answers by reading {writes}. Not "does it look
fine" — the specific thing that would send this back.
"""


def unit_context(unit: str, stages) -> str:
    rows = "\n".join(
        f"| `{d}/` | TODO | TODO |" for d, _ in stages
    ) or "| TODO | TODO | TODO |"
    return f"""# One {unit}

A copy of this folder, one per {unit}. Never start from a blank page.

{ICM_PREAMBLE}

| Stage | One job | Human check |
|---|---|---|
{rows}

Status is what exists. An empty `output/` means that stage has not run.
"""


def piece_context(unit: str) -> str:
    return f"""# One {unit}

A copy of this folder, one per {unit}. Never start from a blank page.

| Folder | What it holds |
|---|---|
| `source/` | what this {unit} is made of. Not written here, gathered here. |
| `work/` | stage output, written by whichever lane this {unit} is in. |
| `notes.md` | TODO: what a person needs to know to pick this up cold. |

The stages are not in here. They are in the lane at the workspace root.
Which lane a {unit} is in is a fact about the {unit}: record it in
`notes.md` and in `_index/log.md`.
"""


def claude_md(title: str, layout: str, records: str, unit: str, stages, lanes) -> str:
    if layout == "per-record":
        where = f"""| Folder | What it holds |
|---|---|
| `_shared/` | the factory: the rules, the output format, the schemas. Stable across every {unit}. |
| `_templates/{unit}/` | the stamp. A new {unit} is a copy of this, never a blank page. |
| `_index/log.md` | one line per {unit}: id, stage. |
| `{records}/` | the records. One folder per {unit}. |"""
        routes = "\n".join(
            f"| {'the previous stage was approved' if i else f'a new {unit} arrived'} "
            f"| {f'`{records}/<id>/{d}/CONTEXT.md`' if i else f'copy `_templates/{unit}/` into `{records}/`, then `{d}/CONTEXT.md`'} "
            f"| TODO |"
            for i, (d, _) in enumerate(stages)
        )
    else:
        where = "\n".join(
            [
                "| Folder | What it holds |",
                "|---|---|",
                f"| `_shared/` | the factory: the rules and the craft law. Stable across every {unit}. |",
                f"| `_templates/{unit}/` | the stamp. A new {unit} is a copy of this, never a blank page. |",
                f"| `_index/log.md` | one line per {unit}: id, lane, stage. |",
            ]
            + [f"| `{d}/` | lane: TODO what this lane is for. |" for d, _ in lanes]
            + [f"| `{records}/` | the records. One folder per {unit}. |"]
        )
        routes = "\n".join(
            f"| TODO: what a person wants when they should enter this lane "
            f"| `{d}/CONTEXT.md` | TODO |"
            for d, _ in lanes
        )

    status_glob = f"`{records}/*/*/output/`" if layout == "per-record" else f"`{records}/*/work/`"
    return f"""# {title}

TODO: one sentence. What goes in, what comes out.

{ICM_PREAMBLE}

## Where things live

{where}

## Route by what just happened

| If | Go to | Then stop at |
|---|---|---|
{routes}
| asked for status | scan {status_glob} and read `_index/log.md` | report what exists |
| **asked to change any rule in `_shared/`** | `CONTEXT.md` → "Changing a shared rule" | **`python3 _shared/check-rules.py` reports clean** |

A revision is not done when the file you were asked about is correct. It is
done when nothing else in the workspace still teaches the old rule. The check
is what tells you which.

## The one rule

Nothing moves to the next stage until a person has read the output of the last
one.

## Rules that override convenience

TODO: name them, keep them few, give each exactly one home. Read the file, not
this table.

| Rule | Lives in |
|---|---|
| TODO | `_shared/TODO.md` |
"""


def context_md(title: str, layout: str, records: str, unit: str, stages, lanes) -> str:
    if layout == "per-record":
        rows = "\n".join(
            f"| {i:02d} | `{d}` | TODO | TODO |"
            for i, (d, _) in enumerate(stages, start=1)
        )
        body = f"""Each {unit} folder is a copy of `_templates/{unit}/`. The stages run inside
it, in order. Every stage writes to its own `output/`, and a person reads that
output before the next stage starts.

| # | Stage | One job | Human check |
|---|---|---|---|
{rows}

## Which stage carries the most weight

TODO: name it, and say why correction is cheapest there. Every ICM workspace
has one stage where a wrong answer wastes everything downstream. Knowing which
is what makes the human checks worth their cost."""
    else:
        rows = "\n".join(f"| `{d}/` | TODO | TODO |" for d, _ in lanes)
        body = f"""Each {unit} folder is a copy of `_templates/{unit}/` and holds only its own
material. The stages live in the lanes at the root, and a {unit} walks one lane
at a time.

| Lane | What it is for | Ends at |
|---|---|---|
{rows}

## Why lanes and not one pipeline

TODO: say what makes these paths genuinely different, rather than stages of one
longer path. If they are stages of one path, this should have been per-record."""

    return f"""# The pipeline, on one screen

TODO: one line in, one line out.

{body}

## What stays the same every run

`_shared/` is the factory. Configure it once:

- TODO: one line per rule file, naming what it owns

`{records}/` is the product. New every run.

---

## Changing a shared rule

A rule changed in one file and not the others is how a workspace goes quietly
wrong. It does not fail. Nothing complains. It gets found by accident.

So a revision is not finished when the file you were asked about is correct.

**1. Ask whether the second copy earns its keep.** Some do not — delete them.
Some do: a stage checklist that restates the rule it enforces is the thing that
makes the rule land at the moment of use. Deleting it to save maintenance
trades product quality for tidiness, which is the wrong trade.

**2. Everything that earns its keep gets declared.** Register it in
`_shared/rule-map.json` so the dependency is visible instead of remembered.

The bias here is **keep the duplicate and track it**. Delete only when the copy
teaches nothing the original does not.

**3. Run the check before you call the work done.**

```
python3 _shared/check-rules.py
```

| | |
|---|---|
| **STALE** | a file derives from a rule whose content has changed since anyone last looked at the pair |
| **UNREGISTERED** | a factory file nothing is tracking, so its drift would be invisible |
| **MISSING** | the map points at a file that has been deleted or moved |

**4. Every STALE file gets opened.** Then update it, or bless it:
`--bless <file> --reason "why no change was needed"`. A blessing is a recorded
decision that a person looked and found nothing to change. `--reason` is
mandatory, because a blessing without one is indistinguishable from a miss.

**5. Commit the rule change and everything it touched in one commit.**

### What this does not catch

The map only knows what has been declared. A new file that quietly restates a
rule and is never registered will show up as UNREGISTERED — which is the prompt
to think about it — but the script cannot read it and work out what it
duplicates. That judgment is still a person's, at the moment the file is
written.

## Status is a file scan

There is no status field to maintain. Status is what exists: an empty stage
`output/` means that stage has not run. `_index/log.md` is the catalog, not the
record.
"""


def rule_map(layout: str, records: str, lanes) -> dict:
    dirs = ["_shared", "_templates"] + ([d for d, _ in lanes] if layout == "per-lane" else [])
    return {
        "_what_this_is": "Which files in the factory restate knowledge that lives "
                         "somewhere else. Checked by _shared/check-rules.py. "
                         "Protocol in the root CONTEXT.md, 'Changing a shared rule'.",
        "_why": "A rule changed in one file and not the others does not fail. "
                "Nothing complains. This map is what complains.",
        "_hashes": "First 12 chars of the sha256 of the dependency's bytes, as of "
                   "the last time a person compared the two files. A mismatch "
                   "means STALE, not wrong.",
        "_scan": {
            "dirs": dirs,
            "files": ["CONTEXT.md", "CLAUDE.md"],
            "ignore": [".git", ".obsidian", "_index", records],
        },
        "files": {},
        "independent": [],
        "blessings": [],
    }


def plan(args) -> list:
    """Every file the stamp will write, as (relative path, content or None)."""
    unit = args.unit or args.records.rstrip("s") or "record"
    stages = numbered(args.stages.split(",")) if args.stages else []
    lanes = [(f"{i:02d}_{slug(n)}", slug(n), [slug(s) for s in ss])
             for i, (n, ss) in enumerate(args.lane or [], start=1)]
    lane_dirs = [(d, n) for d, n, _ in lanes]

    files = [
        ("CLAUDE.md", claude_md(args.title, args.layout, args.records, unit, stages, lane_dirs)),
        ("CONTEXT.md", context_md(args.title, args.layout, args.records, unit, stages, lane_dirs)),
        ("_index/log.md", f"# {args.title} log\n\nOne line per {unit}. The catalog, "
                          f"not the record.\n\n| id | "
                          f"{'lane | ' if args.layout == 'per-lane' else ''}stage |\n"
                          f"|---|---|{'---|' if args.layout == 'per-lane' else ''}\n"),
        ("_shared/rule-map.json",
         json.dumps(rule_map(args.layout, args.records, lane_dirs), indent=2) + "\n"),
        (".gitignore", ".DS_Store\n" + (f"{args.records}/\n" if args.gitignore_records else "")),
        (f"{args.records}/.gitkeep", ""),
    ]

    if args.layout == "per-record":
        files.append((f"_templates/{unit}/CONTEXT.md", unit_context(unit, stages)))
        for i, (d, name) in enumerate(stages, start=1):
            position = (f"Stage {i} of {len(stages)}. "
                        + ("The first thing that happens." if i == 1 else
                           f"Runs after `{stages[i - 2][0]}` has been read by a person."))
            files.append((f"_templates/{unit}/{d}/CONTEXT.md", stage_context(name, position)))
            files.append((f"_templates/{unit}/{d}/output/.gitkeep", ""))
    else:
        files.append((f"_templates/{unit}/CONTEXT.md", piece_context(unit)))
        files.append((f"_templates/{unit}/notes.md", f"# TODO: {unit} name\n\nLane:\n"))
        files.append((f"_templates/{unit}/source/.gitkeep", ""))
        files.append((f"_templates/{unit}/work/.gitkeep", ""))
        for d, name, substages in lanes:
            files.append((f"{d}/CONTEXT.md",
                          f"# {name}\n\nTODO: what a person wants when they come here, and "
                          f"what they leave with.\n\nA {unit} in this lane keeps its material "
                          f"in `{args.records}/<id>/`. This folder holds the stages, not the "
                          f"work.\n\n## Stages\n\n"
                          + "\n".join(f"- `{i:02d}_{s}/`" for i, s in enumerate(substages, start=1))
                          + "\n"))
            for i, s in enumerate(substages, start=1):
                position = (f"Stage {i} of {len(substages)} in the `{name}` lane."
                            if i > 1 else f"Where the `{name}` lane starts.")
                files.append((f"{d}/{i:02d}_{s}/CONTEXT.md", stage_context(
                    s, position, f"`{args.records}/<id>/work/{d}/{i:02d}_{s}/`")))

    return files


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--path", required=True, help="where to stamp it. Must be empty or new.")
    ap.add_argument("--title", required=True, help="human name, used in headings")
    ap.add_argument("--layout", required=True, choices=["per-record", "per-lane"])
    ap.add_argument("--records", required=True,
                    help="folder that holds the records, e.g. applicants, pieces")
    ap.add_argument("--unit", help="singular of --records. Defaults to --records minus a trailing s.")
    ap.add_argument("--stages", help="per-record: comma-separated stage names, in order")
    ap.add_argument("--lane", action="append", metavar="NAME=S1,S2",
                    type=lambda v: (v.split("=", 1)[0], v.split("=", 1)[1].split(",")),
                    help="per-lane: one per lane. Repeatable.")
    ap.add_argument("--gitignore-records", action="store_true",
                    help="records hold personal data and must not be committed")
    ap.add_argument("--dry-run", action="store_true", help="print the tree, write nothing")
    args = ap.parse_args()

    if args.layout == "per-record" and not args.stages:
        sys.exit("--layout per-record needs --stages")
    if args.layout == "per-lane" and not args.lane:
        sys.exit("--layout per-lane needs at least one --lane NAME=stage1,stage2")
    if args.layout == "per-lane" and args.stages:
        sys.exit("--stages is for per-record. Per-lane stages go inside --lane.")
    if not CHECKER_SRC.exists():
        sys.exit(f"Missing {CHECKER_SRC}. The workspace needs its drift checker.")

    dest = check_destination(Path(args.path))
    files = plan(args)

    if args.dry_run:
        print(f"Would write into {dest}:\n")
        for rel, _ in sorted(files) + [("_shared/check-rules.py", None)]:
            print(f"  {rel}")
        return 0

    for rel, content in files:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    checker = dest / "_shared" / "check-rules.py"
    shutil.copy2(CHECKER_SRC, checker)
    checker.chmod(0o755)
    # Both tools read the same entry file. Claude Code reads CLAUDE.md, Codex reads AGENTS.md.
    (dest / "AGENTS.md").symlink_to("CLAUDE.md")

    print(f"Stamped {args.title} into {dest}\n")
    print("It is stamped, not configured. In order:\n")
    print("  1. CONTEXT.md      — what goes in, what comes out, which stage carries the weight")
    print("  2. _shared/        — write the rules. Each one gets exactly one home.")
    print("  3. each stage CONTEXT.md — one job, what it reads, what it writes, the human check")
    print("  4. CLAUDE.md       — fill the route table's stop conditions last, from the stages")
    print(f"\n  grep -rn TODO {dest}    # what is still undecided")
    print("\nThen register what duplicates what, until this reports clean:\n")
    print(f"  cd {dest} && python3 _shared/check-rules.py")
    print("\nA fresh stamp reports every factory file UNREGISTERED. That is correct:")
    print("nothing is authored yet, so nothing is tracked yet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
