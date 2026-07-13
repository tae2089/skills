# Dispatch Plan And Handoff Format

## Dispatch Plan Format

For normal chat output, use a compact table:

| Step | Objective | Capability | Resolution | Executor | Dependencies | Parallel | Output | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W1 | Locate relevant code paths | researcher | existing | `repo-scout` | none | yes | file refs + summary | references checked |

For complex plans, add a spec resolution table before the work-unit table:

| Unit | Required Spec (summary) | Resolution | Executor | Confidence | Evidence |
| --- | --- | --- | --- | --- | --- |
| W1 | read-only researcher, repo search | existing | `repo-scout` | high | description says read-only code exploration |
| W3 | write-scoped implementer, middleware only | existing | `builder` | high | edit-capable implementation role |
| W4 | tester, run commands, no file writes | instantiated | ad-hoc subagent | high | no named tester; runtime spawns arbitrary-prompt subagents |
| W5 | reviewer, read-only | instantiated | ad-hoc subagent | high | no named reviewer; spec fully encodable as preamble |
| W6 | integrate results, final synthesis | main-agent | `main-agent` | high | orchestration stays with the main agent |

Then produce the dispatch plan.

## Dispatch Packet

A dispatch packet is the structured form of one delegated work unit — the contract the `execute-dispatch-unit` skill consumes, and the task contract registered in the durable ledger when the `agent-team` CLI is available. Full example: `examples/dispatch-packet.example.yaml`.

Packet fields, derived from the work-unit schema in `work-units.md`:

| Packet Field | Source |
| --- | --- |
| `unit_id` | work unit `id` |
| `objective` | work unit `objective` |
| `required_executor_spec` | work unit spec, verbatim |
| `resolution` | work unit resolution, verbatim |
| `allowed_scope` / `forbidden_scope` | work unit `scope` + `ownership`, made explicit as path or artifact patterns |
| `non_goals` | boundaries the unit must not cross |
| `dependencies` | work unit `dependencies`, each as a unit id plus a one-line note on what it must have produced |
| `acceptance_criteria` | the unit's completion bar — what the executor's `DONE` is judged against |
| `verification` | commands, checks, or evidence expectations |
| `return_contract` | expected report shape (normally `completion_report`) |
| `handoff_prompt` | the self-contained prompt below, rendered from the fields above |

## Handoff Prompt Contract

When delegation is possible, include a `handoff_prompt` for each delegated work unit. The prompt must be self-contained and should not rely on hidden context from the orchestrator. Derive it from the packet: the spec's `context` becomes the inputs, its `permissions` become the edit/read-only line, `acceptance_criteria` become the completion bar, `verification` becomes the verification expectation.

Each handoff prompt should include:

- A request to use the `execute-dispatch-unit` skill when it is available (host-neutral phrasing; host adapters may substitute their own invocation syntax).
- The work-unit id and objective.
- Relevant inputs and file, module, or artifact scope.
- Explicit non-goals.
- Ownership boundary and conflict warning.
- Acceptance criteria — the conditions the executor's `DONE` claim is judged against.
- Expected output format.
- Verification expectation.
- Whether the executor may edit files or must stay read-only.

Use this shape:

```text
Use the execute-dispatch-unit skill if available.

Task W2: Implement the API validation change.
Scope: edit only src/api/validation/* and tests under tests/api_validation/*.
Non-goals: do not change persistence or UI behavior.
Ownership: other executors may be working elsewhere; do not revert unrelated changes.
Acceptance: invalid payloads return a typed validation error; valid payload behavior unchanged.
Expected output: list changed files, summarize behavior change, report verification commands and results.
Verification: run the targeted API validation tests if available.
```

### Instantiation Preamble

For `instantiated` executors, prepend the spec's role and permission constraints as a preamble, before the task body. The preamble is what makes an ad-hoc general-purpose subagent behave like the executor the spec requires:

```text
Role: You are a test runner. You execute test commands and report evidence; you do not edit source files.
Permissions: file access read-only; command execution allowed; no network.

Use the execute-dispatch-unit skill if available.

Task W4: Verify rate limiting behavior.
...
```

Keep the preamble faithful to the spec — do not grant permissions the spec withholds. When the runtime's spawn mechanism can also restrict tools or write access, apply the restriction there as well; the preamble alone is instruction, not enforcement.

The same constraint preamble also applies to `existing` executors whose permissions exceed the spec (e.g. a write-capable builder resolved to a read-only research spec): prepend the spec's permission line so the broader executor stays inside the spec.

If a work unit is not delegated, omit the full prompt or keep it as a short execution note.
