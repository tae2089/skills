# Backend: github

GitHub Issues are canonical. The local file is a thin pointer.

| Piece | Location |
|---|---|
| Contract | Issue labeled `type:prd` |
| Non-Goals | Same issue, below the contract |
| Verification | Same issue, last section |
| Implementation | Issue labeled `type:design` — the remote stand-in for `implementation.md` |
| Plan | Native sub-issues of the PRD issue — created by `to-issues` |
| Walkthrough | `_workspace/<task-name>/walkthrough.md` — local, never uploaded |

Shape once `to-issues` has run:

```
[type:design] #10  approach, alternatives dropped, assumptions, risks
[type:prd]    #11  problem, contract, non-goals, verification — body links #10
              ├─ #12  increment 1   (native sub-issue)
              ├─ #13  increment 2
              └─ #14  increment 3
```

Sub-issues carry no label — the native parent/child link already expresses the
hierarchy. Labels mark only what the hierarchy cannot: design vs prd.

If the org has native **Issue Types** configured, use those instead of `type:*`
labels.

## Prerequisites

Use `gh` for all issue operations. Confirm the labels exist before first use:

```
gh label list --search type:
```

Create missing ones with `gh label create`.

## Order of creation

Creating issues is visible to the team. State what you are about to create and
get the user's confirmation before the first `gh issue create`.

1. **Design issue** — `gh issue create --label type:design`. Approach, alternatives considered and dropped, assumptions, affected modules, risks, edge cases. Max 12 bullets. Always created; there is no skip.
2. **PRD issue** — `gh issue create --label type:prd`, body in this order:

```markdown
설정을 바꿀 때마다 재배포해야 한다. 운영자가 파일 하나만 고치면 되게 만든다.  <!-- problem, one line -->

## Contract
- ...                                    <!-- max 5 bullets -->

## Non-Goals
- ...                                    <!-- max 3; drop the heading if empty -->

## Verification
`go test ./...` — all pass

Design: #10
```

The Verification command runs the whole project. Sub-issues carry their own
partial commands; this one is not a copy of any of them.

3. **Local `task.md`** — pointer only:

```markdown
# <task-name>

PRD: #11
Design: #10

## Plan
- (filled by to-issues)

## Result
- (filled at completion)
```

The problem line exists because a teammate opening the PRD cold gets the
contract but not the reason for it. One line is the whole budget — background
belongs in the design issue.

Non-Goals and Verification sit in the PRD, not the design issue, because
`to-issues` links every sub-issue to the PRD. A subagent following that link
reaches the bounds and the check; the design issue is one hop further.

Do not create `implementation.md` — the design issue replaces it.
Do not copy the issue body into `task.md`.

Sub-issues are not created here. Hand the PRD number to `to-issues`.

## Starting from an existing issue

Read the issue, start `task.md` with its number, then hand off to `to-issues`.
Do not restate the issue's contract locally.
