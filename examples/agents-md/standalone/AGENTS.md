# Project Guidance

Follow the global prompt rules first. This file only adds project-specific skill routing.

## Skill Routing

- When writing, modifying, or reviewing code, apply `coding-quality-guardrails` as the quality gate.
- When debugging bugs, regressions, flaky behavior, or failing tests, use `diagnosing-bugs` before changing behavior.
- Before implementing new logic with branching, side effects, resource lifecycles, or ordering constraints, use `flow-design` and keep the design note in the task workspace.
- When designing module boundaries, refactoring, or shaping interfaces, use `codebase-design`.
- When aligning terminology or modeling the domain, use `domain-modeling`.
- When a plan is fuzzy, high-impact, or lacks testable acceptance criteria, use `planning-grill` to reach a shared understanding of scope, acceptance, and failure modes before execution. It writes no files.
- When the user explicitly asks for a spec, PRD, or design doc, use `to-spec`; it synthesizes what the conversation already settled — problem, solution, user stories, implementation and testing decisions — and publishes one spec to the destination configured in `.scratch/.tracker`. It does not create the work breakdown.
- When the user explicitly asks for the work breakdown, use `to-issues`; it cuts that spec into tracer-bullet tickets with blocking edges and publishes them to the same destination.
- When preparing context for human or AI code review, use `ready-code-review`; do not use it to perform the review itself.
- After a new abstraction causes 3+ follow-up regressions, or after tests pass and before commit when the change adds persisted fields, interface methods, lifecycle states, or compatibility branches, use `overengineering-review` to check for unnecessary complexity.
- After a non-trivial task, review cycle, bug fix, or debugging session is verified, use `compound-learning` to capture reusable learnings and maintain `docs/solutions/`.

## Issue Tracker

- `.scratch/.tracker`, `.scratch/*/spec.md`, and `.scratch/*/issues/` are shared in version control and must not be ignored. The configuration selects one destination for both `to-spec` and `to-issues`.
- Use `provider: local`, `provider: github`, `provider: gitlab`, or `provider: jira`. Remote providers also require `target: <repository-or-project>`.
- With `provider: jira`, add `spec-target: <site>/wiki/spaces/<SPACE>` to keep the spec in Confluence. `to-spec` then creates a seed index page on first use, the spec page under it, and one Jira parent issue that links the page — at the project's default standard issue type, never an epic. Without the key the spec stays a Jira issue.
- Add `ready-label: <label>` only when new specs and tickets should receive that label. With no key, neither skill applies a label.
- If the file is missing or the configured remote tool is unavailable, both skills preview a fallback to `.scratch/<feature-slug>/` — `spec.md` for the spec, `issues/` for the tickets — and write only after approval.
- Never put tokens, passwords, private keys, webhook URLs, or credential-bearing connection strings in `.scratch/.tracker`.

## Delegating To Subagents

Applies whenever work units are handed to subagents, in dependency order.

- Parallel subagents each get their own git worktree. Never two writers in one working tree.
- A worktree copies the repo, not the world — the same database, port, or external service still collides. Run those units in sequence.
- Two units can pass alone and break together with no file in common: one renames a symbol, the other calls the old name. Run the project's whole verification once on the merged tree.
- Do not merge the branches. Report them, and say the merged-tree verification still has to run.
- Copy the parent's Out of Scope — whatever the spec or ticket calls its not-doing list — into the subagent prompt verbatim; link everything else. A subagent already building the wrong thing does not follow a link.
- A subagent claiming success without the verification output has not finished. Re-dispatch it.
- Running every unit yourself in dependency order is a valid plan, not a failed delegation.

## Project Notes

<!-- Add project-specific build/test commands, danger zones, and conventions here. -->
