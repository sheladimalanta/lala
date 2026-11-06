# Route a task in {{AREA}}

{{HOLD}}Find the row, open the file, and stop where it says.

| If Shela asks for | Go to | First stop |
|---|---|---|
| An app, tool, agent or integration | `~/lala/01_build-app/CONTEXT.md` | `01_plan`: What result proves this worked? |
| An established pipeline | `pipelines/<name>/CONTEXT.md` | That pipeline's human check |
| A one-off lookup, page read or form | `~/lala/_shared/browsing.md` | Is this what you asked for? |
| Project status | Scan `projects/*/work/`, and read `_index/log.md` | Report what exists |
| Data collected from a site, repeatedly | No lane yet. Follow `~/lala/CONTEXT.md`, "A new lane" | Shela approves its stages |
| A change to the workspace itself | Ask Shela to start a session in `~/lala` | |
| Anything else | Ask one question before starting | |

When a project already exists, read its `notes.md` first, then the `CLAUDE.md` at its
root if it has one.
