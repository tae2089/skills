# Severity Rubric

This file is the canonical source for severity definitions. Short-form P0–P3 one-liners are mirrored
verbatim in paste-ready outputs — `reviewer-prompt-template.md`, `severity-calibration.md`, and
`reusable-instruction.md` — so those outputs stand alone without repository access. When you change a
severity definition here, update every mirrored copy in the same edit.

Use severity labels only when a finding has concrete evidence.

## P0

Use P0 for immediate, high-confidence production-breaking issues:

- likely or already-occurring data loss or corruption
- critical security exposure with a plausible exploit path
- primary-path outage or deploy-blocking failure
- irreversible destructive action without required confirmation

## P1

Use P1 for blocking defects that must be fixed before merge:

- clear violation of a documented contract or invariant
- high-confidence availability, quorum, auth, data-integrity, or compatibility regression
- broken user-visible behavior on a normal supported path
- retry/idempotency behavior that can produce an incorrect client-visible outcome
- missing migration, rollback, or safety gate for a risky state change

Do not use P1 for unsupported operations, missing required configuration, or scenarios that require speculative misuse unless code or docs promise support for that scenario.

## P2

Use P2 for important but non-emergency defects:

- bug on an edge path or uncommon but supported configuration
- ambiguous error semantics that can mislead clients but have limited blast radius
- plausible implementation with missing tests for changed behavior
- documentation or runbook gap that can cause realistic operator error
- maintainability issue in touched code that is likely to cause future defects

## P3

Use P3 for minor issues:

- polish, naming, local readability, small docs clarification
- low-risk test cleanup
- non-blocking consistency issue

## Operator Error vs Code Defect

Classify as a code defect when:

- code violates a documented contract in a supported configuration
- a default silently creates unsafe behavior in the normal documented workflow
- the system cannot fail clearly when required input is missing
- existing tests or docs imply the scenario should work

Classify as operator/configuration error when:

- an operator skipped a documented required flag, secret, migration, or runbook step
- the system behaved according to explicit startup configuration
- the requested behavior conflicts with the stated operational contract

When the boundary is unclear, do not escalate severity; recommend documentation or validation improvement.

## Confidence

Attach confidence separately from severity:

- High: direct evidence from code, tests, docs, reproduced output, or logs.
- Medium: code-path evidence is strong and the finding's existence is decided by evidence, but one non-decisive detail remains, such as blast radius, exact environment, or frequency.
- Low: plausible risk whose supported behavior or failure mode depends on an unstated assumption. Ask a targeted question instead of raising a finding.
