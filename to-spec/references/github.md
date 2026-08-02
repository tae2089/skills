# Backend: github

GitHub Issues are canonical. The local file is a thin pointer.

| Piece | Location |
|---|---|
| Contract | Issue labeled `type:prd` |
| Design | Issue labeled `type:seed` |
| Plan | Native sub-issues of the PRD issue — created by `to-issues` |
| Journal | `_workspace/<task-name>/walkthrough.md` — local, never uploaded |

Shape once `to-issues` has run:

```
[type:seed]  #10  design, assumptions, risks
[type:prd]   #11  contract, acceptance criteria — body links #10
             ├─ #12  increment 1   (native sub-issue)
             ├─ #13  increment 2
             └─ #14  increment 3
```

Sub-issues carry no label — the native parent/child link already expresses the
hierarchy. Labels mark only what the hierarchy cannot: seed vs prd.

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

1. **Seed issue** (Full tier only) — `gh issue create --label type:seed`. Background, design approach, assumptions, affected modules, risks. Max 12 bullets.
2. **PRD issue** — `gh issue create --label type:prd`. Contract and acceptance criteria, max 5 bullets, body links the seed issue. Fast tier skips step 1 and the link.
3. **Local `task.md`** — pointer only:

```markdown
# <task-name>

PRD: #11
Seed: #10

## Plan
- (filled by to-issues)

## Result
- (filled at completion)
```

Do not create `implementation.md` — the seed issue replaces it.
Do not copy the issue body into `task.md`.

Sub-issues are not created here. Hand the PRD number to `to-issues`.

## Starting from an existing issue

Read the issue, seed `task.md` with its number, then hand off to `to-issues`. Do
not restate the issue's contract locally.
