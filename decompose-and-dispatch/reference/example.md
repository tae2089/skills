# Worked Example

End-to-end run of the Core Loop for one goal. Use it as a shape, not a fixed answer.

## Goal

> "Add rate limiting to the public API and make sure it doesn't break existing clients."

## 1. Restate goal and success criteria

- Goal: add rate limiting to the public API.
- Success: limits enforced on public endpoints; existing authenticated clients unaffected; verified by tests.

## 2. Decompose

| Step | Objective |
| --- | --- |
| W1 | Find where requests enter and where auth/middleware runs |
| W2 | Find existing client usage patterns and rate assumptions |
| W3 | Implement rate-limit middleware + config |
| W4 | Add tests: limit enforced, authed clients exempt within quota |
| W5 | Review for regressions and missing edge cases |

## 3. Author required executor specs

Written from each unit's needs, before looking at the runtime:

| Unit | Role (spec) | Capability | Permissions |
| --- | --- | --- | --- |
| W1, W2 | read-only code researcher; locates code, never edits | researcher | file read-only, no exec |
| W3 | implementer bounded to middleware + config files | implementer | write-scoped, exec for build |
| W4 | test writer/runner; edits test files only, runs test commands | tester | write-scoped (tests only), exec |
| W5 | correctness reviewer; reads diff, reports findings, never edits | reviewer | file read-only, no exec |

## 4. Capability inventory

Runtime discovery (see `matching.md`) finds:

- Named subagent `repo-scout` — description says read-only code exploration.
- Named subagent `builder` — edit-capable implementation role.
- No test-specific or review-specific named executor.
- The runtime can spawn arbitrary-prompt subagents → the `instantiated` rung exists.
- User asked to "coordinate agents", so delegation is allowed.

## 5. Resolve each spec

| Unit | Required Spec (summary) | Resolution | Executor | Confidence | Evidence |
| --- | --- | --- | --- | --- | --- |
| W1, W2 | read-only researcher | existing | `repo-scout` | high | description says read-only code exploration |
| W3 | write-scoped implementer | existing | `builder` | high | edit-capable implementation role |
| W4 | tester, test-files-only writes | instantiated | ad-hoc subagent | high | no named tester; runtime spawns arbitrary-prompt subagents |
| W5 | read-only reviewer | instantiated | ad-hoc subagent | high | no named reviewer; spec fully encodable as preamble |

No `NEEDS_USER_MAPPING`: the unsatisfied specs resolve by instantiation instead of a user question.

## 6. Quality gate

Each unit passes (see `work-units.md`). W3 ownership bounded to middleware + config files only — no persistence or auth changes. W3 and W4 must not edit the same files concurrently; W4's spec restricts writes to test files.

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
Use the execute-dispatch-unit skill if available.

Task W3: Implement rate-limit middleware for the public API.
Scope: edit only the request-middleware module and its config; add the limiter there.
Inputs: entry points from W1, client patterns from W2.
Non-goals: do not change auth logic, persistence, or response schemas.
Ownership: W4 will add tests after you finish — do not write test files yourself.
Acceptance: limits enforced on public endpoints; authenticated clients within quota unaffected.
Expected output: changed files, summary of limit behavior and defaults, config keys added.
Verification: app builds; existing endpoint handlers untouched in behavior.
```

W4 goes to an instantiated executor — the spec becomes the preamble:

```text
Role: You are a test writer and runner. You edit test files only and run test commands; you never edit production source.
Permissions: file access write-scoped to tests/*; command execution allowed; no network.

Use the execute-dispatch-unit skill if available.

Task W4: Add tests for rate limiting.
Scope: edit only tests/api/rate_limit/*.
Inputs: W3's changed files and limit defaults.
Non-goals: do not modify the middleware implementation.
Ownership: W3 owns the middleware implementation; other executors may be active — do not edit production source.
Acceptance: tests cover limit enforcement and authed-client exemption, and they pass.
Expected output: test files added, test run output showing limits enforced and authed clients exempt.
Verification: targeted rate-limit tests pass; report the command and results.
```

W5 is instantiated the same way with a read-only reviewer preamble.

## 9. Delegation check and status

Delegation is allowed (per the inventory in step 4: the user asked to coordinate agents and the runtime supports subagents), so the handoffs above are dispatched.

`READY_TO_EXECUTE` — every spec resolves to a satisfying existing executor or a spec-faithful instantiated one; no main-agent fallbacks were forced.
