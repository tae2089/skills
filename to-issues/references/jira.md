# Backend: jira

One Jira sub-task per work unit, under the PRD ticket `to-spec` created.

## Prerequisites

The Atlassian MCP server must be authenticated. You need the PRD ticket key from
`to-spec`.

## Creating

List the summaries and the parent key, and get the user's confirmation before the
first write. Creating sub-tasks shows up on the team's board immediately.

For each unit, in dependency order, create a sub-task of the PRD ticket with:

- **Summary** — `01 parse the config file`
- **Description** — scope, acceptance, verification command, and `Depends on`
  with the sub-task keys that must land first

Do not copy the PRD's contract into the sub-task. The parent link is the
reference.

Over-splitting floods the board. One sub-task is one reviewable chunk, not one
test.

## Local pointer

Fill the Plan section in `task.md` with keys only:

```markdown
## Plan
- [ ] Todo — 01 parse the config file (PROJ-124)
- [ ] Todo — 02 wire the parser into startup (PROJ-125) — needs PROJ-124
```

Do not copy sub-task descriptions into `task.md`.

## Updating

- Unit finished → transition its sub-task, update the `task.md` line to `Done`.
  No comment per sub-task.
- Scope change on a unit → edit that sub-task and append one line to
  `walkthrough.md`.
- Whole task complete → one result comment on the PRD ticket: outcome,
  verification command and result, follow-ups. Never paste `walkthrough.md`.
