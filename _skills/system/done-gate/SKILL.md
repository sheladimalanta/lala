---
name: done-gate
description: Check finished work against evidence before claiming it. Use before saying done, shipped, complete, fixed, published or live, for any task. Do NOT use mid-task or for planning.
---

# Done gate

1. Restate the requested deliverable.
2. Match each requirement to the evidence that proves it, and name where that evidence is.
3. Apply each check that fits:

| Work | Check |
|---|---|
| Visual work | Open or render it and look. |
| Code | Run the verify-work skill. |
| Prose for people | Run the writing-style check script. |
| Anything with a verifier | Run it. In ~/lala: `python3 ~/lala/_shared/verify_lala.py`. |
| Live URL | Probe it before listing it. |
| Sheet write | Read back the exact range written. |
| API wrapper | Run one real happy path. |
| Deploy | Check build, deploy status, live status code and expected page markers. |
| Skill, script, workflow or long process | Confirm `~/lala/_shared/PONYTAIL-GATES.md` was applied. |

Skip PDF checks for now.

4. State the remaining risk. Keep what you saw, what you infer and what you plan separate.

A requirement with no evidence is not done. Say what is missing.
