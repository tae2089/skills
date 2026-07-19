---
name: compound-learning
description: Capture reusable learnings from completed and verified work — tasks, reviews, bug fixes, architecture decisions, debugging sessions — into task-scoped notes and durable solution docs so future agents skip re-discovery. Use for "compound learning", "document what worked", "capture a reusable pattern", "summarize lessons", "update solution docs", "close the loop". Do not use for in-progress work, uncertain outcomes, trivial fixes, performing code review itself, or replaying a session as an executable recipe (that is `session-recipe`).
---

# Compound Learning

Capture reusable learning after evidence exists. The goal is not archiving; it is making the next similar task easier.

## Outputs

- Task-scoped capture: `_workspace/<task-name>/compound-learning.md`, next to the task's state files.
- Durable knowledge: `docs/solutions/<category>/<slug>.md`, only when the guidance is verified and reusable beyond the current task.
- No task workspace: present the capture in the final response; the only file written is a solution doc, and only when the learning qualifies as durable.

## Workflow

1. Gather evidence: the task's state files (`task.md` and, when present, `implementation.md` and `walkthrough.md`), test or validation output, review artifacts, changed files, and the current conversation. Reference sources by path; do not copy long excerpts.
2. Apply the Capture Decision. If skip, state the reason in one sentence and stop.
3. Classify the learning as bug track or knowledge track.
4. If `docs/solutions/` exists, search it for overlap; prefer updating a close match over creating a near-duplicate.
5. When a task workspace exists, write `_workspace/<task-name>/compound-learning.md` using the structure in `references/capture-format.md`; otherwise present the same sections in the final response.
6. Record a solution doc decision — `promote`, `update_existing`, or `skip` — with a one-sentence reason, and apply it using `references/solution-doc-format.md`. Promote only guidance that evidence shows worked.
7. List narrow follow-ups or refresh recommendations, or state that there are none.

## Capture Decision

Capture when at least one holds:

- the issue took meaningful investigation
- the root cause was non-obvious
- a reusable workflow, convention, or architectural pattern emerged
- a previous assumption was corrected
- future agents are likely to make the same mistake
- review found a pattern broader than a single line
- the work changed how future planning, design, coding, or review should proceed

Skip when the work is too local to reuse or the outcome is still uncertain. Never present a solution as verified without evidence that it worked.

Track classification:

- **Bug track**: failures, regressions, broken tests, runtime, integration, data, security, or performance issues, and debugging workflows.
- **Knowledge track**: architecture patterns, design decisions, conventions, workflow practices, tool behavior, testing strategy, and coordination lessons.

## Hand Off

When the learning demands follow-up work, hand off instead of expanding scope. Phrase hand-offs as "use the `<skill>` skill if available".

| Learning changes | Hand off to |
| --- | --- |
| Vocabulary, terminology, aliases | `domain-modeling` |
| Plan, scope, or acceptance criteria | `planning-grill` |
| Module shape or interface contract | `codebase-design` |
| Control flow, ordering, or side effects | `flow-design` |
| Review severity policy or false-positive suppressions | `ready-code-review` |
| Needs re-diagnosis on existing code | `diagnosing-bugs` |

## Completion

Compound learning is complete when the capture was skipped with a one-sentence reason, or when all of the following hold:

- the learning is classified as bug track or knowledge track
- every claim is backed by listed evidence (a state file, test output, review artifact, or diff path, or a specific conversation reference)
- reusable guidance is explicit enough to act on without re-reading the original task
- overlap with existing `docs/solutions/` has been checked when the store exists
- `_workspace/<task-name>/compound-learning.md` is written when a task workspace exists
- the solution doc decision (`promote` / `update_existing` / `skip`) is recorded with a one-sentence reason
- follow-ups are listed, or their absence is stated
