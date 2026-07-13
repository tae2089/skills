---
name: planning-grill
description: Stress-test a fuzzy plan into a concrete, code-aware one before decomposition or execution. Use to sharpen scope and acceptance criteria, surface failure modes, pin the concrete implementation details a worker would otherwise guess (data shapes, defaults, edge cases, formats), or turn vague intent into worker-ready task contracts. Runs upstream of decompose-and-dispatch. Skip when the plan is already concrete with testable acceptance criteria and clear task boundaries.
---

# Planning Grill

The goal is not to debate indefinitely. The goal is to convert vague intent into
a concrete, code-aware plan with testable acceptance criteria that a worker can
complete with evidence. This skill sharpens the plan; it does not decompose it or
map executors — hand a sharpened plan to the `decompose-and-dispatch` skill (if
available) for that.

Grill at two altitudes, and often both in one pass:

- **Plan-level** — outcome, scope, approach, acceptance criteria.
- **Detail-level** — pin the concrete implementation decisions that would
  otherwise be left to guesswork (see the Implementation detail dimension in
  `references/grill-patterns.md`). This is decision-fixing, not implementation —
  the worker executes the fixed contract via the `execute-dispatch-unit` skill
  (if available).

## Boundary

For a lightweight planning conversation, run this skill without creating state
files. Create task state files (`task.md`, `implementation.md`, `walkthrough.md`
under `_workspace/<task-name>/`) once the user wants durable tracking, execution,
or follow-up.

This skill routes rather than absorbs. When a blocker is really a different kind
of work, hand off (use each skill if available):

- terminology, naming, overloaded or missing terms → `domain-modeling`
- module boundaries, interface placement, structural shape → `codebase-design`
- branching logic, side effects, ordering constraints → `flow-design`
- correctness, regression risk, or missing verification once the plan is stable → `ready-code-review` or the project's review path

Decomposition is not a routing target: `decompose-and-dispatch` is reachable
only through the `SHARPENED` handoff, never as an escape from sharpening.

## Workflow

1. Frame the plan: intended outcome, scope, and the system it affects.
2. Inspect existing code and docs before asking anything the repository can
   answer. When code or docs contradict the plan, surface the contradiction and
   ask which source should change.
3. Build a short decision checklist across the decision dimensions (see
   `references/grill-patterns.md`): goal, scope, vocabulary, constraints,
   dependencies, acceptance, implementation detail, failure modes, handoff.
4. Resolve unresolved decisions one at a time, most upstream first — follow
   the dimension order, so goal and scope are settled before details. If a
   decision blocks (see the block criteria in Question Discipline), emit one
   Probe Format block and wait; otherwise record it as an Open Question or
   Risk and proceed with the recommended assumption.
5. Record each resolved decision immediately in the task state files when they
   exist.
6. Convert stable decisions into acceptance criteria and task boundaries only
   after the relevant ambiguity is resolved.
7. End with a handoff status (see Handoff Status).

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
  decided yet. Otherwise record the uncertainty under Open Questions or Risks
  and continue.

The `Options` rules are adapted from the `deep-interview` skill in
`devbrother2024/skills` at commit
`de4998a1ad579d3d8654faf66a9e9a9ae09af894`.

## Acceptance Criteria

Good acceptance criteria are testable by a worker or reviewer, tied to behavior,
artifact content, or command output, scoped to one task or phase, and explicit
about what does not count as complete. Avoid criteria that only say the result
should be "clean", "robust", "done", or "better".

## ADR Boundary

Suggest recording a decision as an ADR (via the `domain-modeling` skill) only
when all are true: changing it later would be meaningfully expensive; future
maintainers could not infer it from code alone; and it chose between real
alternatives. Otherwise keep the decision in the task state files.

## Reference Files

Load when you reach that step; do not load up front.

- `references/grill-patterns.md` — the decision dimensions in detail, worked
  Probe Format examples, the decision-log format, and stop conditions.

## Completion

The grill is complete when:

- domain terms the plan relies on are precise
- major dependencies and task boundaries are explicit
- code and docs have been checked for contradictions
- acceptance criteria are testable
- implementation-detail decisions whose wrong guess is costly are pinned, or
  explicitly marked as worker latitude — not parked under risks
- unresolved questions are answered, recorded as risks, or turned into blocked
  work

Do not start decomposition or execution just because the plan sounds plausible.
Hand off only after acceptance criteria and task boundaries are concrete enough
for a worker to complete with evidence.

## Handoff Status

End the grill with a summary of resolved decisions and remaining open
questions or risks — not a replay of the dialogue — plus one status so the
handoff is explicit:

- `SHARPENED`: acceptance criteria and task boundaries are concrete; hand off to
  `decompose-and-dispatch`.
- `BLOCKED_ON_USER`: a blocking decision is unanswered; a Probe is pending and no
  handoff happens until it is resolved.
- `ROUTED`: the dominant blocker belongs to a peer sharpening skill (name it:
  `domain-modeling`, `codebase-design`, or `flow-design` — never
  `decompose-and-dispatch`) and was handed off; the plan returns to the grill
  afterward.
