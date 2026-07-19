# Solution Doc Format

Structure for `docs/solutions/<category>/<slug>.md` when a learning should outlive its task:

```markdown
---
title: ""
category: ""
problem_type: ""
source_task: ""
tags: []
created: "YYYY-MM-DD"
---
# Title
## Context
## Symptoms Or Trigger
## Root Cause Or Principle
## Working Solution
## What Did Not Work
## When To Apply
## Prevention Or Review Checklist
## References
```

For bug-track docs, `Symptoms Or Trigger` describes the observed symptom. For knowledge-track docs, it describes the situation that makes the guidance relevant.

## Categories

Use these unless the repository already has its own taxonomy. Prefer an existing category over a near-duplicate.

- `agent-workflow`: agent coordination, task tracking, harness behavior
- `architecture`: module shape, boundaries, design patterns, migration strategy
- `testing`: test strategy, fixtures, flaky tests, verification patterns
- `tooling`: CLI, build, install, release, scripts, developer tools
- `docs`: documentation structure, examples, stale references
- `data`: schemas, migrations, serialization, persistence
- `integration`: external services, APIs, compatibility, cross-module behavior
- `security`: credentials, permissions, sandboxing, access control

## Overlap Check

Before creating a new doc, search `docs/solutions/` if it exists. Compare overlap on:

- problem statement or situation
- root cause or principle
- solution approach
- referenced files, modules, or workflow steps
- prevention or review guidance

If most dimensions overlap, update the existing doc or recommend a targeted refresh. If only some overlap, create the new doc and link the related one. If no solution store exists, create it only when the learning is clearly reusable.

## Discoverability

If `docs/solutions/` is created or materially used and the repository's root instructions (`AGENTS.md`, `CLAUDE.md`, or equivalent) do not mention it, propose the smallest matching pointer. Apply it only when the user asked for discoverability, the current task already edits root instructions, or the repo already uses similar pointers and the doc would otherwise be hard to find.
