---
name: to-spec
description: Turn an agreed plan into a written spec — problem, solution, user stories, and implementation decisions — in `_workspace/` files, published to a tracker when the project has one. Use before editing any code, test, config, doc, or infra file for a project-changing task; after `planning-grill` reaches a shared understanding; or when the user asks for a spec, PRD, or design doc. Hand off to `to-issues` to break the spec into work units.
---

# To Spec

Write the spec **before** any target file is edited. The spec exists first; the work
units come later, from `to-issues`.

Do not interview the user. Synthesize what the conversation already settled. If the
plan is still fuzzy, go back to `planning-grill`.

Adapted from Matt Pocock's `to-spec` skill in `mattpocock/skills`.

## Step 1 — Where it goes

Always `_workspace/<task-name>/`, kebab-case. Root: the git repository the task
belongs to, else the working directory. Keep it untracked through an existing repo
rule or a local Git exclude — do not edit a tracked `.gitignore` for agent state.

Publishing to a tracker is a step on top, not a different place. Publish when the
repo's `AGENTS.md` / `CLAUDE.md` names a tracker, or when the user asks. Never infer
one from the git remote. The local files are written either way, and `task.md` holds
the link — see [references/publishing.md](references/publishing.md).

Done when: `_workspace/<task-name>/` exists.

## Step 2 — Read the code, then agree on the seams

Explore the repo for the current state of the area you are touching, unless you
already have. Use the project's own vocabulary in the spec, and respect any ADRs
covering that area.

Then sketch the seams you will test the feature at. Prefer seams that already exist.
Use the highest seam you can. The fewer seams across the codebase the better — one
is ideal.

**Show the user the seams and check they match what they expect.** A seam chosen
wrong here makes every test below it test the wrong thing.

Done when: the user has seen the seams and agreed.

## Step 3 — Write the spec

Two files. Nothing is repeated between them — link instead.

| Section | File |
|---|---|
| Problem Statement, Solution, User Stories, Out of Scope, Verification | `task.md` |
| Implementation Decisions, Testing Decisions, Further Notes | `implementation.md` |

### `task.md`

```markdown
# <task-name>

## Problem Statement
지금 사용자가 겪는 문제. 사용자 관점으로.

## Solution
그 문제가 어떻게 없어지는가. 사용자 관점으로 — 만드는 방법이 아니라.

## User Stories
1. As a <actor>, I want <feature>, so that <benefit>
2. ...

## Out of Scope
- 범위 안이라고 오해할 만하지만 아닌 것

## Verification
- [ ] Todo — 고치기 전 US-1의 검사가 실패하는 것 확인 (출력 남길 것)
- [ ] Todo — 프로젝트 전체 명령과 기대 결과
- [ ] Todo — 실물을 손으로 한 번

## Plan
- (filled by to-issues)

## Result
- (filled at completion)
```

### User stories are the numbering everything downstream points at

Make the list long. It should cover every aspect of the feature, not the headline
cases. `to-issues` cites them as `US-1, US-3` and checks the numbering both ways, so
a behavior with no story is a behavior nobody builds.

### Verification says how you find out, in three fixed entries

1. **Fail first.** A test that never failed has not been shown to check anything.
   The code author usually writes the tests, so both can agree and both be wrong.
2. **The whole project** — `go test ./...`, never `go test ./internal/config/...`.
   No test surface: the repo's own full build or validate command. A work unit's
   `verify:` is a part; this is the whole, so the two never collide.
3. **The real artifact, once, by hand.** A suite that passes while the binary does
   not start is a suite testing itself.

Cite a story by number, never by restating it. Stories grow; this list stays at
three.

### `implementation.md`

**Implementation Decisions** — modules built or modified, the interfaces that
change, technical clarifications from the user, architectural decisions, schema
changes, API contracts, specific interactions.

No file paths and no code snippets — both go out of date faster than the prose
around them. Name modules and interfaces instead. One exception: a snippet from a
prototype that pins a decision more precisely than prose can — a state machine, a
reducer, a schema, a type shape. Keep the decision-rich part, not a working demo.

**Testing Decisions** — what makes a good test here (test external behavior, never
implementation details), which modules get tested, and prior art in the codebase for
that kind of test. `to-issues` builds each unit's verify command from the module
list, so name real ones.

**Further Notes** — anything else worth carrying forward.

### A bug fix has no from-scratch problem statement

The behavior exists and is wrong. Problem Statement is 재현 — the exact input that
triggers it — plus 현재 동작, quoted from real output. Solution is 기대 동작.
Verification entry 1 is that reproduction failing before the fix.

Do not write the work breakdown here — that is `to-issues`' job.

Done when: both files exist and no target file has been edited.

## Step 4 — Hand off

Report where the spec landed — a path, and a ticket or issue reference when it was
published. Then hand off to `to-issues`.

## Cross-cutting rules

- **Write the prose in the user's language.** The spec is read by people. Section headings, commands, file paths, labels (`type:prd`), and status values (`Todo` / `Done`) stay verbatim — they are searchable strings, not prose. The templates above are filled in Korean as an example; only their headings are fixed.
- **Never keep the same content in two places.** Reference it by path plus section heading, or by ticket link. When the spec is published, the local file holds the link and a one-line summary, not the body.
- Publishing is visible to the team and awkward to undo. Say what you are about to create and get the user's confirmation before the first write.
