#!/usr/bin/env python3
"""Bootstrap the project-local SDK build system without overwriting evidence."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_SKILLS = (
    "setup-matt-pocock-skills",
    "ask-matt",
    "research",
    "grill-with-docs",
    "to-spec",
    "to-tickets",
    "tdd",
    "implement",
    "diagnosing-bugs",
    "code-review",
)
START_MARKER = "<!-- SDK-PROJECT-BUILD-CONTRACT:START -->"
END_MARKER = "<!-- SDK-PROJECT-BUILD-CONTRACT:END -->"
FORBIDDEN_FRAGMENTS = (
    "cobalt-skills/newsletter-writing-automation",
    "cobalt-skills/blog-creation-system",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap a project-local Claude/OpenAI SDK build system."
    )
    parser.add_argument("project", type=Path, help="Existing git repository root")
    parser.add_argument(
        "--provider",
        choices=("claude", "openai", "both", "none"),
        required=True,
        help="SDK provider whose official docs must support technical claims; none for a non-AI app",
    )
    parser.add_argument(
        "--skip-skill-install",
        action="store_true",
        help="Create local gate files without invoking the skills installer",
    )
    return parser.parse_args()


def providers_for(value: str) -> list[str]:
    if value == "both":
        return ["claude", "openai"]
    if value == "none":
        return []
    return [value]


def reject_wrong_scope(root: Path) -> None:
    rendered = root.as_posix()
    if (root / "_skills").is_dir() or (root / "_templates").is_dir():
        raise ValueError("The workspace root is the router, not a project target")
    for fragment in FORBIDDEN_FRAGMENTS:
        if fragment in rendered:
            raise ValueError(f"Content workflow is excluded from this system: {fragment}")
    if not (root / ".git").exists():
        raise ValueError(f"Target is not a git repository: {root}")


def write_if_absent(path: Path, content: str) -> str:
    if path.exists():
        return "preserved"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "created"


def managed_contract_block() -> str:
    return f"""{START_MARKER}
## SDK Project Build Contract

This contract applies to software engineering work in this project. It does
not replace the newsletter, blog, or other established content workflows.

- Read the project brief and `docs/agents/sdk-build-state.json` first.
- Open the actual skill under `.agents/skills/` before following it.
- Use: setup, research, grill-with-docs, approved spec, tickets, TDD,
  implementation, code review, tests, evals, and a real happy path.
- Record material SDK claims in `docs/agents/sdk-facts.md` with official docs,
  unless the state file lists no providers.
- Before product code, run:
  `python3 scripts/verify_sdk_project_gates.py --stage implementation`
- Before reporting completion, run:
  `python3 scripts/verify_sdk_project_gates.py --stage done`
- After two failed fix attempts, stop editing and restart diagnosis.
{END_MARKER}
"""


def update_instruction(path: Path) -> str:
    current = path.read_text(encoding="utf-8") if path.exists() else "# Project\n"
    block = managed_contract_block()
    if START_MARKER in current and END_MARKER in current:
        before, remainder = current.split(START_MARKER, 1)
        _, after = remainder.split(END_MARKER, 1)
        updated = before.rstrip() + "\n\n" + block + after.lstrip("\n")
    else:
        updated = current.rstrip() + "\n\n" + block
    if updated == current:
        return "unchanged"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(updated, encoding="utf-8")
    return "updated" if path.exists() else "created"


def update_project_instructions(root: Path) -> list[str]:
    claude = root / "CLAUDE.md"
    agents = root / "AGENTS.md"
    if not claude.exists():
        claude.write_text("# Project\n", encoding="utf-8")
    if not agents.exists():
        agents.symlink_to("CLAUDE.md")

    unique: dict[Path, Path] = {}
    for path in (claude, agents):
        unique[path.resolve()] = path.resolve()
    results = []
    for resolved in unique.values():
        results.append(f"{resolved.name}: {update_instruction(resolved)}")
    return results


def install_missing_skills(root: Path, skip: bool) -> list[str]:
    missing = []
    for skill in REQUIRED_SKILLS:
        canonical = root / ".agents" / "skills" / skill / "SKILL.md"
        claude = root / ".claude" / "skills" / skill
        if not canonical.is_file() or not claude.exists():
            missing.append(skill)
    if not missing or skip:
        return missing
    command = [
        "npx",
        "skills",
        "add",
        "mattpocock/skills",
        "--skill",
        *missing,
        "--agent",
        "codex",
        "claude-code",
        "-y",
    ]
    subprocess.run(command, cwd=root, check=True)
    return []


def initial_state(providers: list[str]) -> str:
    gate_names = (
        "grill",
        "spec",
        "tickets",
        "sdk_facts",
        "tests",
        "evals",
        "code_review",
        "happy_path",
    )
    gates = {
        name: {
            "status": "pending",
            "evidence": ["docs/agents/sdk-facts.md"] if name == "sdk_facts" else [],
        }
        for name in gate_names
    }
    gates["spec"]["approved_by_lala"] = False
    state = {
        "schema_version": 1,
        "providers": providers,
        "phase": "grilling",
        "failed_fix_attempts": 0,
        "gates": gates,
        "notes": [],
    }
    return json.dumps(state, indent=2) + "\n"


def sdk_facts_template(providers: list[str]) -> str:
    if not providers:
        return "# SDK Facts\n\nThis project uses no AI provider, so this gate does not apply.\n"
    provider_label = ", ".join(providers)
    return f"""# SDK Facts

Providers: {provider_label}

Record every material SDK fact used by the specification or implementation.
Use current official documentation. Do not write remembered facts as verified.

| Claim | Provider | Official source URL | Checked date | Used by |
|---|---|---|---|---|
| Replace this row with a verified claim. | {providers[0]} |  |  |  |
"""


def evals_template() -> str:
    return """# Project Evals

Store the golden cases and output-quality checks for this SDK project here.

The done gate requires:

- a passing test evidence file
- a passing eval evidence file
- a code-review evidence file
- a real happy-path evidence file

Structural tests alone do not prove AI output quality.
"""


def main() -> int:
    args = parse_args()
    root = args.project.expanduser().resolve()
    reject_wrong_scope(root)
    providers = providers_for(args.provider)

    missing = install_missing_skills(root, args.skip_skill_install)
    if missing and args.skip_skill_install:
        print("Skill installation skipped. Setup verification will remain blocked.")

    source_verifier = Path(__file__).with_name("verify_sdk_project_gates.py")
    target_verifier = root / "scripts" / "verify_sdk_project_gates.py"
    target_verifier.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_verifier, target_verifier)
    os.chmod(target_verifier, 0o755)

    actions = [
        f"sdk-build-state.json: {write_if_absent(root / 'docs/agents/sdk-build-state.json', initial_state(providers))}",
        f"sdk-facts.md: {write_if_absent(root / 'docs/agents/sdk-facts.md', sdk_facts_template(providers))}",
        f"evals/README.md: {write_if_absent(root / 'evals/README.md', evals_template())}",
        "verifier: installed",
        *update_project_instructions(root),
    ]
    print("SDK project bootstrap complete")
    print(f"Project: {root}")
    for action in actions:
        print(f"- {action}")
    print(
        "Next: run setup-matt-pocock-skills, then verify with "
        "python3 scripts/verify_sdk_project_gates.py --stage setup"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"SDK project bootstrap failed: {exc}", file=sys.stderr)
        sys.exit(1)

