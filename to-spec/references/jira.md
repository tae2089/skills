# Backend: jira

Jira and Confluence are canonical. The local file is a thin pointer.

| Piece | Location |
|---|---|
| Contract | Jira PRD ticket (description + acceptance criteria) |
| Design | Confluence design page — the remote stand-in for `implementation.md` |
| Plan | Jira sub-tasks of the PRD ticket — created by `to-issues` |
| Journal | `_workspace/<task-name>/walkthrough.md` — local, never uploaded |

## Prerequisites

The Atlassian MCP server must be authenticated. If only `authenticate` tools are
exposed, stop and ask the user to authenticate before creating anything.

The project key and Confluence space come from the repo's `AGENTS.md`. If absent,
ask once and record them there.

## Order of creation

Creating a ticket or a Confluence page is visible to the team. State what you are
about to create and get the user's confirmation before the first write.

1. **Confluence design page** (Full tier only) — background, problem, approach, assumptions, affected modules, risks, edge cases. Max 12 bullets.
2. **Jira PRD ticket** — description opens with one line saying what problem this solves and for whom, then the contract and acceptance criteria, max 5 bullets, then a link to the design page. Fast tier skips step 1 and the link, but keeps the problem line.
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

Do not create `implementation.md` — the design page replaces it.
Do not copy the ticket body into `task.md`.

Sub-tasks are not created here. Hand the PRD ticket key to `to-issues`.

## Starting from an existing ticket

Read the ticket, start `task.md` with its link, then hand off to `to-issues`. Do
not restate the ticket's contract locally.
