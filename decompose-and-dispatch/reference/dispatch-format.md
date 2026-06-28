# Dispatch Plan And Handoff Format

## Dispatch Plan Format

For normal chat output, use a compact table:

| Step | Objective | Capability | Executor | Dependencies | Parallel | Output | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| W1 | Locate relevant code paths | researcher | `main-agent` | none | yes | file refs + summary | references checked |

For complex plans, add a mapping table before the work-unit table:

| Capability | Candidate Executors | Selected Executor | Confidence | Evidence |
| --- | --- | --- | --- | --- |
| researcher | `repo-scout`, `main-agent` | `repo-scout` | high | description says read-only code exploration |
| implementer | `builder`, `main-agent` | `builder` | high | edit-capable implementation role |
| tester | none | `main-agent` | low | no test-specific executor found |

Then produce the dispatch plan.

## Handoff Prompt Contract

When delegation is possible, include a `handoff_prompt` for each delegated work unit. The prompt must be self-contained and should not rely on hidden context from the orchestrator.

Each handoff prompt should include:

- The work-unit id and objective.
- Relevant inputs and file, module, or artifact scope.
- Explicit non-goals.
- Ownership boundary and conflict warning.
- Expected output format.
- Verification expectation.
- Whether the executor may edit files or must stay read-only.

Use this shape:

```text
Task W2: Implement the API validation change.
Scope: edit only src/api/validation/* and tests under tests/api_validation/*.
Non-goals: do not change persistence or UI behavior.
Ownership: other executors may be working elsewhere; do not revert unrelated changes.
Expected output: list changed files, summarize behavior change, report verification commands and results.
Verification: run the targeted API validation tests if available.
```

If a work unit is not delegated, omit the full prompt or keep it as a short execution note.
