# Parallelism, Conflict, And Delegation Rules

## Parallelism And Conflict Rules

Parallelize only when work units are independent enough to avoid coordination cost.

Good parallel candidates:

- Read-only research over different modules or questions.
- Review passes with different concerns such as security, correctness, and tests.
- Test or reproduction work that can run while implementation proceeds.
- Implementation work with disjoint file or ownership scopes.

Avoid parallelism when:

- Two units edit the same files, generated artifacts, schema, lockfiles, or shared interfaces.
- One unit needs decisions from another unit before it can start.
- The work requires a single coherent design choice.
- The runtime has limited agent threads, budget, approvals, or external-system access.

For each parallel group, state the grouping:

```yaml
parallel_groups:
  - id: P1
    units: [W1, W2, W3]
    reason: "read-only discovery tasks with no shared write scope"
  - id: P2
    units: [W5, W6]
    reason: "independent verification after W4 completes"
```

## Delegation Rules

Delegation is optional and runtime-dependent.

Only delegate when all are true:

- The user explicitly asked for delegation, subagents, workers, parallel execution, or an execution plan that assigns work.
- The runtime exposes a delegation mechanism.
- The work unit is concrete, self-contained, and materially advances the goal.
- The executor's write scope is clear, or the task is read-only.
- The handoff prompt is self-contained.

Do not delegate when:

- The runtime has no visible delegation mechanism.
- The mapping confidence is low and the work is write-heavy or externally visible.
- The task requires a single coherent edit across overlapping files.
- Delegation would duplicate work already being done.
- The work unit fails the quality gate.

When delegation is not available, keep the executor as `main-agent` and still preserve the capability classification.
