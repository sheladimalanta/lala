---
name: verify-work
description: Verify code changes before saying the work is done. Use after editing code and before reporting it finished, fixed, passing or ready. Runs the project's tests, reads git diff, checks that no test was removed or weakened, and reports PASS or FAIL with the commands and output as evidence. Do NOT use for planning, for reviewing someone else's code, or for edits that touch no code.
---

# Verify Work

1. Find the test command in the project's `CLAUDE.md`, `README.md`, `package.json`,
   `pyproject.toml`, `Makefile`, or the Stop hook in `.claude/settings.json`.
   If there is none, report FAIL: no test command.
2. Run it. Keep the exact command, its exit code and the end of its output.
3. Run `git status` and `git diff HEAD`, and read untracked files too. Read every change.
4. Check every test file in the diff. FAIL if a test was deleted or skipped
   (`skip`, `xfail`, `.only`, `@Disabled`), if an assertion was removed or loosened,
   if an expected value was changed to match new output without the spec saying so,
   or if config was changed to leave a test out of the run.
5. Report:

   ```
   VERIFY: PASS | FAIL
   Tests: <command> -> exit <code>
   <last lines of output>
   Diff: <files changed>
   Tests weakened: none | <file:line and what changed>
   ```

PASS needs exit 0 and no weakened test. Otherwise it's FAIL, and the work isn't done.
