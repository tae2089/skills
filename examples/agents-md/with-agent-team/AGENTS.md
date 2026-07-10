# Project Guidance

Follow the global prompt rules first. This file adds project-specific skill routing for a project that uses the `agent-team` CLI (github.com/tae2089/agent-team) as its durable work ledger.

## Skill Routing

- When writing, modifying, or reviewing code, apply `coding-quality-guardrails` as the quality gate.
- When debugging bugs, regressions, flaky behavior, or failing tests, use `diagnosing-bugs` before changing behavior.
- Before implementing new logic with branching, side effects, resource lifecycles, or ordering constraints, use `flow-design` and keep the design note in the task workspace.
- When designing module boundaries, refactoring, or shaping interfaces, use `codebase-design`.
- When aligning terminology or modeling the domain, use `domain-modeling`.
- For multi-step or multi-agent work, use `decompose-and-dispatch` to split the work into bounded units. Use `execute-dispatch-unit` only for a clearly assigned unit with scope, dependencies, and verification.
- When preparing context for human or AI code review, use `ready-code-review`; do not use it to perform the review itself.
- To record a session, distill completed work into a replayable recipe, or replay a `recipe.yaml`, use `session-recipe`.

## agent-team Routing

agent-team bundles its own skills; restrict them as follows so methodology stays single-sourced:

- Use only agent-team's CLI operation skills (the `agent-team-*` prefix: run/task/message/inbox/sync/event commands), and load `agent-team-shared` before any command-specific one — it defines the state directory, global flags, and error handling they all assume. Never use its `recipe-*` and `persona-*` skills — the skills routed above own all methodology, even where an excluded skill looks like a closer match (worker checkpoints → `execute-dispatch-unit`'s Ledger Checkpoints; planning → `decompose-and-dispatch`; architecture → `codebase-design`; terminology → `domain-modeling`).
- When executing an assigned unit, follow `execute-dispatch-unit` for scope, verification, and reporting; its Ledger Checkpoints section defines which `agent-team-*` calls to make.
- When planning, `decompose-and-dispatch` owns decomposition and executor mapping, and its Durable Ledger section defines the run/task registration calls.
- Do not route by the word "recipe": here it means a replayable session recipe (`session-recipe`, `recipe.yaml`); agent-team's `recipe-*` skills are excluded above.

## Project Notes

<!-- Add project-specific build/test commands, danger zones, and conventions here. -->
