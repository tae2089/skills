# Backend: jira

Jira and Confluence are canonical. The local file is a thin pointer.

| Piece | Location |
|---|---|
| Contract | Jira PRD ticket (description + acceptance criteria) |
| Non-Goals | Same ticket, below the contract |
| Verification | Same ticket, last section |
| Implementation | Confluence design page — the remote stand-in for `implementation.md` |
| Plan | Jira sub-tasks of the PRD ticket — created by `to-issues` |
| Walkthrough | `_workspace/<task-name>/walkthrough.md` — local, never uploaded |

## Prerequisites

The Atlassian MCP server must be authenticated. If only `authenticate` tools are
exposed, stop and ask the user to authenticate before creating anything.

The project key and Confluence space come from the repo's `AGENTS.md`. If absent,
ask once and record them there.

## Order of creation

Creating a ticket or a Confluence page is visible to the team. State what you are
about to create and get the user's confirmation before the first write.

1. **Confluence design page** — background, problem, approach, alternatives considered and dropped, assumptions, affected modules, risks, edge cases. Max 12 bullets. Always created; there is no skip.
2. **Jira PRD ticket** — description in this order:

```markdown
설정을 바꿀 때마다 재배포해야 한다. 운영자가 파일 하나만 고치면 되게 만든다.  <!-- problem, one line -->

## Contract
- ...                                    <!-- max 5 bullets -->

## Non-Goals
- ...                                    <!-- max 3; drop the heading if empty -->

## Verification
`go test ./...` — all pass

Design: <Confluence page URL>
```

The Verification command runs the whole project. Sub-tasks carry their own
partial commands; this one is not a copy of any of them.

3. **Local `task.md`** — pointer only:

```markdown
# <task-name>

Ticket: <PRD ticket URL>
Design: <Confluence page URL>

## Plan
- (filled by to-issues)

## Result
- (filled at completion)
```

The problem line exists because a teammate opening the ticket cold gets the
contract but not the reason for it. One line is the whole budget — background
belongs on the design page.

Non-Goals and Verification sit in the ticket, not on the design page, because
`to-issues` links every sub-task to the ticket. A subagent following that link
reaches the bounds and the check; the design page is one hop further.

Do not create `implementation.md` — the design page replaces it.
Do not copy the ticket body into `task.md`.

Sub-tasks are not created here. Hand the PRD ticket key to `to-issues`.

## Starting from an existing ticket

Read the ticket, start `task.md` with its link, then hand off to `to-issues`. Do
not restate the ticket's contract locally.
