# Finding Contract

A review finding is valid only when it includes enough evidence for the author to verify it.

## Required Fields

Each finding must include:

- `severity`: P0, P1, P2, or P3
- `file/line`: exact changed line or nearby line
- `evidence`: code, test, docs, log, command output, or runbook text
- `violated_contract`: broken invariant, API contract, operational contract, or user expectation
- `failure_mode`: what goes wrong and under which conditions
- `suggested_fix_or_test`: concrete next action
- `confidence`: high or medium. Low-confidence items and items whose existence depends on unresolved assumptions must be Open Questions.

## Rejection Rules

This is the canonical source for rejection rules. Paste-ready outputs restate them: in full in
`reviewer-prompt-template.md`, and as a compressed summary in `severity-calibration.md` (Finding
Rejection Rules) and `reusable-instruction.md` (Review Rejection Rules). When you add or change a rule
here, update those restatements in the same edit so no rule is dropped from the summaries.

Do not raise a finding when:

- the issue's existence depends on an unstated assumption that can be answered with a question
- the behavior is explicitly listed as a non-goal
- the pattern is covered by false-positive suppression
- the comment is only a style preference with no maintainability impact
- the issue requires unsupported configuration or operator error and docs are clear
- there is no changed-line relevance
- confidence is low

## Missing Context

If the reviewer cannot classify an issue without more information, require an open question:

```md
Question: Is <condition> a supported operational path? If yes, <code path> may violate <contract>. If not, documenting it as an operator requirement is preferable.
```

Do not raise low-confidence items or items whose existence depends on unresolved assumptions as findings; keep them as Open Questions.

## Good Finding Shape

```md
- [P2] Preserve retryable leader-transition errors for forwarded writes
  File: server/admin.go:99
  Evidence: forwarded leader failure returns an untyped error and falls through to the bad-request path in statusForError.
  Violated contract: write failures during election must remain retryable 5xx responses.
  Failure mode: clients may stop instead of retrying a mutation that should be retried.
  Suggested fix/test: map forwarded leader 5xx failures into the existing retryable error taxonomy and add a follower-forwarding test.
  Confidence: high.
```
