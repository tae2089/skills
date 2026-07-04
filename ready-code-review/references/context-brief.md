# Review Context Brief

Use this structure for short review context briefs. The goal is not to perform the review, but to compress the core evidence and questions a reviewer should see first.

## Required Sections

### Source Discovery

- If repository or filesystem access is available, briefly list the standard candidates checked with `rg --files` and the results.
- Record discovered project instructions, README/runbook, docs, `.github`, task files, and design notes.
- Mark absent candidates as `absent`; if repository/filesystem access is unavailable, write `N/A: no repository or filesystem access`.

### Evidence Source

- List the evidence sources used.
- Distinguish change evidence from supporting evidence.
- If change evidence is missing, write `N/A: <reason>` and the needed question.

### Review Focus

- List 1-5 areas where reviewer attention is most valuable.
- Prefer specific contracts, paths, and risks.

### Non-Goal

- List intentionally out-of-scope items that should not become review findings.
- If none apply, write `none known`.

### False-positive Suppression

- List applicable suppressions.
- If none apply, write `none known`.

### Open Questions

- List questions that cannot be turned into finding instructions because evidence or contracts are missing.
- Put unverified assumptions that determine whether a finding exists here as questions.
- If there are no questions, write `none known`.

## Minimal Template

```md
## Review Context Brief

### Source Discovery
- N/A: <reason>

### Evidence Source
- N/A: <reason>

### Review Focus
- N/A: <reason>

### Non-Goal
- none known

### False-positive Suppression
- none known

### Open Questions
- none known
```
