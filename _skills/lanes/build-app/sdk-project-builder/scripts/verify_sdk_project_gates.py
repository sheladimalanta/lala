#!/usr/bin/env python3
"""Verify the project-local Claude/OpenAI SDK build gates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


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

CONTRACT_MARKER = "SDK-PROJECT-BUILD-CONTRACT:START"
EXPECTED_STATUS = {
    "grill": "complete",
    "spec": "approved",
    "tickets": "ready",
    "sdk_facts": "verified",
    "tests": "passed",
    "evals": "passed",
    "code_review": "passed",
    "happy_path": "passed",
}
IMPLEMENTATION_GATES = ("grill", "spec", "tickets", "sdk_facts")
DONE_GATES = (
    "grill",
    "spec",
    "tickets",
    "sdk_facts",
    "tests",
    "evals",
    "code_review",
    "happy_path",
)
OFFICIAL_DOMAINS = {
    "claude": {
        "docs.anthropic.com",
        "docs.claude.com",
        "platform.claude.com",
        "code.claude.com",
    },
    "openai": {
        "developers.openai.com",
        "platform.openai.com",
        "learn.chatgpt.com",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify setup, implementation, or done gates for an SDK project."
    )
    parser.add_argument(
        "--project",
        type=Path,
        default=Path.cwd(),
        help="Project root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--stage",
        choices=("setup", "implementation", "done"),
        required=True,
        help="Gate stage to verify.",
    )
    return parser.parse_args()


def read_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing state file: {path}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"State must be a JSON object: {path}")
        return {}
    return value


def check_inside_project(root: Path, raw: str, errors: list[str]) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        errors.append("Evidence path must be a non-empty string")
        return None
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        errors.append(f"Evidence path escapes the project: {raw}")
        return None
    return candidate


def check_setup(root: Path, state: dict, errors: list[str]) -> None:
    if not (root / ".git").exists():
        errors.append("Project root is not a git repository")

    for skill in REQUIRED_SKILLS:
        canonical = root / ".agents" / "skills" / skill / "SKILL.md"
        if not canonical.is_file():
            errors.append(f"Missing project skill: {canonical.relative_to(root)}")
        claude_link = root / ".claude" / "skills" / skill
        if not claude_link.exists():
            errors.append(f"Missing Claude skill link: {claude_link.relative_to(root)}")
        elif claude_link.resolve() != canonical.parent.resolve():
            errors.append(
                f"Claude skill does not point to canonical source: "
                f"{claude_link.relative_to(root)}"
            )

    lock_path = root / "skills-lock.json"
    lock = read_json(lock_path, errors)
    installed = lock.get("skills", {}) if isinstance(lock, dict) else {}
    for skill in REQUIRED_SKILLS:
        if skill not in installed:
            errors.append(f"skills-lock.json does not contain: {skill}")

    instruction_paths = (root / "CLAUDE.md", root / "AGENTS.md")
    for path in instruction_paths:
        if not path.exists():
            errors.append(f"Missing project instructions: {path.name}")
            continue
        instruction_text = path.read_text(encoding="utf-8")
        if CONTRACT_MARKER not in instruction_text:
            errors.append(f"Missing SDK build contract in {path.name}")
        if "## Agent skills" not in instruction_text:
            errors.append(f"Matt setup has not added the Agent skills block to {path.name}")

    required_files = (
        root / "docs" / "agents" / "sdk-build-state.json",
        root / "docs" / "agents" / "sdk-facts.md",
        root / "docs" / "agents" / "issue-tracker.md",
        root / "docs" / "agents" / "domain.md",
        root / "evals" / "README.md",
        root / "scripts" / "verify_sdk_project_gates.py",
    )
    for path in required_files:
        if not path.is_file():
            errors.append(f"Missing SDK build-system file: {path.relative_to(root)}")

    if (root / ".agents" / "skills" / "triage" / "SKILL.md").is_file():
        triage_config = root / "docs" / "agents" / "triage-labels.md"
        if not triage_config.is_file():
            errors.append(
                f"Installed triage skill needs configuration: "
                f"{triage_config.relative_to(root)}"
            )

    providers = state.get("providers")
    if not isinstance(providers, list):
        errors.append("State providers must be a list; empty means a non-AI app")
    else:
        invalid = sorted(set(providers) - set(OFFICIAL_DOMAINS))
        if invalid:
            errors.append(f"Unsupported state providers: {', '.join(invalid)}")

    attempts = state.get("failed_fix_attempts")
    if not isinstance(attempts, int) or attempts < 0:
        errors.append("failed_fix_attempts must be a non-negative integer")
    elif attempts >= 2:
        errors.append(
            "Two failed fix attempts are recorded. Stop implementation and re-diagnose."
        )


def evidence_paths(root: Path, gate: str, value: dict, errors: list[str]) -> list[Path]:
    raw_evidence = value.get("evidence")
    if not isinstance(raw_evidence, list) or not raw_evidence:
        errors.append(f"Gate {gate} needs at least one evidence path")
        return []
    paths: list[Path] = []
    for raw in raw_evidence:
        path = check_inside_project(root, raw, errors)
        if path is None:
            continue
        if not path.is_file():
            errors.append(f"Gate {gate} evidence does not exist: {raw}")
            continue
        paths.append(path)
    return paths


def official_domains_in(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    domains: set[str] = set()
    for token in text.replace("(", " ").replace(")", " ").split():
        if not token.startswith(("https://", "http://")):
            continue
        cleaned = token.rstrip(".,;|]>")
        hostname = urlparse(cleaned).hostname
        if hostname:
            domains.add(hostname.lower())
    return domains


def check_gate(
    root: Path,
    state: dict,
    gate: str,
    errors: list[str],
) -> None:
    gates = state.get("gates")
    if not isinstance(gates, dict):
        errors.append("State gates must be an object")
        return
    value = gates.get(gate)
    if not isinstance(value, dict):
        errors.append(f"Missing gate state: {gate}")
        return
    expected = EXPECTED_STATUS[gate]
    if value.get("status") != expected:
        errors.append(
            f"Gate {gate} status must be {expected!r}, found {value.get('status')!r}"
        )
        return
    paths = evidence_paths(root, gate, value, errors)

    if gate == "spec" and value.get("approved_by_lala") is not True:
        errors.append("Spec gate requires approved_by_lala=true")

    if gate == "sdk_facts" and paths:
        providers = state.get("providers", [])
        found: set[str] = set()
        for path in paths:
            found.update(official_domains_in(path))
        for provider in providers:
            allowed = OFFICIAL_DOMAINS.get(provider, set())
            if not found.intersection(allowed):
                errors.append(
                    f"SDK facts contain no official {provider} documentation URL"
                )


def main() -> int:
    args = parse_args()
    root = args.project.expanduser().resolve()
    errors: list[str] = []
    state_path = root / "docs" / "agents" / "sdk-build-state.json"
    state = read_json(state_path, errors)
    check_setup(root, state, errors)

    # A non-AI app has no SDK claims to source and no model output to evaluate.
    skip = {"sdk_facts", "evals"} if state.get("providers") == [] else set()
    if args.stage in {"implementation", "done"}:
        for gate in IMPLEMENTATION_GATES:
            if gate not in skip:
                check_gate(root, state, gate, errors)
    if args.stage == "done":
        for gate in DONE_GATES:
            if gate not in IMPLEMENTATION_GATES and gate not in skip:
                check_gate(root, state, gate, errors)

    if errors:
        print(f"SDK PROJECT GATE: FAIL ({args.stage})")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"SDK PROJECT GATE: PASS ({args.stage})")
    print(f"Project: {root}")
    print(f"Skills: {len(REQUIRED_SKILLS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
