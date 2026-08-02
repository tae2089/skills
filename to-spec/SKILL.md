---
name: to-spec
description: Turn an agreed plan into a written spec — contract, acceptance criteria, and design — in local `_workspace/` files or GitHub Issues. Use before editing any code, test, config, doc, or infra file for a project-changing task; after `planning-grill` reaches a shared understanding; or when deciding where a contract or design doc should live. Hand off to `to-issues` to break the spec into work units.
---

# To Spec

Write the spec **before** any target file is edited. The contract and the design
exist first; the work units come later, from `to-issues`.

Each piece of state has exactly **one** canonical location. Never keep the same
content in two places — link instead.

## Step 1 — Resolve the backend

First hit wins: `_workspace/<task-name>/.tracker`, then `_workspace/.tracker`, then
a tracker declared in the repo's `AGENTS.md` / `CLAUDE.md`. One line: `local` or
`github`. Write the per-task file only when this task differs from the repo
default.

None of those exist? Ask the user once — `local` when no teammate will read this
task's state, `github` when someone else needs the contract — and write the answer
to `_workspace/.tracker`. Never infer it from the git remote. `to-issues` reads the
same files and never asks again.

Any other tracker — Jira, Linear, Notion — is `local` plus a push, not a backend.
See `references/local.md`.

Root for `_workspace/`: the git repository the task belongs to, else the working
directory. Keep it untracked via an existing repo rule or a local Git exclude — do
not edit a tracked `.gitignore` for agent state.

Done when: the backend is known and cached in a `.tracker` file.

## Step 2 — Write the spec

Load exactly one. It holds the template and where each piece goes:

- **local** → [references/local.md](references/local.md)
- **github** → [references/github.md](references/github.md)

Every backend stores the same six pieces:

| Piece | Content | Cap |
|---|---|---|
| Contract | Expected behavior and acceptance criteria. Every bullet names a **trigger** and an **observable result**. | 5 bullets |
| Non-Goals | What a reasonable reader would expect in scope but is not. | 3 bullets |
| Test Cases | Real input → real expected output, numbered `TC-1`, `TC-2`, … | none |
| Verification | The commands that check those cases. | 3 entries |
| Implementation | Approach, assumptions, affected modules, risks, edge cases, alternatives dropped and why. | 12 bullets |
| Walkthrough | Append-only event log, one line per event: `[time] decision\|error\|verification: one-line summary`. **Always local**, never mirrored to a shared backend. | — |

Contract, Non-Goals, Test Cases, and Verification live in one place — a work unit
links there, so it is the only spec a subagent is guaranteed to reach.

### Never invent a value the user has not given

Write the gap in place instead:

    - 설정 파일 경로는 [NEEDS CLARIFICATION: 고정 경로인가, --config 플래그인가?]

A guess becomes the contract, and nobody downstream can tell it from a decision.
Markers are greppable. One or two unknowns — ask now and fill them in. More than
that, the plan was never settled: go back to `planning-grill`.

### A contract bullet with no trigger is not testable

Not "config parsing should be robust" — "잘못된 YAML을 만나면 문제된 키를 담은
타입 에러를 반환하고 exit 1". With no observable result, only the author can check
it.

### Non-Goals name what someone would plausibly reach for

An adjacent module, a cleanup the diff invites, a generalization the second caller
would need. Do not list what nobody would attempt — a thin section reads as
"nothing is out of bounds". An approach you considered and dropped is an
implementation note, not a non-goal.

### A test case has real values in it, or it is not one

The contract states a rule; a case states one instance of it, in values you could
type. A "case" that restates a contract bullet in words is not one — delete it.

**No cap on the count.** A task cut into nine work units needs at least nine cases
— `to-issues` flags a unit covering none as work nobody asked for. Two filters keep
the list from becoming the test file in prose:

- Keep only the cases where getting it wrong changes what gets built.
- Two cases the same code path satisfies are one case. `port: "eighty"` and
  `port: "abc"` hit the same branch — keep the value most likely to break. The rest
  belong in the test file, which should loop over all of them.

### Verification says how you find out; test cases say what must be true

So it lists runners, never cases. Three entries, whatever the case count:

1. **Fail first.** A test that never failed has not been shown to check anything.
   The code author usually writes the tests, so both can agree and both be wrong.
2. **The whole project** — `go test ./...`, never `go test ./internal/config/...`.
   No test surface: the repo's own full build or validate command. A work unit's
   `verify:` is a part; this is the whole, so the two never collide.
3. **The real artifact, once, by hand.** A suite that passes while the binary does
   not start is a suite testing itself.

Cite a case by number, never by value — `TC-1`, not `exit 1, stderr에 server.port`.
Copied values go stale on one side. Cases grow; this list stays at three.

### Implementation notes are always written, whatever the task size

No file paths and no code snippets — both go out of date faster than the prose
around them. Name modules and interfaces instead.

### A bug fix has no from-scratch contract

The behavior exists and is wrong. Replace the contract with 재현 (the exact input
that triggers it), 현재 동작 (what happens now, quoted from real output), and
기대 동작 (what should happen instead). TC-1 is the reproduction; verification
entry 1 is that test failing before the fix.

### The walkthrough records only what the plan could not know

Failed verifications with their cause, scope changes, and the final verification
result. Decisions made before work started belong in the implementation notes.
Read only the tail (~20 lines).

Do not write the work breakdown here — that is `to-issues`' job.

Done when: the contract, the numbered test cases, the verification list, and the
implementation notes exist in their canonical location, and no target file has been
edited yet.

## Step 3 — Hand off

Report the backend, where the contract and the implementation notes landed (a path,
a ticket key, or an issue number), and every `[NEEDS CLARIFICATION: ...]` still in
the spec — those are the questions `planning-grill` did not settle. Then hand off to
`to-issues`.

Do not implement behavior whose contract is not written down.

## Cross-cutting rules

- **Write the prose in the user's language.** Contract, non-goals, implementation notes, and walkthrough lines are read by people. Commands, file paths, labels (`type:prd`), and status values (`Todo` / `Done`) stay verbatim — they are searchable strings, not prose.
- **Never copy content between locations.** Reference by path + section heading, or by ticket/issue link. Exception: output explicitly built to be pasted into a tool that cannot read files.
- **Link, don't duplicate.** When the contract lives in a ticket, the local file holds the ticket link and a one-line summary — not the ticket body.
- **The walkthrough never leaves the machine.** No backend mirrors it.
- Creating a GitHub issue, or pushing to any team tracker, is visible to the team. Say what you are about to create and get the user's confirmation before the first write.
