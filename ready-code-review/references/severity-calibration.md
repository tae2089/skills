# Severity / Suppression Calibration

Use this structure when calibrating only P0/P1/P2/P3, blocking/non-blocking, confidence, or false-positive suppression. It can be used without PR/diff-specific change details, but applying it to actual findings or a specific change requires change evidence.

## Required Sections

### Source Discovery

- If repository or filesystem access is available, list the standard candidates checked with `rg --files` and the results.
- Record project instructions, README/runbook, docs, `.github`, task files, and design notes reflected in the calibration.
- Mark absent candidates as `absent`; if repository/filesystem access is unavailable, write `N/A: no repository or filesystem access`.

### Scope

- Name the repo, service, package, PR, review surface, or reviewer this calibration applies to.
- List paths, reviewer types, or change classes that are excluded.

### Evidence Source

- Classify evidence as provided, repository, filesystem, or external/referenced.
- For change-specific calibration, distinguish orientation evidence from change evidence.
- If change evidence is missing, state that this calibrates only severity/suppression policy and does not apply policy to actual findings.

### Severity Summary

- Summarize P0/P1/P2/P3 according to `severity-rubric.md`.
- If repo-specific escalation/downgrade criteria exist, state how they differ from the default rubric.
- Separate conditions where unsupported configuration, operator error, or speculative misuse may become blocking findings from conditions where they cannot.

### Confidence Policy

- Define High, Medium, and Low separately from severity.
- Limit Medium to cases where the finding's existence is evidence-backed and only non-decisive details remain.
- Put Low items or items whose existence depends on unstated assumptions into Open Questions.

### Finding Rejection Rules

- Summarize the rejection rules from `finding-contract.md` directly in the output.
- Include changed-line relevance, evidence contract, non-goals, suppressions, unsupported configuration, style-only preference, and low-confidence handling.

### False-positive Suppression

- List applicable suppressions from `false-positive-patterns.md` and repo-local suppression files.
- If none apply, write `none known`.
- Express each suppression as a specific pattern that should block or downgrade findings.

### Open Questions

- List questions that must be answered before finalizing severity or suppression policy.
- If there are no questions, write `none known`.

## Minimal Template

```md
## Severity / Suppression Calibration

### Source Discovery
- N/A: <reason>

### Scope
- N/A: <reason>

### Evidence Source
- N/A: <reason>

### Severity Summary
- P0: immediate production-breaking issue, data loss/corruption, critical security exposure, deploy-blocking outage.
- P1: supported-path contract violation or high-confidence production/user-visible regression that must be fixed before merge.
- P2: supported edge-path bug, bounded semantics issue, changed-behavior test gap, realistic operator-error risk, touched-code maintainability risk.
- P3: polish, naming, local readability, small docs clarification, low-risk test cleanup.

### Confidence Policy
- High: direct code, test, docs, log, or reproduced-output evidence.
- Medium: the finding's existence is evidence-backed, but one non-decisive detail remains.
- Low: supported behavior or failure mode depends on an unstated assumption, so this is a question rather than a finding.

### Finding Rejection Rules
- Do not raise findings unrelated to a changed line or nearby line.
- Treat items whose existence depends on unstated assumptions, low-confidence concerns, unsupported configurations, clear operator error, non-goals, false-positive suppressions, or style-only preferences as questions or non-blocking notes instead of findings.

### False-positive Suppression
- none known

### Open Questions
- none known
```
