# Backend: github

GitHub Issues are canonical. The local file is a thin pointer.

| Piece | Location |
|---|---|
| Contract | Issue labeled `type:prd` |
| Design | Issue labeled `type:design` — the remote stand-in for `implementation.md` |
| Plan | Native sub-issues of the PRD issue — created by `to-issues` |
| Journal | `_workspace/<task-name>/walkthrough.md` — local, never uploaded |

Shape once `to-issues` has run:

```
[type:design] #10  approach, assumptions, risks
[type:prd]    #11  problem, contract, acceptance criteria — body links #10
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

1. **Design issue** (Full tier only) — `gh issue create --label type:design`. Approach, assumptions, affected modules, risks, edge cases. Max 12 bullets.
2. **PRD issue** — `gh issue create --label type:prd`. Body opens with one line saying what problem this solves and for whom, then the contract and acceptance criteria, max 5 bullets, then a link to the design issue. Fast tier skips step 1 and the link, but keeps the problem line.
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

Do not create `implementation.md` — the design issue replaces it.
Do not copy the issue body into `task.md`.

Sub-issues are not created here. Hand the PRD number to `to-issues`.

## Starting from an existing issue

Read the issue, start `task.md` with its number, then hand off to `to-issues`.
Do not restate the issue's contract locally.
