# Changing the workspace

Sessions start here only to change the workspace. App and area work starts in
`~/lala/areas/<area>/`.

Read `_shared/PONYTAIL-GATES.md` first for every row below.

| If Shela wants | Do this | Stop when |
|---|---|---|
| A new area | Confirm it has separate accounts or data. Copy `_templates/area/`, replace `{{AREA}}`, link `AGENTS.md` to `CLAUDE.md`, run `git init`. | Shela confirms its accounts |
| A new lane, such as scraping | Load `_skills/system/icm-workspace/SKILL.md`. Author it from one real project. Add it to each area's `CONTEXT.md`. | Shela approves its stages |
| A new pipeline | Load `icm-workspace` and stamp it into an empty `areas/<area>/pipelines/<name>/`. | Shela approves its stages |
| A new shared skill | Put it in `_skills/`. Link it to both tool homes only if any area may need it at any time. Otherwise, name it by path in a stage contract. | Its description triggers on real prompts and not on unrelated ones |
| A rule change | Change its one home. Search for any restatement and update it in the same commit. | `python3 _shared/verify_lala.py` passes |

Add a skill registry when there are about 10 custom skills or one gets missed.
Add a Google connection when a real task needs that account, read-only first.
