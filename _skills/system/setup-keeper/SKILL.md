---
name: setup-keeper
description: Offer to save a lasting instruction in the right setup file. Use when Shela corrects you, repeats an instruction, states a lasting preference, or says "always" or "never". Also use when Shela asks for the monthly setup check. Do NOT use for instructions that only apply to the current task.
---

# Setup keeper

Choose the location with `reference.md` in this folder.

## Saving an instruction

1. If it applies only to the current task, don't offer to save it (row 7).
2. Never save passwords, keys or tokens. Point to `~/.lala-secrets/<area>/` instead (row 8).
3. Ask once whether to save it. Name the location, the matching row in `reference.md`, and where
   Codex gets the same instruction. If Shela says no, drop it.
4. Read the target file first. If the instruction is already there, say so. If it contradicts
   something there, show both and ask which one wins.
5. Show the exact change. Write only after Shela approves.
6. If Codex can't write the file from its sandbox, give Shela the exact change to apply from
   Claude Code.
7. After saving, add one row to `~/lala/_shared/setup-log.md`. If the file doesn't exist,
   create it with this header:

   | Date | What Shela said | Saved to | Row | Why | Tool |
   |---|---|---|---|---|---|

## Monthly check

Only when Shela asks for it.

1. Ask Shela to run `/doctor prompt-audit` in Claude Code and share the output. If it isn't
   available, say so and continue.
2. Run `python3 ~/lala/_shared/verify_lala.py`. It fails if a skill folder under `_skills` isn't
   listed in `_skills/INDEX.md`.
3. Read the last month of `~/lala/_shared/setup-log.md`. Check each entry against
   `reference.md` for anything saved in the wrong place.
4. Report the findings. Change nothing until Shela approves.
