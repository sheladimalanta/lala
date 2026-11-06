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
