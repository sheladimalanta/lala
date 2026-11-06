---
name: sdk-project-builder
description: Set up and govern a software project through verified gates, whether it uses the Claude SDK, Anthropic API, OpenAI SDK, OpenAI API, AI agents, tool calling, or no AI at all. Opened by path from the 01_build-app lane. Do not use for the established newsletter, blog, YouTube, Writings by Lala, or other content-production workflows.
---

# SDK Project Builder

Apply the project-local build system described here and in
`references/build-contract.md`.

## Start

1. Read the target repository's `AGENTS.md`, `CLAUDE.md`, brief, and current
   git state.
2. Confirm the task is software work. Keep newsletter and blog workflows out
   of this lane.
3. Apply the Ponytail gate before adding project surface.
4. Bootstrap an unconfigured repository with:

   `python3 <skill-dir>/scripts/bootstrap_sdk_project.py PROJECT --provider PROVIDER`

   Use `claude`, `openai`, or `both` for `PROVIDER`. Use `none` for an app with
   no AI features, which skips the SDK facts and evals gates only.
5. Run the setup gate:

   `python3 PROJECT/scripts/verify_sdk_project_gates.py --project PROJECT --stage setup`

## Build flow

Open and follow the actual project-local Matt Pocock skill at every step.
Never reconstruct a skill from memory.

1. Run `setup-matt-pocock-skills` once per repository.
2. Use `research` for SDK facts. Record every material SDK claim in
   `docs/agents/sdk-facts.md` with an official source.
3. Use `grill-with-docs` until the important decisions and vocabulary are
   resolved.
4. Use `to-spec`, then obtain Lala's approval.
5. Use `to-tickets`.
6. Run the implementation gate. Do not write product code unless it passes.
7. Use `tdd` and `implement`, one ticket at a time.
8. Use `diagnosing-bugs` for failures. After two failed fix attempts, stop,
   reset the diagnosis, and return to the relevant earlier phase.
9. Use `code-review`.
10. Run tests, output-quality evals, and one real happy path.
11. Run the done gate before reporting completion.

## Gates

The project state file is `docs/agents/sdk-build-state.json`.

- Before implementation:
  `python3 scripts/verify_sdk_project_gates.py --stage implementation`
- Before completion:
  `python3 scripts/verify_sdk_project_gates.py --stage done`

Update the state file only from directly observed evidence. Every completed
gate requires one or more existing evidence files inside the project.

## Source rules

- For Claude SDK/API claims, use current official Anthropic or Claude
  documentation.
- For OpenAI SDK/API claims, use the OpenAI developer documentation route.
- With provider `none`, record material claims about other services in the spec
  with their official docs.
- If a material SDK fact cannot be cited, stop and research it.
- Do not treat a passing unit test as proof of output quality.

## Done gate

Before saying the project is complete:

1. Re-read this skill and the project contract.
2. Run the `done` verifier.
3. Confirm the verifier reports `PASS`.
4. Report any unresolved product, security, or deployment risk.

