---
name: decompose-and-dispatch
description: Break a complex goal into atomic work units and map each to the best available runtime executor, with dependencies, parallelism, and an execution-ready dispatch plan. Use when planning multi-step work, coordinating multiple agents or workers, adapting a plan across coding-agent runtimes, or deciding which agent or tool owns each task.
---

# Decompose And Dispatch

Use this skill to turn a goal into the smallest practical work units and map those units to whichever executors are actually available in the current runtime.

The skill is runtime-neutral. Do not assume agent names are standardized. Agent names are local aliases, not portable semantics.

## Core Loop

Follow this sequence:

1. Restate the user goal and success criteria.
2. Build an execution capability inventory for the current runtime.
3. Decompose the goal into atomic work units.
4. Classify each unit by required capability.
5. Map each unit to the best available executor.
6. Apply the work unit quality gate.
7. Mark dependencies, parallelism, ownership, risks, and verification.
8. Produce a dispatch plan with handoff prompts when delegation is possible.
9. Only delegate or spawn work when the runtime supports it and the user has allowed delegation, subagents, workers, or parallel execution.

## Capability Inventory

Before assigning work, identify what execution capabilities are available. Use runtime-provided metadata, visible tools, local agent files, user-provided mappings, or other environment-specific configuration.

Use these portable capability classes:

| Capability | Use For |
| --- | --- |
| `orchestrator` | Plan control, sequencing, decisions, conflict resolution, integration, final synthesis |
| `researcher` | Read-only code search, documentation research, source discovery, context gathering |
| `implementer` | Code edits, refactors, artifact creation, migrations, fixes |
| `tester` | Reproduction, command execution, test runs, verification evidence |
| `reviewer` | Correctness review, risk review, regression checks, missing-test analysis |
| `specialist` | Domain-specific reasoning such as security, frontend, data, platform, product, design, or framework expertise |
| `operator` | Browser, app, cloud, MCP, connector, CLI, deployment, or external-system operation |
| `documenter` | Specs, plans, changelogs, handoff notes, runbooks, user-facing docs |

If the runtime has named agents, map each capability to the closest available named executor. If no delegation mechanism exists, assign the capability to the main agent and mark delegation as unavailable.

While building the inventory, also check whether the `agent-team` CLI is runnable — it enables the durable ledger below.

## Durable Ledger (optional, requires the `agent-team` CLI)

When the `agent-team` CLI is available and delegation is allowed, register the dispatch plan in its out-of-process ledger so completion claims are gated and executor death leaves evidence:

- Create one run for the plan (`agent-team run create`) and one task per work unit (`agent-team task create`, with the unit's packet as the task contract). Record the run id and each task id in the dispatch plan.
- Every handoff prompt must carry the unit's ledger coordinates: `RUN_ID`, `TASK_ID`, `AGENT`, the artifact root `_workspace/RUN_ID/`, and the orchestrator's recipient name for messages. Executors mirror their lifecycle per the `execute-dispatch-unit` skill's ledger rules.
- The orchestrator monitors with `run status`/`task list`, and detects abandoned units with `task stale --older-than <duration>`. Before reassigning or retrying a stale unit, record vanish evidence: the unit id, its last ledger event, and the current git state of its `allowed_scope` classified as clean, dirty, or unknown.
- Close the run (`run close`) only after every task is terminal; the ledger rejects completion without evidence and an artifact path — treat a rejection as a real gap, not an obstacle to force past.

Command details live with the CLI's own bundled skills and `--help`; they take precedence over the summaries here. When the CLI is absent, proceed exactly as before and note in the dispatch plan that no ledger is available (no completion gating, no stale detection).

## Reference Files

Load the relevant file when you reach that step. Do not load all of them up front.

- `reference/matching.md` — Runtime discovery checklist, evidence-ordered executor matching, confidence levels, runtime adapter notes, and host adapter config (`agents/openai.yaml` = Codex app UI metadata).
- `reference/work-units.md` — Atomic work unit criteria, the quality gate, and the full work-unit YAML schema.
- `reference/dispatch-format.md` — Dispatch plan tables, capability mapping table, and the handoff prompt contract.
- `reference/parallelism-and-delegation.md` — Parallel grouping rules, conflict avoidance, and when to delegate vs keep on the main agent.
- `reference/example.md` — Full end-to-end worked example of the Core Loop, from goal to dispatch plan and status.

## Output Contract

End with one of these statuses:

- `READY_TO_EXECUTE`: The plan has clear units, mappings, dependencies, and verification.
- `READY_WITH_FALLBACKS`: Some mappings fall back to the main agent, but execution can proceed.
- `NEEDS_USER_MAPPING`: Executor mapping is ambiguous enough that user confirmation is needed before delegation.
- `BLOCKED`: Required context, permissions, or runtime capability is missing and no safe fallback exists.

If the status is `NEEDS_USER_MAPPING`, ask at most three concise mapping questions. Prefer questions that unblock multiple work units at once.

When the user asks for implementation after planning, execute according to the plan while preserving ownership boundaries and avoiding overlapping writes.
