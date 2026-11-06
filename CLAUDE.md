# lala

Shela's main workspace for Claude Code and Codex. Tasks go in, reviewed work comes out.

Built on ICM: folders carry sequencing, hierarchy carries context, files carry
state. If something needs explaining, the explanation goes in that folder's
`CONTEXT.md`.

## Where things live

| Folder | What it holds |
|---|---|
| `areas/` | The work, its data and its accounts. Each area is its own repo. |
| `01_build-app/` | The lane for building apps: stage contracts only, never project files. |
| `_skills/` | One source for every shared skill. |
| `_shared/` | Rules, standards, Git identities and the workspace verifier. |
| `_templates/` | Stamps for a new area or project. |

## Route

| If | Go to |
|---|---|
| Doing work in an area | Stop and ask Shela to start the session in `~/lala/areas/<area>/` |
| Changing the workspace itself | `~/lala/CONTEXT.md` |
| Already in an area | That area's `CONTEXT.md` |

## The one rule

Nothing moves to the next stage until Shela has read the output of the last one.

## Rules that override convenience

| Rule | Lives in |
|---|---|
| Check whether new surface needs to exist | `~/lala/_shared/PONYTAIL-GATES.md` |
| Stay inside the area the session started in | That area's `CLAUDE.md` |
| Never store secrets in a repo. Keep them in `~/.lala-secrets/<area>/` | Here |
| Ask Shela before sending, sharing, publishing, deleting or pushing | Here |

## Foundations
- Use English only. Explain simply, and give one step at a time when I need to act.
- Always give file paths in full, starting from /Users/lala/. Never shorten them, start them with ~, or make them relative.
- For any prose written for people, such as posts, newsletters, emails, docs and copy, use the writing-style skill. Never use em dashes or exclamation points.
- Read, don't assume. Open the relevant protocol and target files before acting. Reread them, and run their verifier, before saying the work is complete. Correctness matters more than speed.
- No empty words. Say saved, fixed, verified, published or done only after seeing the file, command result, API state, sheet readback, live page or screen that proves it. Name the evidence and where it is. Keep what you saw, what you infer and what you plan separate.
- Truth, Justice and Wisdom routing. Base routing and ownership on evidence you saw. Respect the boundary of the area or lane that owns the work. Take a known direct route without loading unrelated context. Open the workspace map only when the route is unknown, crosses areas, is stale or conflicting, or would change the system structure. The map only routes work. It never grants publishing, credential or production authority.
- Before saying done, use the done-gate skill.
- I often run several Claude Code and Codex terminals at once. Keep edits scoped to the task. Never revert files you didn't change, and treat other terminals' changes as real work. If a shared file changed, reread it and edit only the relevant part.
- When I correct you or state a lasting preference, use the setup-keeper skill to offer to save it.
- When I ask to save the session, use the session-save skill.
- Skills are listed in ~/lala/_skills/INDEX.md. Each area lists its projects in _index/log.md.
