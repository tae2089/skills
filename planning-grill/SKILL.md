---
name: planning-grill
description: Stress-test fuzzy intent into a code-aware, worker-ready plan or durable task.md Seed before execution. Use when scope, acceptance criteria, failure modes, data shapes, defaults, edge cases, or handoff boundaries are unclear, or when a durable Seed is requested. May precede decompose-and-dispatch when delegated or coordinated work is needed. Skip concrete plans with testable acceptance criteria and clear task boundaries.
---

# Planning Grill

The goal is not to debate indefinitely. The goal is to convert vague intent into
a concrete, code-aware plan with testable acceptance criteria that a worker can
complete with evidence. This skill sharpens the plan; it does not decompose it or
map executors.

Grill at two altitudes, and often both in one pass:

- **Plan-level** — outcome, scope, approach, acceptance criteria.
- **Detail-level** — pin the concrete implementation decisions that would
  otherwise be left to guesswork (see the Implementation detail dimension in
  `references/grill-patterns.md`). This is decision-fixing, not implementation.

## Modes And Boundaries

Choose one mode before probing:

- `LIGHTWEIGHT`: the user wants planning conversation only, with no durable
  tracking, execution, or follow-up. Keep decisions in the final inline summary.
- `DURABLE`: the user wants a persisted plan, execution, or follow-up. Create the
  repository's task state files; `_workspace/<task-name>/task.md` is the canonical
  Seed that the next worker consumes without the original conversation. Keep
  design-only detail in `implementation.md` and event history in `walkthrough.md`.

Do not create a second Seed that duplicates `task.md`.

This skill routes rather than absorbs. When a blocker is really a different kind
of sharpening, hand off and resume the grill after the peer result (use each
skill if available):

- terminology, naming, overloaded or missing terms → `domain-modeling`
- module boundaries, interface placement, structural shape → `codebase-design`
- branching logic, side effects, ordering constraints → `flow-design`

After `SHARPENED`, choose the next consumer by its own trigger:

- use `decompose-and-dispatch` only for delegated, parallel, multi-agent, or
  dependency/ownership-coordinated work
- do not use `execute-dispatch-unit` unless an actual dispatch packet exists
- otherwise return the contract for the requested next step; normal skill routing
  applies independently

No downstream skill is an escape from unresolved ambiguity.

## Workflow

1. Frame the plan: intended outcome, scope, and the system it affects.
2. Select lightweight or durable output. For durable work, read the Seed Contract
   in `references/grill-patterns.md`, create or update `task.md`, and preserve any
   task-file schema required by the repository.
3. Inspect existing code and docs before asking anything the repository can
   answer. When code or docs contradict the plan, surface the contradiction and
   ask which source should change.
4. Build a short decision checklist across the decision dimensions (see
   `references/grill-patterns.md`): goal, scope, vocabulary, constraints,
   dependencies, acceptance, implementation detail, failure modes, handoff.
5. Resolve unresolved decisions one at a time, most upstream first — follow
   the dimension order, so goal and scope are settled before details. If a
   decision blocks (see the block criteria in Question Discipline), emit one
   Probe Format block and wait; otherwise record it as an explicit Assumption or
   Risk and proceed with the recommended assumption.
6. Record each resolved decision immediately in the matching Seed field when
   `task.md` exists; otherwise use the inline Decision Log Pattern.
7. Convert stable decisions into observable behavior scenarios, ordered
   acceptance or validation items, and bounded implementation boundaries. Do
   this only after the decisions those items depend on are stable; do not create
   dispatch packets or executor mappings.
8. Run the completion checks and the Durable Seed Gate when applicable. When the
   Seed is writable, keep it current for every terminal result; do not mark it
   `SHARPENED` until the gate passes.
9. Select the next consumer by its own trigger, then emit the Handoff Envelope.

## Planning Checks

Before asking the user, search for:

- context docs: `AGENTS.md`, `CLAUDE.md`, `README`, `docs/`, `adr/`, `architecture/`
- domain vocabulary in code: package, type, and command names; config keys; API
  routes; schema names
- existing contracts: skills, agent definitions, conventions, acceptance
  criteria, test fixtures

Do not ask the user to answer what local files, command output, or existing
artifacts already answer.

## Question Discipline

Ask at most one blocking question per turn. Compound questions are forbidden.
Deliver every blocking question as a single Probe Format block — four labeled
lines, plus an optional `Options` list:

```md
Current understanding: <one-sentence summary of the plan and what is decided>
Blocked decision: <the unresolved decision + why it matters, one line>
Recommended answer: <your recommendation (if wrong: <consequence>)>
Question: <one concrete question, no compound clauses>
Options: <optional — see rules>
- <option A>
- <option B>
- (free-form answer)
```

