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
- When the skill change is fuzzy, high-impact, or lacks testable acceptance criteria, use `planning-grill` to sharpen scope, acceptance, and failure modes before decomposing it.
- For large cross-skill changes, use `decompose-and-dispatch` to split the work into bounded units. Use `execute-dispatch-unit` only for a clearly assigned unit with scope, dependencies, and verification.
- After a non-trivial skill change, review cycle, or debugging session is verified, use `compound-learning` to capture reusable learnings.

## Repository Notes

- Keep skill bodies concise. Put branch-specific detail in directly linked `references/` files.
- Keep examples, templates, scripts, and assets close to the skill that uses them.
- Prefer evidence from existing skill files, references, README entries, and `_workspace/` task notes over assumptions.
- For markdown-only changes, verify with structural inspection and targeted `rg` searches instead of inventing a test result.
- `examples/agents-md/` holds copy-paste `AGENTS.md` templates for downstream projects that install these skills; this file governs only work inside this repository.
