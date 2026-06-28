# Worked Example

End-to-end run of the Core Loop for one goal. Use it as a shape, not a fixed answer.

## Goal

> "Add rate limiting to the public API and make sure it doesn't break existing clients."

## 1. Restate goal and success criteria

- Goal: add rate limiting to the public API.
- Success: limits enforced on public endpoints; existing authenticated clients unaffected; verified by tests.

## 2. Capability inventory

Runtime discovery (see `matching.md`) finds:

- Named subagent `repo-scout` — description says read-only code exploration. → `researcher`, confidence high.
- Named subagent `builder` — edit-capable implementation role. → `implementer`, confidence high.
- No test-specific or review-specific executor. → `tester`, `reviewer` fall back to `main-agent`.
- Delegation mechanism: subagents available. User asked to "coordinate agents", so delegation is allowed.

## 3-5. Decompose, classify, map

| Step | Objective | Capability | Executor | Confidence |
| --- | --- | --- | --- | --- |
| W1 | Find where requests enter and where auth/middleware runs | researcher | `repo-scout` | high |
| W2 | Find existing client usage patterns and rate assumptions | researcher | `repo-scout` | high |
| W3 | Implement rate-limit middleware + config | implementer | `builder` | high |
| W4 | Add tests: limit enforced, authed clients exempt within quota | tester | `main-agent` | low (fallback) |
| W5 | Review for regressions and missing edge cases | reviewer | `main-agent` | low (fallback) |

## 6. Quality gate

Each unit passes (see `work-units.md`). W3 ownership bounded to middleware + config files only — no persistence or auth changes. W3 and W4 must not edit the same files concurrently.

## 7. Dependencies and parallelism

```yaml
parallel_groups:
  - id: P1
    units: [W1, W2]
    reason: "read-only discovery, no shared write scope"
dependencies:
  W3: [W1, W2]
  W4: [W3]
  W5: [W3, W4]
```

## 8. Dispatch plan with handoff

P1 (W1, W2) dispatched in parallel to `repo-scout`. After they return, W3 to `builder`:

```text
Task W3: Implement rate-limit middleware for the public API.
Scope: edit only the request-middleware module and its config; add the limiter there.
Inputs: entry points from W1, client patterns from W2.
Non-goals: do not change auth logic, persistence, or response schemas.
Ownership: W4 will add tests after you finish — do not write test files yourself.
Expected output: changed files, summary of limit behavior and defaults, config keys added.
Verification: app builds; existing endpoint handlers untouched in behavior.
```

W4, W5 stay on `main-agent` (no specialized executor).

## 9. Status

`READY_WITH_FALLBACKS` — research and implementation map to high-confidence executors; testing and review fall back to the main agent but execution can proceed.
