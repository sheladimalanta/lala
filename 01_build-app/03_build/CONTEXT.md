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

- `verify-work`, a system skill, after code is edited and before the work is called done

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
7. Once the project has a working test command, show Shela this Stop hook, then add
   it to the project's `.claude/settings.json` with `<test command>` filled in:

   ```json
   {
     "hooks": {
       "Stop": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "cd \"$CLAUDE_PROJECT_DIR\" && <test command> 1>&2 || exit 2"
             }
           ]
         }
       ]
     }
   }
   ```

   All test output goes to stderr. If the tests fail, the hook exits with code 2,
   which stops Claude from finishing and gives it the failures to fix.
   Start every `03_build` session inside the project folder, so the project's
   `.claude/settings.json` and `$CLAUDE_PROJECT_DIR` apply.
8. If Codex is building instead, once the project has a working test command, show
   Shela this Stop hook, then add it to the project's `.codex/hooks.json` with
   `<test command>` filled in:

   ```json
   {
     "hooks": {
       "Stop": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "python3 \"$HOME/lala/_shared/codex_stop_gate.py\" \"<test command>\"",
               "timeout": 600
             }
           ]
         }
       ]
     }
   }
   ```

   The gate runs the tests from the Git root. If they fail, it gives Codex the
   failures to fix, up to 5 times per session, then stops the session and says the
   tests still fail. Start the session inside the project folder, and trust the hook
   in `/hooks` before it can run.

## What it writes

Code, tests, `errors.md`, and `progress.md`, which ends with Skills used.

## Standard

`~/lala/_shared/standards/SOURCES.md`, row `03_build`.

## The human check before anything moves on

Does every ticket pass, and does the result still match the spec? A stubbed feature
counts as a failed ticket.
