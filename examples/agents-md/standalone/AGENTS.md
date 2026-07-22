# Project Guidance

Follow the global prompt rules first. This file only adds project-specific skill routing.

## Skill Routing

- When writing, modifying, or reviewing code, apply `coding-quality-guardrails` as the quality gate.
- When debugging bugs, regressions, flaky behavior, or failing tests, use `diagnosing-bugs` before changing behavior.
- Before implementing new logic with branching, side effects, resource lifecycles, or ordering constraints, use `flow-design` and keep the design note in the task workspace.
- When designing module boundaries, refactoring, or shaping interfaces, use `codebase-design`.
- When aligning terminology or modeling the domain, use `domain-modeling`.
- When a plan is fuzzy, high-impact, or lacks testable acceptance criteria, use `planning-grill` to sharpen scope, acceptance, and failure modes before execution. Run it before `decompose-and-dispatch` only when delegated or coordinated work is needed.
- For multi-step or multi-agent work, use `decompose-and-dispatch` to split the work into bounded units. Use `execute-dispatch-unit` only for a clearly assigned unit with scope, dependencies, and verification.
- When preparing context for human or AI code review, use `ready-code-review`; do not use it to perform the review itself.
- After a new abstraction causes 3+ follow-up regressions, or after tests pass and before commit when the change adds persisted fields, interface methods, lifecycle states, or compatibility branches, use `overengineering-review` to check for unnecessary complexity.
- To record a session, distill completed work into a replayable recipe, or replay a `recipe.yaml`, use `session-recipe`.
- After a non-trivial task, review cycle, bug fix, or debugging session is verified, use `compound-learning` to capture reusable learnings and maintain `docs/solutions/`.

## Project Notes

<!-- Add project-specific build/test commands, danger zones, and conventions here. -->
