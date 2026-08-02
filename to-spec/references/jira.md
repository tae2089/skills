# Backend: jira

Jira and Confluence are canonical. The local file is a thin pointer.

| Piece | Location |
|---|---|
| Contract | Jira PRD ticket (description + acceptance criteria) |
| Design | Confluence seed page |
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

1. **Confluence seed page** (Full tier only) — background, problem, design approach, assumptions, affected modules, risks, edge cases. Max 12 bullets.
2. **Jira PRD ticket** — contract and acceptance criteria, max 5 bullets, plus a link to the seed page. Skip step 1 on Fast tier and the ticket carries no seed link.
3. **Local `task.md`** — pointer only:

```markdown
# <task-name>

Ticket: <PRD ticket URL>
Seed: <Confluence page URL>

## Plan
- (filled by to-issues)

## Result
- (filled at completion)
```

Do not create `implementation.md` — the seed page replaces it.
Do not copy the ticket body into `task.md`.

Sub-tasks are not created here. Hand the PRD ticket key to `to-issues`.

## Starting from an existing ticket

Read the ticket, seed `task.md` with its link, then hand off to `to-issues`. Do
not restate the ticket's contract locally.
