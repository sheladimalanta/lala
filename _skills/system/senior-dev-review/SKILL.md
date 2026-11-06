---
name: senior-dev-review
description: Run an evidence-first senior engineering review of a codebase, workflow, agent, app, script, integration, or production-readiness claim. Use when the user asks for a senior dev, senior developer, senior engineer, code review, architecture review, robustness review, launch readiness, production-grade check, risk review, or wants a Senior Dev + Ponytail check. Do NOT use for writing new features or for routine edits.
---

# Senior Dev Review

## First Move

Find the project before reviewing:

1. Read the area's `CONTEXT.md` and the project's `notes.md`.
2. If a repo-specific `README.md`, `CLAUDE.md`, `AGENTS.md`, `SKILL.md`, review doc, security doc, or runbook exists, read it before judging.

Do not review from filenames alone. Do not call something production-ready without running or naming the verifier.

## Review Workflow

1. Summarize the intended system behavior and current state from source files.
2. Inspect the implementation path, tests, configs, deployment/runtime assumptions, credentials path, and user-facing workflow.
3. Run the available verifiers in the repo. If a verifier cannot run, record the exact blocker.
4. Review for:
   - correctness and edge cases
   - security and privacy boundaries
   - data ownership and customer-data leakage
   - operational failure modes
   - dependency and environment drift
   - test coverage and observability
   - launch/readiness gaps
5. Apply `~/lala/_shared/PONYTAIL-GATES.md` when the review involves production readiness, new dependencies, migration, reusable scripts, skills, workflows, or external integrations.

## Output Shape

Lead with findings, ordered by severity. Use file and line references when reviewing code.

Include:

- Verification actually run
- Blocked checks
- Readiness verdict
- Top risks
- Smallest next action that improves production readiness

If writing a review artifact, put it in the target project repo or requested output folder.

## Rubric

Score or judge only after evidence collection:

- Architecture fit: Does the design match the job?
- Code quality: Is the implementation simple, maintainable, and bounded?
- Behavioral correctness: Does it handle real and edge inputs?
- Security/privacy: Are secrets, auth, customer data, and destructive actions controlled?
- Operations: Can it be run, monitored, recovered, and verified?
- User impact: Does the workflow protect Lala's reputation and avoid embarrassing output?

## Stop Conditions

Stop and report if the review depends on credentials, private data, or production access that cannot be read or tested safely. Do not invent a pass.
