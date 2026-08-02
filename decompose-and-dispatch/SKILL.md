---
name: decompose-and-dispatch
description: Run an existing list of work tickets by giving each one to a subagent, in dependency order. Use when the user asks for delegated, parallel, or multi-agent execution of issues, tickets, or a plan that is already broken into units. Skip when the work is not broken down yet, or when one agent doing it in sequence is simpler.
---

# Decompose And Dispatch

The work is already cut into units. This skill reads those units and gives each
one to a subagent.

Do not re-decompose. If a unit is the wrong size, fix it where it lives and come
back.

## Step 1 — Read the units

The user says what to run: a parent reference, a list of references, or a file
path. If they gave a parent, read its children.

- **a file** — the `## Plan` section of the file (each line is one unit)
- **Jira** — the parent ticket's sub-tasks, or the listed keys
- **GitHub** — `gh issue list` filtered to the parent's sub-issues, or the listed numbers

If no target was given, ask for one. Do not go looking for a plan to run —
guessing wrong means subagents write files for work nobody asked for.

Each unit must carry all five of these:

| Field | What it is |
|---|---|
| objective | the observable change, one sentence |
| scope | the files it may write |
| acceptance | the condition that proves it is done |
| verification | the exact command and its expected result |
| depends on | the units that must land first, or none |

A unit missing any of them is not ready. Say which unit and which field, and
stop. Do not fill the gap by guessing.

## Step 2 — Group by dependency

Units whose dependencies are all done can start now. Everything else waits.

Among the ready units, decide which may run at the same time — see
[reference/parallelism.md](reference/parallelism.md). Two units that write the
same files never run together, whatever their dependency lines say.

## Step 3 — Dispatch

Delegate only when the runtime can spawn subagents **and** the user asked for
delegated, parallel, or multi-agent work. Otherwise run the units yourself, in
order — that is a normal outcome, not a fallback.

Each subagent prompt must be self-contained and carry exactly this:

- the unit reference — file path and unit number, ticket key, or issue number
- the objective, verbatim from the unit
- `allowed_scope`: the files it may write, and the instruction to touch nothing else
- the parent's non-goals, verbatim, if the parent states any
- the verification command and its expected result
- the report contract: what changed, the verification output, anything left undone

Non-goals are the one thing that gets copied rather than linked. A subagent that
has already started building the wrong thing does not stop to follow a link.

Everything else stays out of the prompt. The unit references its parent; the
subagent reads the parent if it needs the contract.

## Step 4 — Collect and report

A unit is done only when its verification command ran and passed. A subagent
claiming success without that output has not finished — say so and re-dispatch.

Update each unit's status where it lives as results come in. Report at the end:
units done, units blocked and why, and what runs next.

End with one of:

- `READY_TO_EXECUTE` — every unit has a runner and a verification command.
- `PARTIAL` — some units ran; name the blocked ones and what unblocks them.
- `BLOCKED` — required context, permission, or runtime capability is missing and
  no safe fallback exists.
