#!/usr/bin/env python3
"""Verify that ~/lala is wired correctly. Read-only. Exit 0 means PASS."""

import json
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
ROOT = HOME / "lala"
AREA_EMAILS = {
    "cobalt": "shela@cobaltintelligence.com",
    "church": "lala.dimalanta@ibcmanila.org",
    "learning": None,  # the GitHub email chosen at install time
    "personal": None,
}
SYSTEM_SKILLS = ("icm-workspace", "senior-dev-review", "verify-work")
STAGES = ("01_plan", "02_design", "03_build", "04_test", "05_deploy", "06_maintain")
OLD_REFS = ("Life-Dashboard", "laladimalanta", "verify-core-paths", "personal-skills/")


def run_git(*args: str) -> str:
    done = subprocess.run(["git", *args], capture_output=True, text=True)
    return done.stdout.strip()


def check_entry(folder: Path, errors: list) -> None:
    agents = folder / "AGENTS.md"
    if not (folder / "CLAUDE.md").is_file():
        errors.append(f"Missing {folder}/CLAUDE.md")
    if not agents.is_symlink() or agents.resolve() != (folder / "CLAUDE.md").resolve():
        errors.append(f"{agents} must be a symlink to CLAUDE.md")
    if not (folder / "CONTEXT.md").is_file():
        errors.append(f"Missing {folder}/CONTEXT.md")


def check_clean_settings(errors: list) -> None:
    path = HOME / ".claude" / "settings.json"
    try:
        settings = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        errors.append("~/.claude/settings.json is missing or not valid JSON")
        return
    if settings.get("disableClaudeAiConnectors") is not True:
        errors.append("disableClaudeAiConnectors must be true")
    if settings.get("syncClaudeAiPlugins") is not False:
        errors.append("syncClaudeAiPlugins must be false")
    if settings.get("skillOverrides", {}).get("brand-guidelines") != "off":
        errors.append("skillOverrides.brand-guidelines must be off")
    if settings.get("permissions", {}).get("defaultMode") != "default":
        errors.append("permissions.defaultMode must be default (manual mode)")


def main() -> int:
    errors: list = []
    check_entry(ROOT, errors)
    check_clean_settings(errors)

    default_config = ROOT / "_shared" / "git" / "default.gitconfig"
    github_email = run_git("config", "--file", str(default_config), "user.email")
    if not github_email:
        errors.append("No GitHub email in _shared/git/default.gitconfig")
    if (ROOT / ".git").exists() and run_git("-C", str(ROOT), "symbolic-ref", "--short", "HEAD") != "main":
        errors.append("~/lala must be on branch main")

    lane = ROOT / "01_build-app"
    if not (lane / "CONTEXT.md").is_file():
        errors.append("Missing 01_build-app/CONTEXT.md")
    for stage in STAGES:
        if not (lane / stage / "CONTEXT.md").is_file():
            errors.append(f"Missing stage contract: {stage}")

    for name, fixed_email in AREA_EMAILS.items():
        area = ROOT / "areas" / name
        email = fixed_email or github_email
        check_entry(area, errors)
        if not (area / ".git").exists():
            errors.append(f"{name} is not a Git repo")
        else:
            actual = run_git("-C", str(area), "config", "user.email")
            if actual != email:
                errors.append(f"{name} commits as {actual!r}, expected {email!r}")

    for home in (HOME / ".claude" / "skills", HOME / ".agents" / "skills"):
        for skill in SYSTEM_SKILLS:
            link = home / skill
            target = ROOT / "_skills" / "system" / skill
            if not link.is_symlink() or link.resolve() != target.resolve():
                errors.append(f"{link} must be a symlink to {target}")
            elif not (link / "SKILL.md").is_file():
                errors.append(f"{link} has no SKILL.md")

    for path in (ROOT / "_skills").rglob("*"):
        if path.is_file() and path.suffix in {".md", ".py", ".yaml"}:
            text = path.read_text(encoding="utf-8")
            for ref in OLD_REFS:
                if ref in text:
                    errors.append(f"Old reference {ref!r} in {path.relative_to(ROOT)}")

    for path in [ROOT / "CLAUDE.md", ROOT / "CONTEXT.md", *lane.rglob("CONTEXT.md")]:
        if "TODO" in path.read_text(encoding="utf-8"):
            errors.append(f"Unresolved TODO in {path.relative_to(ROOT)}")

    if errors:
        print("LALA WORKSPACE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("LALA WORKSPACE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