Rules:

- `Recommended answer` is required and must inline the consequence of being
  wrong, so the requester sees the cost without a follow-up. This is a judgment,
  not a menu of equal options.
- Attach `Options` only when the requester would struggle to answer from a
  blank, or when contrasting options surface their implicit judgment criteria —
  never when they would narrow the requester's thinking to multiple choice. Use
  2-3 options, list the recommended option first, and end with
  `- (free-form answer)`. If four or more options seem necessary, split the
  decision into smaller probes instead.
- After each answer, restate `Current understanding` in a one-line
  acknowledgment before the next probe.
- Block only when the answer changes scope, owner, task ordering, an artifact
  contract, acceptance criteria, or a safety boundary, and the decision is one
  the requester must own. When a defensible assumption exists, prefer
  recommending it and recording the risk over blocking — touching scope or
  acceptance is not by itself a reason to block on a plan where little is
  decided yet. Otherwise record the uncertainty as an explicit assumption or
  risk with its consequence and verification path, then continue.

The `Options` rules are adapted from the `deep-interview` skill in
`devbrother2024/skills` at commit
`de4998a1ad579d3d8654faf66a9e9a9ae09af894`.

## Acceptance Criteria

Good acceptance criteria are testable by a worker or reviewer, tied to behavior,
artifact content, or command output, scoped to one task or phase, and explicit
about what does not count as complete. Avoid criteria that only say the result
should be "clean", "robust", "done", or "better".

## Durable Seed Gate

A durable Seed is ready only when all of these checks pass:

- another worker can identify the outcome, scope, non-goals, affected system,
  and dependencies without the original conversation
- every behaviorally material normal, boundary, and failure case maps to an
  observable acceptance or validation item
- constraints, invariants, data shapes, defaults, and error semantics whose
  wrong guess is costly are fixed; genuine free choices are `Worker Latitude`
- repository evidence and user decisions are distinguishable from assumptions,
  and contradictions are resolved or explicitly blocking
- no open question can change behavior, scope, an artifact contract, acceptance,
  task ordering, or a safety boundary

Do not replace these checks with an LLM-assigned clarity or ambiguity score. A
score may orient further questioning, but it is not evidence that the Seed is
worker-ready.

## ADR Boundary

Suggest recording a decision as an ADR (via the `domain-modeling` skill) only
when all are true: changing it later would be meaningfully expensive; future
maintainers could not infer it from code alone; and it chose between real
alternatives. Otherwise keep the decision in the task state files.

## Reference Files

Load when you reach that step; do not load up front.

- `references/grill-patterns.md` — the decision dimensions in detail, worked
  Probe Format examples, the durable Seed contract, the decision-log format, and
  stop conditions.

## Completion

The grill is complete when:

- domain terms the plan relies on are precise
- major dependencies and task boundaries are explicit
- code and docs have been checked for contradictions
- acceptance criteria are testable
- implementation-detail decisions whose wrong guess is costly are pinned, or
  explicitly marked as worker latitude — not parked under risks
- every remaining assumption or risk is explicitly non-blocking, has a
  consequence and verification path, and does not meet the block criteria
- when durable mode is active, `task.md` satisfies the Durable Seed Gate and
  contains the ordered acceptance or validation items the next worker will use

Do not start decomposition or execution just because the plan sounds plausible.
Hand off only after acceptance criteria and task boundaries are concrete enough
for a worker to complete with evidence.

## Handoff Envelope

End with the resolved decisions and remaining non-blocking assumptions or risks,
not a replay of the dialogue, followed by this envelope:

```text
Artifact: inline-only | _workspace/<task-name>/task.md | unavailable (<intended path>)
Status: SHARPENED | BLOCKED_ON_USER | ROUTED | BLOCKED
Next: <requested direct step, triggered downstream skill, pending probe, or blocker>
```

Use the statuses as follows:

- `SHARPENED`: acceptance criteria and task boundaries are concrete and, in
  durable mode, the Durable Seed Gate passes; `Next` follows the triggered next
  step rather than defaulting to decomposition.
- `BLOCKED_ON_USER`: a blocking decision is unanswered; a Probe is pending and no
  handoff happens until it is resolved.
- `ROUTED`: the dominant blocker belongs to a peer sharpening skill (name it:
  `domain-modeling`, `codebase-design`, or `flow-design` — never
  `decompose-and-dispatch`) and was handed off; the plan returns to the grill
  afterward.
- `BLOCKED`: required repository evidence, access, permission, or durable
  artifact creation failed and no safe planning fallback satisfies the request.
