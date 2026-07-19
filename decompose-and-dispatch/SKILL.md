---
name: decompose-and-dispatch
description: Decompose a complex goal into independently executable work units and resolve each unit to an executor. Use when the user requests delegated, parallel, or multi-agent work, or when multiple units require dependency, ownership, or capability coordination. Skip ordinary sequential implementation by one agent.
---

# Decompose And Dispatch

Use this skill to turn a goal into the smallest practical work units, state what executor each unit _needs_, and only then resolve those needs against whatever the current runtime actually offers.

The skill is spec-first: the required executor spec is a first-class artifact authored from the work unit's needs, independent of which agents happen to exist. Matching against existing executors is a secondary check — a spec-satisfaction test, not the starting point.

The skill is runtime-neutral. Do not assume agent names are standardized. Agent names are local aliases, not portable semantics.

## Core Loop

Follow this sequence:

1. Restate the user goal and success criteria.
2. Decompose the goal into atomic work units.
3. Author a required executor spec for each unit (see Required Executor Spec below).
4. Build an execution capability inventory for the current runtime: delegation mechanisms, named executors, and whether arbitrary-prompt subagents can be instantiated.
5. Resolve each spec down the resolution ladder (see below).
6. Apply the work unit quality gate.
7. Mark dependencies, parallelism, ownership, risks, and verification.
8. Produce a dispatch plan with handoff prompts when delegation is possible. Handoff prompts are derived from the spec; instantiated executors get the spec's role and permission constraints as a preamble.
9. Only delegate or spawn work when delegation is allowed. Delegation is allowed only when the runtime supports it and the user asked for delegation, subagents, workers, parallel execution, or an execution plan that assigns work — this is the single definition every reference file uses; the delegation rules in `reference/parallelism-and-delegation.md` add per-unit conditions.

## Required Executor Spec

Every work unit carries a spec describing the executor it needs, written before looking at what is available. A spec states:

- `role` — a one-line role definition, usable verbatim as an agent preamble.
- `capability` — one portable capability class (see table below), as shorthand.
- `tools` / `permissions` — what the executor must be able to do: file access (read-only, write-scoped, none), network, command execution.
- `context` — the inputs the executor must receive to work self-contained.
- `verification` — the evidence the executor must return.

The full schema lives in `reference/work-units.md`.

Portable capability classes (shorthand inside the spec — the spec adds the precision the class alone lacks):

| Capability     | Use For                                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------------------- |
| `orchestrator` | Plan control, sequencing, decisions, conflict resolution, integration, final synthesis                        |
| `researcher`   | Read-only code search, documentation research, source discovery, context gathering                            |
| `implementer`  | Code edits, refactors, artifact creation, migrations, fixes                                                   |
| `tester`       | Reproduction, command execution, test runs, verification evidence                                             |
| `reviewer`     | Correctness review, risk review, regression checks, missing-test analysis                                     |
| `specialist`   | Domain-specific reasoning such as security, frontend, data, platform, product, design, or framework expertise |
| `operator`     | Browser, app, cloud, MCP, connector, CLI, deployment, or external-system operation                            |
| `documenter`   | Specs, plans, changelogs, handoff notes, runbooks, user-facing docs                                           |

## Resolution Ladder

Resolve each spec in this order (satisfaction evidence, tie-breaking, and confidence rules in `reference/matching.md`):

1. **`existing`** — a named executor whose evidence satisfies the spec (preferred when it truly fits — curation beats an ad-hoc spec).
2. **`instantiated`** — nothing satisfies the spec, but the runtime can spawn arbitrary-prompt subagents able to carry the spec's tools and permissions: embed the spec's role and permission constraints as a handoff-prompt preamble, ephemerally.
3. **`main-agent`** — delegation is not allowed, or no available mechanism can satisfy the spec. Keep the unit on the main agent; the spec still drives sequencing and verification.

## Durable Ledger (optional, requires the `agent-team` CLI)

While building the capability inventory, check whether the `agent-team` CLI is runnable. When it is and delegation is allowed, register the dispatch plan in its out-of-process ledger so completion claims are gated and executor death leaves evidence:

- Create one run for the plan (`agent-team run create`) and one task per work unit (`agent-team task create`, with the unit's packet as the task contract). Record the run id and each task id in the dispatch plan.
- Every handoff prompt must carry the unit's ledger coordinates: `RUN_ID`, `TASK_ID`, `AGENT`, the artifact root `_workspace/RUN_ID/`, and the orchestrator's recipient name for messages. Executors mirror their lifecycle per the `execute-dispatch-unit` skill's ledger rules.
- The orchestrator monitors with `run status`/`task list`, and detects abandoned units with `task stale --older-than <duration>`. Before reassigning or retrying a stale unit, record vanish evidence: the unit id, its last ledger event, and the current git state of its `allowed_scope` classified as clean, dirty, or unknown.
- Close the run (`run close`) only after every task is terminal; the ledger rejects completion without evidence and an artifact path — treat a rejection as a real gap, not an obstacle to force past.

Before any ledger call, load the CLI's `agent-team-shared` skill if available — it defines the state directory, global flags, and error handling the command-specific `agent-team-*` skills assume. Command details live with those bundled skills and `--help`; they take precedence over the summaries here. When the CLI is absent, proceed exactly as before and note in the dispatch plan that no ledger is available (no completion gating, no stale detection).

## Reference Files

Load the relevant file when you reach that step. Do not load all of them up front.

- `reference/matching.md` — Runtime discovery checklist, the spec-satisfaction check, the resolution ladder in detail, instantiation rules, confidence levels, and runtime adapter notes.
- `reference/work-units.md` — Atomic work unit criteria, the quality gate, and the full work-unit YAML schema including the required executor spec and resolution blocks.
- `reference/dispatch-format.md` — Dispatch plan tables, spec resolution table, the dispatch packet schema (worked example in `examples/dispatch-packet.example.yaml`), and the handoff prompt contract including the instantiation preamble.
- `reference/parallelism-and-delegation.md` — Parallel grouping rules, conflict avoidance, and when to delegate vs keep on the main agent.
- `reference/example.md` — Full end-to-end worked example of the Core Loop, from goal to dispatch plan and status.

## Output Contract

End with one of these statuses:

- `READY_TO_EXECUTE`: The plan has clear units, specs, resolutions, dependencies, and verification. When delegation is not allowed, main-agent execution is the plan — not a fallback — so this status still applies.
- `READY_WITH_FALLBACKS`: Delegation was allowed but some specs could not be satisfied and fell back to the main agent; execution can proceed.
- `NEEDS_USER_MAPPING`: Spec satisfaction is ambiguous and instantiation cannot resolve it — exact conditions in `reference/matching.md`. User confirmation is needed before delegation.
- `BLOCKED`: Required context, permissions, or runtime capability is missing and no safe fallback exists.

When more than one status applies, report the most severe: `BLOCKED` > `NEEDS_USER_MAPPING` > `READY_WITH_FALLBACKS` > `READY_TO_EXECUTE`.

If the status is `NEEDS_USER_MAPPING`, ask at most three concise mapping questions. Prefer questions that unblock multiple work units at once.

When the user asks for implementation after planning, execute according to the plan while preserving ownership boundaries and avoiding overlapping writes.
