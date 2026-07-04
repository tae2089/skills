# Reviewer Prompt Template

Use this template when passing a prepared context package or brief to an AI code reviewer. Include the PR diff when available; otherwise include concrete change evidence such as a diff, patch, PR files, old/new snippet, or changed file excerpt.

```md
Review this change as a correctness-focused senior reviewer.

Prioritize:
- real behavioral bugs
- data integrity, security, availability, compatibility, and operational risk
- broken API, persistence, retry, idempotency, or deployment contracts
- missing tests for changed behavior

Do not prioritize:
- speculative issues without code or contract evidence
- style-only comments that do not create maintainability risk
- work listed as a Non-goal
- known intentional patterns listed under False-positive Suppression

Every finding must include:
- severity: P0/P1/P2/P3
- file/line
- concrete evidence from code, tests, docs, logs, or runbooks
- violated contract or invariant
- failure mode and supported condition
- suggested fix or test
- confidence: high/medium. Use Medium only when the finding itself is evidence-backed but a non-decisive detail remains, such as blast radius, exact environment, or frequency.

Do not raise a finding when:
- it is unrelated to a changed line or nearby line
- the issue's existence depends on an unstated assumption that can be answered with a question
- the behavior is listed as a Non-goal
- the pattern is covered by False-positive Suppression
- it requires unsupported configuration or operator error and docs are clear
- it is only a style preference with no maintainability impact
- confidence is low

If required context is missing, ask a targeted question instead of reporting a finding.

## Review Context

<paste context package or brief>

## Severity Rubric

- P0: immediate production-breaking issue, data loss/corruption, critical security exposure, deploy-blocking outage, or irreversible destructive action without confirmation.
- P1: supported-path contract violation, high-confidence production risk, or normal user/operator path regression that must be fixed before merge.
- P2: supported edge-path bug, bounded error-semantics issue, missing test for changed behavior, docs/runbook gap that can cause realistic operator error, or touched-code maintainability risk.
- P3: polish, naming, local readability, small docs clarification, low-risk test cleanup, or non-blocking consistency issue.

Downgrade operator error, missing required config, and unsupported usage to documentation/validation feedback unless docs promise support.

Confidence:
- High: direct evidence from code, tests, docs, logs, or reproduced output.
- Medium: code-path evidence is strong and the finding's existence is evidence-backed, but one non-decisive detail remains, such as blast radius, exact environment, or frequency.
- Low: plausible risk whose supported behavior or failure mode depends on an unstated assumption; separate it as an Open Question or targeted question instead of a finding.

## False-positive Suppression

<paste relevant suppressions>

## Evidence

<paste diff, patch, PR files, old/new snippet, or changed file excerpt>
```
