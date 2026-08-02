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

1. `_workspace/.tracker` exists → read it (one line: `local`, `jira`, or `github`).
2. The repo's `AGENTS.md` / `CLAUDE.md` declares a tracker → use it.
3. Ask the user once: local, jira, or github? Then write the answer to `_workspace/.tracker`.

Never infer the backend from the git remote — a GitHub remote does not mean the
team tracks work in GitHub Issues.

Choose `local` when no teammate will read this task's state. Choose `jira` or
`github` when someone other than you needs the contract or the design.

Root for `_workspace/`: the git repository the task belongs to; if there is no
single repository, the working directory. Keep `_workspace/` untracked via an
existing repo rule or a local Git exclude. Do not edit a tracked `.gitignore`
solely for agent state.

`to-issues` and `decompose-and-dispatch` read `_workspace/.tracker` and do not
resolve the backend again. This step is the only place that decides it.

Done when: the backend is known and cached in `_workspace/.tracker`.

## Step 2 — Pick the tier

**Fast tier** only when ALL hold:

- no public interface, schema, persistence, migration, external side-effect, security/auth, concurrency, or compatibility change
- one bounded implementation/test or validation increment
- an existing local pattern applies
- no competing design choices, diagnosis, or cross-module coordination needed

Otherwise — or when unsure — **Full tier**.

Escalate Fast → Full the moment diagnosis, a new design decision, scope
expansion, or another behavioral increment appears.

Fast tier skips the design artifact (`implementation.md` / seed page / seed
issue) in every backend.

Done when: the tier is stated and, for Fast tier, each of the four conditions is true.

## Step 3 — Write the spec

Load exactly one:

- **local** → [references/local.md](references/local.md)
- **jira** → [references/jira.md](references/jira.md)
- **github** → [references/github.md](references/github.md)

Every backend stores the same three pieces:

| Piece | Content |
|---|---|
| Contract | Expected behavior, acceptance criteria. Max 5 bullets. |
| Design | Approach, assumptions, affected modules, risks, edge cases. Max 12 bullets. Full tier only. |
| Journal | Append-only event log. **Always local**, never mirrored to Jira or GitHub. |

Journal format, one line per event — record only design decisions, failed
verifications with cause, scope changes, and final verification:

```
[time] decision|error|verification: one-line summary
```

Read only its tail (~20 lines) unless older context is needed.

Do not write the work breakdown here. The ordered plan is `to-issues`' job.

Done when: the contract and, on Full tier, the design exist in their canonical
location, and no target file has been edited yet.

## Step 4 — Hand off

Report the backend, the tier, and where the contract and design landed — a path,
a ticket key, or an issue number. Then hand off to `to-issues` to break the spec
into work units.

Do not implement behavior whose contract is not written down.

## Cross-cutting rules

- **Never copy content between locations.** Reference by path + section heading, or by ticket/issue link. Exception: output explicitly built to be pasted into a tool that cannot read files.
- **Link, don't duplicate.** When the contract lives in a ticket, the local file holds the ticket link and a one-line summary — not the ticket body.
- **Journal never leaves the machine.** No backend mirrors it.
- Creating a Jira ticket, a Confluence page, or a GitHub issue is visible to the team. Say what you are about to create and get the user's confirmation before the first write to a shared backend.
