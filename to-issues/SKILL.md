---
name: to-issues
description: Break a written spec into ordered, reviewable work units and record them as issues — `task.md` Plan lines, Jira sub-tasks, or GitHub sub-issues. Use after `to-spec` has written the contract, when starting from an existing PRD ticket or issue, or when the user asks to split work into issues or tickets. Hand off to `decompose-and-dispatch` to run them.
---

# To Issues

Turn one spec into the ordered work units that implement it. Each unit becomes an
issue. `decompose-and-dispatch` gives each issue to a subagent.

The spec already exists — `to-spec` wrote it. Read it; do not restate it.

## Step 1 — Read the backend and the spec

Resolve the backend the same way `to-spec` did, stopping at the first hit:

1. `_workspace/<task-name>/.tracker` (one line: `local`, `jira`, or `github`).
2. `_workspace/.tracker`.

If neither exists, `to-spec` has not run — run that first instead of guessing a
backend. Do not invent a third resolution rule here; a different order from
`to-spec` puts the contract in one backend and the work units in another.

Then read the spec from that backend: the local `task.md` Contract plus
`implementation.md`, or the PRD ticket plus the Confluence design page, or the
`type:prd` issue plus the `type:design` issue.

Done when: the backend is known and the contract is in front of you.

## Step 2 — Cut the work into units

Size each unit as **one reviewable chunk** — roughly one pull request. Not one
per test; not one per file. Over-splitting floods the board and multiplies
handoff cost.

Each unit must state:

- **Objective** — the observable change, in one sentence.
- **Scope** — the files or modules it may touch, and what it must not touch.
- **Acceptance** — the condition that proves it is done: a behavior, a file's
  content, or a command's output.
- **Verification** — the exact command to run, and the expected result.
- **Depends on** — the units that must land first, by their issue reference.
  Empty for units that can start immediately.

A unit with no verification command is not ready. Go back to the spec and find
what would prove it.

Check every unit against the spec's Non-Goals before writing it. A unit that
implements a non-goal does not get created — the spec said no. If the work
genuinely turns out to be needed, that is a contract change: go back to
`to-spec`, do not quietly add the unit here.

Order the units so that dependencies come first. Say which ones can run at the
same time — `decompose-and-dispatch` uses that to decide what runs in parallel.

Done when: every unit has all five fields and the dependency order is explicit.

## Step 3 — Write the issues

Load exactly one:

- **local** → [references/local.md](references/local.md)
- **jira** → [references/jira.md](references/jira.md)
- **github** → [references/github.md](references/github.md)

Creating Jira sub-tasks or GitHub sub-issues is visible to the team and awkward
to undo. List what you are about to create — count, titles, parent — and get the
user's confirmation before the first write. The local backend needs no
confirmation.

Done when: every unit exists in the backend, in order, linked to its parent, and
the local `task.md` Plan lists them with `Todo` status.

## Step 4 — Hand off

Report the parent reference, the unit count, and which units have no dependencies
and can start now. To run them, hand the parent reference to
`decompose-and-dispatch` — that skill takes the target as an argument and knows
nothing about this one.

## Cross-cutting rules

- **Never copy the spec into a unit.** A unit links to the parent; the parent
  holds the contract. Repeat only what the unit's own scope needs.
- **Never put a secret value in an issue.**
- Re-running this skill on a spec that already has issues amends the existing
  ones. Do not create a second set.
- When execution shows a unit was cut wrong, fix that unit's issue and note the
  change in `walkthrough.md`. A contract that turns out wrong goes back to
  `to-spec`, not edited here.
