# Reusable Review Instruction

Use this structure when creating AI reviewer instructions that apply repeatedly to a repository or organization. It should contain durable review contracts, not PR/diff-specific change details.

## Required Sections

### Source Discovery

- If repository or filesystem access is available, list the standard candidates checked with `rg --files` and the results.
- Record project instructions, README/runbook, docs, `.github`, task files, and design notes reflected in the reusable instructions.
- Mark absent candidates as `absent`; if repository/filesystem access is unavailable, write `N/A: no repository or filesystem access`.

### Scope

- Name the repo, service, package, team, or review surface these instructions apply to.
- List repos or paths that are excluded.

### Evidence Source

- Classify evidence as provided, repository, filesystem, or external/referenced.
- Distinguish durable sources reflected in the reusable instructions from short-lived change-specific sources.
- If there is no diff-specific evidence, write `N/A: reusable instruction, not change-specific`.

### Repo-wide Invariant

- List durable rules that every review must preserve.
- Include API contracts, data integrity, auth boundaries, compatibility, idempotency, migration/rollback, observability, and operator workflows.

### Review Rejection Rules

- List conditions that must not become findings.
- If the output will be pasted into an external reviewer, include the necessary rejection rules directly instead of referencing filenames only.
- Add repo-specific false positives when they exist.

### Severity Policy

- Summarize how P0/P1/P2/P3 and confidence should be separated.
- If the output will be pasted into an external reviewer, directly summarize the P0/P1/P2/P3 and confidence criteria.
- State any repo-specific escalation/downgrade criteria that differ from the default rubric.

### Suppression Policy

- List reusable suppressions from `false-positive-patterns.md` and repo-local suppression files.
- If none apply, write `none known`.

### Review Focus

- List areas that repeatedly deserve deeper review.
- Examples: retry semantics, auth boundaries, migration ordering, compatibility, generated files, operator contracts.

### Non-Goal

- List intentionally out-of-scope work that should not become review findings.
- If none apply, write `none known`.

### Open Questions

- List questions that must be answered before turning them into reusable instructions.
- Put low-confidence candidates and items whose existence depends on unverified assumptions here instead of finalizing them as finding instructions.
- If there are no questions, write `none known`.

## Minimal Template

```md
## Reusable Review Instruction

### Source Discovery
- N/A: <reason>

### Scope
- N/A: <reason>

### Evidence Source
- N/A: <reason>

### Repo-wide Invariant
- N/A: <reason>

### Review Rejection Rules
- Do not raise findings unrelated to a changed line or nearby line.
- Treat items whose existence depends on unstated assumptions, low-confidence concerns, unsupported configurations, clear operator error, non-goals, false-positive suppressions, or style-only preferences as questions or non-blocking notes instead of findings.

### Severity Policy
- P0: immediate production-breaking issue, data loss/corruption, critical security exposure, deploy-blocking outage.
- P1: supported-path contract violation or high-confidence production/user-visible regression that must be fixed before merge.
- P2: supported edge-path bug, bounded semantics issue, changed-behavior test gap, realistic operator-error risk, touched-code maintainability risk.
- P3: polish, naming, local readability, small docs clarification, low-risk test cleanup.
- Separate confidence from severity: high means direct evidence; medium means the finding exists based on evidence but one non-decisive detail remains; low means supported behavior or failure mode depends on an unstated assumption and should be a question.

### Suppression Policy
- none known

### Review Focus
- N/A: <reason>

### Non-Goal
- none known

### Open Questions
- none known
```
