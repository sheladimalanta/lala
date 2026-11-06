# SDK Project Build System

## Scope

Use this system for software projects, including:

- Claude SDK or Anthropic API
- OpenAI SDK or OpenAI API
- AI agents and tool use
- AI-backed applications and integrations
- Apps with no AI features, using provider `none`

Do not route established newsletter, blog, YouTube, Writings by Lala, or
other working content-production workflows through this system.

## Architecture

The `sdk-project-builder` skill routes the work. Matt Pocock's source skills remain local to
each SDK project:

```text
project/
├── .agents/skills/
├── .claude/skills/
├── skills-lock.json
├── CLAUDE.md
├── AGENTS.md
├── docs/agents/
│   ├── sdk-build-state.json
│   └── sdk-facts.md
├── evals/
└── scripts/verify_sdk_project_gates.py
```

`.agents/skills/` is the project-local source used by Codex.
`.claude/skills/` contains Claude Code links to the same source.
`skills-lock.json` records the installed upstream skills.

The selected engineering set is:

- `setup-matt-pocock-skills`
- `ask-matt`
- `research`
- `grill-with-docs`
- `to-spec`
- `to-tickets`
- `tdd`
- `implement`
- `diagnosing-bugs`
- `code-review`

Add `wayfinder` or `prototype` only when a project actually needs them.

## Required flow

```text
Ponytail
  -> setup
  -> official-doc research
  -> grill-with-docs
  -> approved spec
  -> tickets
  -> implementation gate
  -> TDD and implementation
  -> code review
  -> tests and evals
  -> real happy path
  -> done gate
```

## Human decisions

Lala approves the specification and any material scope change. The agent may
research facts and recommend an answer, but it must not invent product
requirements or SDK behavior.

## Evidence gates

The verifier checks three stages:

- `setup`: project-local skills, Claude/Codex parity, instructions, state,
  SDK-facts register, and eval surface exist.
- `implementation`: grilling, approved specification, tickets, and official
  SDK-fact evidence exist.
- `done`: tests, output-quality evals, code review, and one real happy-path
  operation have passing evidence.

Every completed state requires an existing project-relative evidence file.
Booleans without evidence do not pass.

## Enforcement boundary

This version uses an explicit deterministic verifier. It does not install a
global lock or modify Claude Code hooks. A blocking hook may be considered
only after the verifier has completed a warning-first pilot and Lala
separately approves the hook.

## Failure rule

After two failed fix attempts on the same change:

1. Stop editing.
2. Record the failed attempts.
3. Re-open `diagnosing-bugs`.
4. Re-check the SDK facts and the originating specification.
5. Return to grilling or specification when the failure exposes a missing
   decision.

