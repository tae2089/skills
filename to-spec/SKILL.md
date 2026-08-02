---
name: to-spec
description: Turn an agreed plan into a written spec — contract, acceptance criteria, and design — in local `_workspace/` files, Jira + Confluence, or GitHub Issues. Use before editing any code, test, config, doc, or infra file for a project-changing task; after `planning-grill` reaches a shared understanding; or when deciding where a contract or design doc should live. Hand off to `to-issues` to break the spec into work units.
---

# To Spec

Write the spec **before** any target file is edited. The contract and the design
exist first; the work units come later, from `to-issues`.

Each piece of state has exactly **one** canonical location. Never keep the same
content in two places — link instead.

## Step 1 — Resolve the backend

Resolve in this order, stopping at the first hit:

1. `_workspace/<task-name>/.tracker` exists → read it (one line: `local`, `jira`, or `github`).
2. `_workspace/.tracker` exists → read it.
3. The repo's `AGENTS.md` / `CLAUDE.md` declares a tracker → use it.
4. Ask the user once: local, jira, or github? Then write the answer to `_workspace/.tracker`.

The per-task file exists so one repo can hold a shared-backend task and a
throwaway local task at the same time. Write it only when this task differs from
the repo default.

Never infer the backend from the git remote — a GitHub remote does not mean the
team tracks work in GitHub Issues.

Choose `local` when no teammate will read this task's state. Choose `jira` or
`github` when someone other than you needs the contract or the design.

Root for `_workspace/`: the git repository the task belongs to; if there is no
single repository, the working directory. Keep `_workspace/` untracked via an
existing repo rule or a local Git exclude. Do not edit a tracked `.gitignore`
solely for agent state.

`to-issues` resolves the backend with the **same two-step order** and does not
ask again. Changing the order in one skill and not the other splits the backend
silently — the contract lands in one place and the work units in another.

Done when: the backend is known and cached in a `.tracker` file.

## Step 2 — Write the spec

Load exactly one:

- **local** → [references/local.md](references/local.md)
- **jira** → [references/jira.md](references/jira.md)
- **github** → [references/github.md](references/github.md)

Every backend stores the same five pieces:

| Piece | Content |
|---|---|
| Contract | Expected behavior, acceptance criteria. Max 5 bullets. |
| Non-Goals | What a reasonable reader would expect in scope but is not. Max 3 bullets. Omit when nothing plausible is out of scope. |
| Verification | The command that proves the whole task is done, and its expected result. One line. |
| Implementation | Approach, assumptions, affected modules, risks, edge cases, alternatives considered and dropped. Max 12 bullets. |
| Walkthrough | Append-only event log. **Always local**, never mirrored to Jira or GitHub. |

The contract says *what* and *when it is done*; the implementation notes say
*how* and *why*. Keep them apart — a contract that drifts into approach stops
being checkable.

Contract, Non-Goals, and Verification live together in one place: `task.md` on
`local`, the PRD ticket or `type:prd` issue elsewhere. That place is what a unit
links to, so it is the only spec a subagent is guaranteed to reach.

On `jira` and `github` the contract opens with one line naming the problem it
solves and for whom, because a teammate opens that ticket without this
conversation. `local` skips the line — nobody reads it cold.

**Always write the implementation notes.** There is no small-task exemption. Starting
work with no written approach is how the same decision gets made twice, in two
different ways, by two different people.

Check the notes against these four before handing off. Any one of them true means
the notes need more than a sentence:

- a public interface, schema, persistence, migration, external side-effect, security/auth, concurrency, or compatibility change
- no existing local pattern to copy
- competing design choices that had to be settled
- diagnosis or cross-module coordination

**Non-Goals stop drift.** Write a non-goal when the work sits next to something
an implementer would plausibly reach for: an adjacent module, a cleanup the
diff invites, a generalization the second caller would need. Do not list things
nobody would attempt — an empty-ish Non-Goals section reads as "nothing is out
of bounds", which is worse than no section.

    Non-Goals
    - `internal/worker`의 환경변수 호출부는 그대로 둔다.
    - 설정 핫 리로드는 안 한다. 반영하려면 재시작해야 한다.

An approach you considered and dropped is **not** a non-goal — it is an
implementation note. `--no-reload because inotify is unreliable on the CI mounts`
belongs next to the approach it lost to.

**Verification runs the whole project.** Not a subset — `go test ./...`, never
`go test ./internal/config/...`. In a repo with no test surface, the repo's own
full build or validate command. A work unit's `verify:` is always a part; this is
always the whole. That is why the two never say the same thing.

Walkthrough format, one line per event:

```
[time] decision|error|verification: one-line summary
```

Record only what the plan could not know in advance: failed verifications with
their cause, scope changes, and the final verification result. Decisions made
*before* work started belong in the implementation notes, not here — they came
out of `planning-grill` and already have a home.

Read only its tail (~20 lines) unless older context is needed.

Do not write the work breakdown here. The ordered plan is `to-issues`' job.

Done when: the contract, the verification command, and the implementation notes
exist in their canonical location, and no target file has been edited yet.

## Step 3 — Hand off

Report the backend and where the contract and the implementation notes landed — a
path, a ticket key, or an issue number. Then hand off to `to-issues` to break the
spec into work units.

Do not implement behavior whose contract is not written down.

## Cross-cutting rules

- **Write the prose in the user's language.** Contract, non-goals, implementation notes, and walkthrough lines are read by people. Commands, file paths, labels (`type:prd`), and status values (`Todo` / `Done`) stay verbatim — they are searchable strings, not prose.
- **Never copy content between locations.** Reference by path + section heading, or by ticket/issue link. Exception: output explicitly built to be pasted into a tool that cannot read files.
- **Link, don't duplicate.** When the contract lives in a ticket, the local file holds the ticket link and a one-line summary — not the ticket body.
- **The walkthrough never leaves the machine.** No backend mirrors it.
- Creating a Jira ticket, a Confluence page, or a GitHub issue is visible to the team. Say what you are about to create and get the user's confirmation before the first write to a shared backend.
