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
- **GitHub** — `gh issue list` filtered to the parent's sub-issues, or the listed numbers
- **any other tracker** — the parent's children, through whatever MCP server is connected

If no target was given, ask for one. Do not go looking for a plan to run —
guessing wrong means subagents write files for work nobody asked for.

Each unit must carry these two:

| Field | What it is |
|---|---|
| objective | the observable change, one sentence |
| depends on | the units that must land first, or none |

A unit missing either is not ready. Say which unit and which field, and stop. Do
not fill the gap by guessing.

**verification** — the exact command and its expected result — gets used when the
unit has it. Passed down, and the output is required back. Never invent one. A unit
with none still runs and goes in the report as `unverified`.

A unit does not carry a file list, and this skill does not ask for one. Nobody
knows which files an implementation touches until it is written. The objective and
the parent's non-goals are the bounds; the subagent reports the files afterwards.

Tickets from any producer run here, not only the ones `to-issues` wrote.

## Step 2 — Group by dependency

Units whose dependencies are all done can start now. Everything else waits.

Among the ready units, decide which may run at the same time — see
[reference/parallelism.md](reference/parallelism.md).

## Step 3 — Dispatch

Delegate only when the runtime can spawn subagents **and** the user asked for
delegated, parallel, or multi-agent work. Otherwise run the units yourself, in
order — that is a normal outcome, not a fallback.

Parallel subagents each get their own git worktree — never two writers in one
working tree.

Each subagent prompt must be self-contained and carry exactly this:

- the unit reference — file path and unit number, ticket key, or issue number
- the objective, verbatim from the unit
- the parent's non-goals, verbatim, if the parent states any
- the verification command and its expected result, when the unit has one
- the report contract: **every file it changed**, the verification output, anything
  left undone

Non-goals are the one thing that gets copied rather than linked. A subagent that
has already started building the wrong thing does not stop to follow a link.

Everything else stays out of the prompt. The unit references its parent; the
subagent reads the parent if it needs the contract.

## Step 4 — Collect and report

A unit that has a verification command is done only when that command ran and
passed. A subagent claiming success without the output has not finished — say so
and re-dispatch. A unit with no command is done when the subagent says so, and
stays `unverified` in the report.

Update each unit's status where it lives as results come in.

Parallel work leaves one branch per worktree. **This skill does not merge them.**
Report the branches, and say the project's whole verification command has to run
once after the merge — [reference/parallelism.md](reference/parallelism.md) says
why every unit passing alone is not enough.

Report at the end: units done, units unverified, units blocked and why, branches
left to merge, and what runs next.

End with one of:

- `READY_TO_EXECUTE` — every unit has a runner.
- `PARTIAL` — some units ran; name the blocked ones and what unblocks them.
- `BLOCKED` — required context, permission, or runtime capability is missing and
  no safe fallback exists.
