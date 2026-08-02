# Project Guidance

Follow the global prompt rules first. This file only adds repository-specific routing.

## Skill Routing

- When creating or revising a `SKILL.md`, use `writing-great-skills` first to keep invocation metadata, progressive disclosure, completion criteria, and references predictable.
- When modifying skill instructions, references, examples, or scripts, use `coding-quality-guardrails` as the quality gate for small, reviewable diffs and honest verification.
- When a skill change introduces branching workflow, side effects, ordering constraints, or a new multi-step procedure, use `flow-design` before editing and keep the pseudocode or design note in the task workspace.
- When a change reshapes skill boundaries, splits or merges references, changes reusable interfaces, or affects how multiple skills compose, use `codebase-design` before editing.
- When one change triggers both `flow-design` and `codebase-design`, run both: draft the flow with `flow-design` first, then use `codebase-design` to shape the interfaces the flow's operations require.
- When debugging a broken skill workflow, failing validation, confusing invocation, or reported regression, use `diagnosing-bugs` before changing behavior.
- When preparing a skill package for human or AI review, use `ready-code-review` to produce context, non-goals, severity policy, and false-positive suppressions before asking for findings.
- After a skill change adds a new abstraction that causes 3+ follow-up regressions, or after its tests pass and before commit when it adds persisted fields, interface methods, lifecycle states, or compatibility branches, use `overengineering-review` to check for unnecessary complexity.
- When the skill change is fuzzy, high-impact, or lacks testable acceptance criteria, use `planning-grill` to reach a shared understanding of scope, acceptance, and failure modes. It writes no files.
- Before editing any skill file, use `to-spec` to write the spec — problem, solution, user stories, implementation decisions — in `_workspace/<task-name>/`.
- When the spec covers more than one reviewable chunk, use `to-issues` to cut it into ordered work units in the `task.md` Plan section.
- After a non-trivial skill change, review cycle, or debugging session is verified, use `compound-learning` to capture reusable learnings.

## Delegating To Subagents

Applies whenever work units are handed to subagents, in dependency order.

- Parallel subagents each get their own git worktree. Never two writers in one working tree.
- A worktree copies the repo, not the world — the same database, port, or external service still collides. Run those units in sequence.
- Two units can pass alone and break together with no file in common: one renames a symbol, the other calls the old name. Run the project's whole verification once on the merged tree.
- Do not merge the branches. Report them, and say the merged-tree verification still has to run.
- Copy the parent's Out of Scope into the subagent prompt verbatim; link everything else. A subagent already building the wrong thing does not follow a link.
- A subagent claiming success without the verification output has not finished. Re-dispatch it.
- Running every unit yourself in dependency order is a valid plan, not a failed delegation.

## Repository Notes

- Keep skill bodies concise. Put branch-specific detail in directly linked `references/` files.
- Keep examples, templates, scripts, and assets close to the skill that uses them.
- Prefer evidence from existing skill files, references, README entries, and `_workspace/` task notes over assumptions.
- For markdown-only changes, verify with structural inspection and targeted `rg` searches instead of inventing a test result.
- `examples/agents-md/` holds copy-paste `AGENTS.md` templates for downstream projects that install these skills; this file governs only work inside this repository.
