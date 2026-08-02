# Project Guidance

Follow the global prompt rules first. This file adds project-specific skill routing for a project that uses the `agent-team` CLI (github.com/tae2089/agent-team) as its durable work ledger.

## Skill Routing

- When writing, modifying, or reviewing code, apply `coding-quality-guardrails` as the quality gate.
- When debugging bugs, regressions, flaky behavior, or failing tests, use `diagnosing-bugs` before changing behavior.
- Before implementing new logic with branching, side effects, resource lifecycles, or ordering constraints, use `flow-design` and keep the design note in the task workspace.
- When designing module boundaries, refactoring, or shaping interfaces, use `codebase-design`.
- When aligning terminology or modeling the domain, use `domain-modeling`.
- When a plan is fuzzy, high-impact, or lacks testable acceptance criteria, use `planning-grill` to reach a shared understanding of scope, acceptance, and failure modes before execution. It writes no files.
- Before editing any project file, use `to-spec` to write the spec — problem, solution, user stories, and implementation decisions. It always writes `_workspace/<task-name>/`; publishing to a tracker is a separate step, only when this file names one or the user asks.
- When the spec covers more than one reviewable chunk, use `to-issues` to cut it into ordered work units, each covering user stories by number and carrying its own verification command.
- When preparing context for human or AI code review, use `ready-code-review`; do not use it to perform the review itself.
- After a new abstraction causes 3+ follow-up regressions, or after tests pass and before commit when the change adds persisted fields, interface methods, lifecycle states, or compatibility branches, use `overengineering-review` to check for unnecessary complexity.
- After a non-trivial task, review cycle, bug fix, or debugging session is verified, use `compound-learning` to capture reusable learnings and maintain `docs/solutions/`.

## Delegating To Subagents

Applies whenever work units are handed to subagents, in dependency order.

- Parallel subagents each get their own git worktree. Never two writers in one working tree.
- A worktree copies the repo, not the world — the same database, port, or external service still collides. Run those units in sequence.
- Two units can pass alone and break together with no file in common: one renames a symbol, the other calls the old name. Run the project's whole verification once on the merged tree.
- Do not merge the branches. Report them, and say the merged-tree verification still has to run.
- Copy the parent's Out of Scope — whatever the spec or ticket calls its not-doing list — into the subagent prompt verbatim; link everything else. A subagent already building the wrong thing does not follow a link.
- A subagent claiming success without the verification output has not finished. Re-dispatch it.
- Running every unit yourself in dependency order is a valid plan, not a failed delegation.

## agent-team Routing

agent-team bundles its own skills; restrict them as follows so methodology stays single-sourced:

- Use only agent-team's CLI operation skills (the `agent-team-*` prefix: run/task/message/inbox/sync/event commands), and load `agent-team-shared` before any command-specific one — it defines the state directory, global flags, and error handling they all assume. Never use its `recipe-*` and `persona-*` skills — the skills routed above own all methodology, even where an excluded skill looks like a closer match (plan sharpening / `recipe-agent-team-planning-grill` → `planning-grill`; work breakdown → `to-issues`; delegated execution → the Delegating To Subagents rules above; architecture → `codebase-design`; terminology → `domain-modeling`; compound learning / `recipe-agent-team-compound-learning` → `compound-learning`).
- The work units live in the spec `to-spec` wrote — `_workspace/<task-name>/task.md`, and the tracker if it was published — not in the agent-team ledger. Use the `agent-team-*` commands for run/task registration and messaging on top of those units; never let them re-decompose the work.
- Do not route by the word "recipe": agent-team's `recipe-*` skills are excluded above.

## Project Notes

<!-- Add project-specific build/test commands, danger zones, and conventions here. -->
