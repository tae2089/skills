---
name: execute-dispatch-unit
description: Execute exactly one assigned dispatch packet or atomic work unit, staying inside allowed scope, respecting non-goals and forbidden scope, verifying the result, and returning a structured completion report. Use when an agent, worker, or subagent is handed a bounded task with fields such as unit_id, objective, allowed_scope, dependencies, acceptance_criteria, verification, or return_contract — typically a packet produced by decompose-and-dispatch.
---

# Execute Dispatch Unit

Use this skill when you are the executor for one dispatched work unit. Your job is not to redesign the plan. Your job is to complete the assigned unit, stay inside its boundaries, and report back clearly.

This is the executor counterpart of `decompose-and-dispatch`, which produces the dispatch packets and handoff prompts this skill consumes. The packet field names below mirror that skill's handoff contract.

If the packet conflicts with higher-priority system, developer, platform, safety, or repository instructions, follow the higher-priority instructions and report the conflict.

## Execution Loop

Follow this sequence:

1. Parse the dispatch packet.
2. Confirm the unit is executable with the provided context.
3. Identify allowed scope, forbidden scope, non-goals, dependencies, and acceptance criteria.
4. Perform only the assigned work.
5. Verify according to the packet when possible.
6. Return the completion report.

Do not execute adjacent work just because it looks useful. Do not change the plan unless the packet explicitly asks you to revise planning artifacts.

## Required Packet Fields

A good dispatch packet should include:

```yaml
unit_id: W3
objective: "Add validation for missing project slug"
capability: implementer
allowed_scope:
  - "src/api/projects/*"
  - "tests/api/projects/*"
forbidden_scope:
  - "database migrations"
  - "frontend UI"
non_goals:
  - "Do not redesign project routing"
dependencies:
  - "W1 discovery summary"
acceptance_criteria:
  - "Missing slug returns a typed validation error"
  - "Existing valid slug behavior remains unchanged"
verification:
  - "Run targeted project API tests if available"
return_contract: completion_report
```

If a packet is missing a field, continue only when the intent and safe scope are still clear. Otherwise return `BLOCKED`.

## Boundary Rules

Treat boundaries as hard constraints:

- Edit only inside `allowed_scope`.
- Never edit `forbidden_scope`.
- Treat `non_goals` as explicit out-of-scope work.
- Do not revert or overwrite unrelated changes.
- Assume other executors may be working in the same repository.
- Prefer the smallest change that satisfies the acceptance criteria.
- If you discover a broader issue, report it as a follow-up instead of expanding scope.

For read-only units, do not edit files. Return findings with concrete references.

For write units, list every changed file in the completion report.

## Dependency Handling

Before work starts, check dependencies:

- If dependency outputs are included, use them as input.
- If a dependency is missing but the packet is still safely executable, proceed and note the assumption.
- If a missing dependency changes the objective, scope, or acceptance criteria, return `BLOCKED`.
- If your findings contradict a dependency output, stop and report the conflict.

Do not silently reinterpret another unit's output.

## Verification Rules

Run the requested verification when it is available and safe.

If the exact verification cannot run:

- Try the nearest safe targeted check.
- State why the requested verification could not run.
- Distinguish between verified behavior and unverified assumptions.

Do not claim success without evidence. Use `PARTIAL` when implementation is complete but verification is incomplete.

## Stop Conditions

Stop and return `BLOCKED` when:

- The objective is ambiguous.
- Safe scope is unclear.
- The task requires editing forbidden files.
- A required dependency output is missing.
- The acceptance criteria conflict with each other.
- The task requires credentials, approvals, network, tools, or external systems that are unavailable.
- Verification is mandatory and no safe verification path exists.
- You discover likely overlap with another executor's write scope.

When blocked, do not guess. Return the smallest question or missing input that would unblock the unit.

## Completion Report

Return exactly one completion report at the end.

Use this format:

```yaml
unit_id: W3
status: DONE | PARTIAL | BLOCKED | FAILED
summary:
  - "What changed or what was found"
changed_files:
  - "path/to/file"
verification:
  attempted:
    - "command or check"
  result: "pass | fail | not_run"
  evidence:
    - "short result, error, or reason"
blockers:
  - "missing input, permission, dependency, or conflict"
follow_ups:
  - "out-of-scope issue or recommended next unit"
notes:
  - "important assumption or integration note"
```

Use `DONE` only when the acceptance criteria are satisfied and verification is adequate for the packet. Use `PARTIAL` when useful work is complete but verification or a secondary criterion remains unresolved. Use `FAILED` when you attempted the unit and could not produce a usable result.

## Output Discipline

Keep the report compact and integration-ready.

Do not include long logs unless requested. Summarize logs and point to files or commands. If you made code or artifact changes, include enough detail for the orchestrator to review and integrate them without rereading your full process.

## Reference Files

- `reference/example.md` — End-to-end worked example: receive a packet, confirm boundaries, do the work, verify, and return a completion report.
- `agents/example.yaml` — Illustrative adapter interface config (`display_name`, `short_description`, `default_prompt`) showing how a host runtime can surface this skill. Treat it as a template, not portable semantics.
