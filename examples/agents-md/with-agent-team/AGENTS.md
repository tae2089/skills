# Project Guidance

Follow the global prompt rules first. This file adds project-specific skill routing for a project that uses the `agent-team` CLI (github.com/tae2089/agent-team) as its durable work ledger.

## Skill Routing

- When writing, modifying, or reviewing code, apply `coding-quality-guardrails` as the quality gate.
- When debugging bugs, regressions, flaky behavior, or failing tests, use `diagnosing-bugs` before changing behavior.
- Before implementing new logic with branching, side effects, resource lifecycles, or ordering constraints, use `flow-design` and keep the design note in the task workspace.
- When designing module boundaries, refactoring, or shaping interfaces, use `codebase-design`.
- When aligning terminology or modeling the domain, use `domain-modeling`.
- When a plan is fuzzy, high-impact, or lacks testable acceptance criteria, use `planning-grill` to reach a shared understanding of scope, acceptance, and failure modes before execution. It writes no files.
- Before editing any project file, use `to-spec` to record the contract and design. It picks the backend once — local `_workspace/`, Jira + Confluence, or GitHub Issues — and caches it in `_workspace/.tracker`.
- When the spec covers more than one reviewable chunk, use `to-issues` to cut it into ordered work units with acceptance and a verification command each.
- For multi-step or multi-agent work, use `decompose-and-dispatch` to run those units — one subagent per unit, in dependency order.
- When preparing context for human or AI code review, use `ready-code-review`; do not use it to perform the review itself.
- After a new abstraction causes 3+ follow-up regressions, or after tests pass and before commit when the change adds persisted fields, interface methods, lifecycle states, or compatibility branches, use `overengineering-review` to check for unnecessary complexity.
- After a non-trivial task, review cycle, bug fix, or debugging session is verified, use `compound-learning` to capture reusable learnings and maintain `docs/solutions/`.

## agent-team Routing

agent-team bundles its own skills; restrict them as follows so methodology stays single-sourced:

- Use only agent-team's CLI operation skills (the `agent-team-*` prefix: run/task/message/inbox/sync/event commands), and load `agent-team-shared` before any command-specific one — it defines the state directory, global flags, and error handling they all assume. Never use its `recipe-*` and `persona-*` skills — the skills routed above own all methodology, even where an excluded skill looks like a closer match (plan sharpening / `recipe-agent-team-planning-grill` → `planning-grill`; work breakdown → `to-issues`; delegated execution → `decompose-and-dispatch`; architecture → `codebase-design`; terminology → `domain-modeling`; compound learning / `recipe-agent-team-compound-learning` → `compound-learning`).
- The work units live in the backend `to-spec` chose, not in the agent-team ledger. Use the `agent-team-*` commands for run/task registration and messaging on top of those units; never let them re-decompose the work.
- Do not route by the word "recipe": agent-team's `recipe-*` skills are excluded above.

## Project Notes

<!-- Add project-specific build/test commands, danger zones, and conventions here. -->
