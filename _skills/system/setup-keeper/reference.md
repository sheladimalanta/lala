# Where a setup change goes

Source: `~/lala/_shared/guides/claude-code-customization-guide.html`, based on the setup as of
November 6, 2026. Some Codex permission features are beta or experimental, so check them before
relying on them.

## Decision order

1. Should it always apply? Use the smallest `CLAUDE.md` that covers it.
2. Is it a procedure you repeat? Make it a skill.
3. Can it never have exceptions? Use a setting or a hook.

Claude reads instructions and usually follows them, but can decide not to. The tool applies
settings and hooks itself.

## The map

| Row | If it | Claude Code | Codex |
|---|---|---|---|
| 1 | Applies everywhere in lala | `~/lala/CLAUDE.md` | Reads it through `~/.codex/AGENTS.md`, a link to `~/lala/CLAUDE.md` |
| 2 | Applies to one area | `~/lala/areas/<area>/CLAUDE.md` | That area's `AGENTS.md`, a link to its `CLAUDE.md` |
| 3 | Applies to one project | The project's `CLAUDE.md`. Create it if missing. | The project's `AGENTS.md`, linked to its `CLAUDE.md` |
| 4 | Applies only to certain files | `.claude/rules/<topic>.md` with a `paths:` line | The same rule in the nearest `AGENTS.md` above those files. Codex reads instruction files from the Git root down to where it starts, not folders below. |
| 5 | Is a repeated procedure or checklist | A skill: `_skills/system/` for all areas, `_skills/lanes/` for one build stage, or the project's `.agents/skills/` for one app, linked into the project's `.claude/skills/`. Add it to `_skills/INDEX.md`. | The same skill, through `~/.agents/skills/` or the project's `.agents/skills/` |
| 6 | Must never happen, or must always happen | `deny` or `ask` rules in `settings.json`, or a hook | `.rules` files for commands, the permission profile in `config.toml` (`default_permissions` and `[permissions.<name>]`) for files, `hooks.json` for checks |
| 7 | Is only for the current task | Don't save it. | Don't save it. |
| 8 | Is a password, key or token | Never in instruction files. Only in `~/.lala-secrets/<area>/`. | The same |

## Row details

- Row 1: `~/.codex/AGENTS.md` is a link, so editing it edits `~/lala/CLAUDE.md`. Add only what
  Claude can't work out itself.
- Row 2: `verify_lala.py` checks that each area's `AGENTS.md` links to its `CLAUDE.md`.
- Row 4: Add a rule only when a project needs one. Codex `.rules` files are different: they
  control commands, not files.
- Row 5: Turn a task you've explained twice into a skill. For a system skill, also link its
  folder into `~/.claude/skills/` and `~/.agents/skills/`, and add it to `SYSTEM_SKILLS` in
  `~/lala/_shared/verify_lala.py`.
- Row 6:
  - Everywhere: `~/.claude/settings.json`. Codex: `~/.codex/config.toml` and
    `~/.codex/rules/default.rules`.
  - One area: `<area>/.claude/settings.json`. Codex: that area's `.codex/config.toml`.
  - Hooks: the project's `.claude/settings.json`, then check them with `/hooks`. Codex:
    `~/.codex/hooks.json` or the project's `.codex/hooks.json`, then review and trust them with `/hooks`.
  - Edit Codex config files from outside Codex, then restart Codex.
  - `verify_lala.py` requires some settings in `~/.claude/settings.json`. Don't change those.

## Not used for now

- `CLAUDE.local.md`: skip it. Codex has no direct match. `AGENTS.override.md` replaces a folder's
  `AGENTS.md` instead of adding to it.
- Auto memory and Codex memories: notes the tool saves itself. Setup-keeper doesn't save there.
- Output style: skip it, because `CLAUDE.md` covers this.

## After a change

Start a new session. In Claude Code, run `/context all` to see what loaded. In Codex, use
`/debug-config` to check settings.
