---
name: decompose-and-dispatch
description: Run the issues `to-issues` created by giving each one to a subagent, in dependency order. Use when the user asks for delegated, parallel, or multi-agent execution of an existing issue list. Skip when there is no issue list yet — run `to-issues` first — or when one agent doing the work in sequence is simpler.
---

# Decompose And Dispatch

The work is already cut into units. `to-issues` did that. This skill reads those
issues and gives each one to a subagent.

Do not re-decompose. If a unit turns out to be the wrong size, fix its issue
through `to-issues` and come back.

## Step 1 — Read the issues

Read `_workspace/.tracker` for the backend, then load the units:

- **local** — the `## Plan` section of `_workspace/<task-name>/task.md`
- **jira** — the PRD ticket's sub-tasks
- **github** — `gh issue list` filtered to the PRD's sub-issues

Each unit already carries its objective, scope, acceptance, verification command,
and dependencies. A unit missing any of those is not ready — send it back to
`to-issues`.

## Step 2 — Group by dependency

Units whose dependencies are all `Done` can start now. Everything else waits.

Among the ready units, decide which may run at the same time — see
[reference/parallelism.md](reference/parallelism.md). Two units that write the
same files never run together, whatever their dependency lines say.

## Step 3 — Dispatch

Delegate only when the runtime can spawn subagents **and** the user asked for
delegated, parallel, or multi-agent work. Otherwise run the units yourself, in
order — that is a normal outcome, not a fallback.

Each subagent prompt must be self-contained and carry exactly this:

- the issue reference — file path and unit number, ticket key, or issue number
- the objective, verbatim from the issue
- `allowed_scope`: the files it may write, and the instruction to touch nothing else
- the verification command and its expected result
- the report contract: what changed, the verification output, anything left undone

Do not paste the spec into the prompt. The issue links to its parent; the
subagent reads the parent if it needs the contract.

## Step 4 — Collect and report

A unit is `Done` only when its verification command ran and passed. A subagent
claiming success without that output has not finished — say so and re-dispatch.

Update each unit's status in its backend as results come in. Report at the end:
units done, units blocked and why, and what runs next.

End with one of:

- `READY_TO_EXECUTE` — every unit has a runner and a verification command.
- `PARTIAL` — some units ran; name the blocked ones and what unblocks them.
- `BLOCKED` — required context, permission, or runtime capability is missing and
  no safe fallback exists.
