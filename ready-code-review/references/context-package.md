# Context Package

Use this structure when preparing review context before requesting a code review. It can be used without a PR or git diff when provided evidence, filesystem evidence, or referenced evidence is sufficient.

## Required Sections

### Source Discovery

- If repository or filesystem access is available, list the standard candidates checked with `rg --files` and the results.
- Record discovered project instructions, README/runbook, docs, `.github`, task files, and design notes.
- Mark absent candidates as `absent`; if repository/filesystem access is unavailable, write `N/A: no repository or filesystem access`.

### Evidence Source

- Classify evidence as provided, repository, filesystem, or external/referenced.
- Distinguish orientation evidence from change evidence.
- If only `git status`, file lists, PR titles, or task descriptions are available, mark change evidence as missing.

### Change Summary

- Summarize behavioral changes in 1-5 bullets.
- Name affected modules, endpoints, commands, jobs, schemas, and config keys.
- Distinguish structural-only changes from behavioral changes.
- If change evidence is insufficient, do not assert changed behavior; write `N/A: change evidence missing` or leave a question.

### Reason

- State the problem being solved and the impact on users, operators, or developers.
- Include relevant issue, incident, design, or runbook context when available.
- Record decisions that are not visible from code alone.

### Reviewer Focus

- List the areas where careful review is most valuable.
- Prefer specific risks: retry semantics, membership changes, auth boundaries, migration ordering, concurrency, persistence, compatibility, observability, test integrity, and similar concerns.

### Invariant / Contract

- List rules that must remain true after the change.
- Include API contracts, data integrity rules, idempotency, backward compatibility, operational runbooks, and failure semantics.
- Write each invariant so a reviewer can test or disprove it.

### Operational Contract

Capture assumptions about how the system runs:

- startup flags and defaults
- deployment ordering
- feature flags
- migrations and rollback
- alert/dashboard/runbook expectations
- operator responsibilities
- Label unverified assumptions with `Assumption:` and move them to Open Questions if they determine whether a finding exists.

### Known Non-Goal

- List intentionally out-of-scope work.
- Include refactors, optimizations, API redesigns, migrations, docs, or compatibility cleanup that should not become review findings.

### False-positive Suppression

- List suppressions from `false-positive-patterns.md` and any repo-local suppression files that apply to this review.
- If none apply, write `none known`.
- Express each suppression as a specific pattern that should block or downgrade findings.

### Test / Verification Evidence

- List added or changed tests and what each proves.
- List commands run and their results.
- List untested items and why the gap is acceptable.

### Known Risk

- State unresolved risks honestly.
- Say whether each risk should block merge, needs follow-up, or is accepted under the current contract.

### Open Questions

- List questions that cannot be turned into finding instructions because evidence, supported behavior, or contracts are missing.
- If there are no questions, write `none known`.

## Minimal Template

```md
## Review Context

### Source Discovery
- N/A: <reason>

### Evidence Source
- N/A: <reason>

### Change Summary
- N/A: <reason>

### Reason
- N/A: <reason>

### Reviewer Focus
- N/A: <reason>

### Invariant / Contract
- N/A: <reason>

### Operational Contract
- N/A: <reason>

### Known Non-Goal
- none known

### False-positive Suppression
- none known

### Test / Verification Evidence
- N/A: <reason>

### Known Risk
- none known

### Open Questions
- none known
```
