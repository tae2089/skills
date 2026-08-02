---
name: to-issues
description: Break a written spec into ordered, reviewable work units and record them as issues — `task.md` Plan lines or GitHub sub-issues. Use after `to-spec` has written the contract, when starting from an existing PRD issue, or when the user asks to split work into issues or tickets. Hand off to `decompose-and-dispatch` to run them.
---

# To Issues

Turn one spec into the ordered work units that implement it. Each unit becomes an
issue. `decompose-and-dispatch` gives each issue to a subagent.

The spec already exists — `to-spec` wrote it. Read it; do not restate it.

## Step 1 — Read the backend and the spec

Read `_workspace/<task-name>/.tracker`, else `_workspace/.tracker`. Neither exists
means `to-spec` has not run — run it first rather than guessing a backend or adding
a resolution rule of your own.

Then read the spec from that backend: the local `task.md` Contract plus
`implementation.md`, or the `type:prd` issue plus the `type:design` issue. A
`local` task whose contract was pushed to some other tracker holds the link in
`task.md` — follow it.

Done when: the backend is known and the contract is in front of you.

## Step 2 — Cut the work into units

Size each unit as **one reviewable chunk** — roughly one pull request. Not one
per test; not one per file. Over-splitting floods the board and multiplies
handoff cost.

Bound a unit by behavior, never by a file list. Which files an implementation
touches is not known until it is written, and a list guessed now either blocks the
subagent or gets ignored. The objective and the spec's Non-Goals are the bounds.

Each unit must state:

- **Objective** — the observable change, in one sentence.
- **Covers** — the spec's test cases this unit satisfies, by number: `TC-1, TC-3`.
- **Verification** — the exact command to run, and the expected result.
- **Depends on** — the units that must land first, by their issue reference.
  Empty for units that can start immediately.

A unit with no verification command is not ready. Go back to the spec and find
what would prove it — nobody watches a subagent work, so the command is the only
thing that can say "done".

**Take the check from the test cases; do not invent one.** The spec's
`## Test Cases` are values the user agreed to. A unit's verification command
exercises one or more of them, and `covers:` says which. A condition invented
here is a contract nobody approved.

When every unit is written, check the numbering both ways:

- a test case no unit covers → work you forgot to cut
- a unit covering no test case → work nobody asked for

Report both before creating anything. A test case with no unit is the more
dangerous one: everything passes and the feature is incomplete.

If the spec still holds a `[NEEDS CLARIFICATION: ...]` marker, do not write a
unit that depends on the missing answer. Say which marker blocks which unit and
send it back to `to-spec`.

Check every unit against the spec's Non-Goals before writing it. A unit that
implements a non-goal does not get created — the spec said no. If the work
genuinely turns out to be needed, that is a contract change: go back to
`to-spec`, do not quietly add the unit here.

Order the units so that dependencies come first. Say which ones can run at the
same time — `decompose-and-dispatch` uses that to decide what runs in parallel.

Done when: every unit has all four fields, every test case is covered by at least
one unit, and the dependency order is explicit.

## Step 3 — Write the issues

Load exactly one:

- **local** → [references/local.md](references/local.md)
- **github** → [references/github.md](references/github.md)

Creating GitHub sub-issues, or pushing units to any team tracker, is visible to
the team and awkward to undo. List what you are about to create — count, titles,
parent — and get the user's confirmation before the first write. The local backend
needs no confirmation.

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
