---
name: to-issues
description: Break a written spec into ordered, reviewable work units and record them as issues — `task.md` Plan lines, plus tracker issues when the spec was published. Use after `to-spec` has written the spec, or when the user asks to split work into issues or tickets. Stops at the written units; running them is a separate ask.
---

# To Issues

Turn one spec into the ordered work units that implement it. Each unit becomes an
issue, sized so one agent can take it start to finish.

The spec already exists — `to-spec` wrote it. Read it; do not restate it.

Adapted from Matt Pocock's `to-tickets` skill in `mattpocock/skills`.

## Step 1 — Read the spec

`_workspace/<task-name>/task.md` plus `implementation.md`. No `task.md` means
`to-spec` has not run — run it first.

A published spec leaves `task.md` holding a link instead of the sections. Follow it
and read the ticket.

Done when: the user stories and the implementation decisions are in front of you.

## Step 2 — Cut the work into units

Each unit is a **vertical slice**: a narrow but complete path through every layer it
touches — schema, API, UI, tests. Not a horizontal slice of one layer.

- A finished slice can be demoed or verified on its own.
- A slice fits in one fresh context window.
- Any prefactoring — "make the change easy, then make the easy change" — is its own
  unit, and it comes first.

Size each unit as one reviewable chunk, roughly one pull request. Not one per user
story; not one per file. Over-splitting floods the board and multiplies handoff cost.

Bound a unit by behavior, never by a file list. Which files an implementation
touches is not known until it is written, and a list guessed now either blocks the
subagent or gets ignored. The objective and the spec's Out of Scope are the bounds.

Each unit must state:

- **Objective** — the end-to-end behavior this unit makes work, in one sentence,
  from the user's side. Not a layer-by-layer list. It becomes the unit's title line
  in the Plan, so keep it short enough to read as one.
- **Covers** — the user stories this unit satisfies, by number: `US-1, US-3`.
- **Verification** — the exact command to run, and the expected result. Build it
  from the spec's Testing Decisions, which name the modules that get tested.
- **Depends on** — the units that must land first, by their issue reference. Empty
  for units that can start immediately.

A unit with no verification command is not ready. Nobody watches a subagent work, so
the command is the only thing that can say "done".

### Wide refactors are the exception to vertical slicing

A wide refactor is one mechanical change — rename a column, retype a shared symbol —
that breaks thousands of call sites at once. No vertical slice can land green, so do
not force one. Sequence it **expand–contract** instead:

1. **Expand** — add the new form beside the old. Nothing breaks. One unit.
2. **Migrate** — move call sites over in batches, sized by how far the change
   reaches: per package, per directory. Each batch is its own unit, and each depends
   on the expand. The old form still exists, so each batch stays green.
3. **Contract** — delete the old form once no caller remains. Depends on every
   migrate batch.

When even the batches cannot stay green alone, keep the sequence but give them one
shared integration branch, and add a final integrate-and-verify unit that depends on
all of them. Green is promised only there.

### Check the numbering both ways

- a user story no unit covers → work you forgot to cut
- a unit covering no user story → work nobody asked for

A story with no unit is the more dangerous one: everything passes and the feature is
incomplete. Report both.

Check every unit against the spec's Out of Scope before writing it. A unit that
implements one does not get created — the spec said no. If it genuinely turns out to
be needed, that is a spec change: go back to `to-spec`.

Done when: every unit has all four fields, every user story is covered, and the
dependency order is explicit.

## Step 3 — Quiz the user

Present the breakdown as a numbered list before creating anything. Per unit: title,
what it delivers, and what blocks it.

Then the numbering check from Step 2 — which stories no unit covers, which units
cover no story. Empty on both sides is a result: say so, so the user can tell a clean
check from a skipped one.

Ask:

- Does the granularity feel right — too coarse, too fine?
- Are the blocking edges right? Does each unit depend only on units that genuinely
  gate it?
- Should any units be merged or split further?

Iterate until the user approves. This is the gate — nothing downstream checks the
breakdown again.

Done when: the user has approved the list.

## Step 4 — Write the issues

Fill the Plan section of `task.md`, always:

```markdown
## Plan
- [ ] Todo — 01 설정 파일 파싱
      covers: US-1, US-3
      verify: `go test ./internal/config/...` — 전부 통과
      needs: —
- [ ] Todo — 02 시작 시점에 파서 연결
      covers: US-4
      verify: `go test ./cmd/server/...` — 전부 통과
      needs: 01
```

Number units `01`, `02`, … in dependency order, blockers first, so a subagent can be
pointed at one by number. `needs: —` means it can start now.

Headings and field names are fixed; the text in them goes in the user's language.

A Plan line **is** the issue when the spec was never published. Do not create a file
per unit — a subagent reads `task.md` and its own line. Never copy the spec into a
unit — the unit points at the parent, and the parent holds the stories.

When the spec was published, also create one issue per unit on that tracker — see
[references/publishing.md](references/publishing.md). Re-running this skill on a
spec that already has units amends them; never create a second set.

Statuses are `Todo` → `In Progress` → `Done`. Whoever runs the units moves them —
when they are dispatched, the agent holding the verification output does it. `Done`
only after that unit's `verify` command passed.

Done when: every unit is in the Plan in dependency order with `Todo` status, and
mirrored to the tracker if the spec was published.

## Step 5 — Hand off

Report the unit count and which units have no dependencies and can start now. Stop
there. Running the units is a separate ask, and the project's own rules say how to
delegate them.
