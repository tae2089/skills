# Parallelism And Conflict Rules

Run units at the same time only when they are independent enough that
coordinating them costs less than the time saved.

Good parallel candidates:

- Read-only research over different modules or questions.
- Review passes with different concerns — security, correctness, tests.
- Test or reproduction work that can run while implementation proceeds.
- Implementation work with file scopes that do not overlap.

Do not parallelize when:

- Two units write the same files, generated artifacts, schema, lockfiles, or
  shared interfaces.
- One unit needs a decision from another before it can start.
- The work needs one coherent design choice across both units.
- The runtime is short on agent slots, budget, approvals, or access to an
  external system.

State each group explicitly before dispatching:

```yaml
parallel_groups:
  - id: P1
    units: [01, 02, 03]
    reason: "read-only discovery, no shared write scope"
  - id: P2
    units: [05, 06]
    reason: "independent verification after 04 lands"
```

## When not to delegate a unit at all

Keep a unit on the main agent when:

- its `allowed_scope` overlaps a unit already running
- the change needs one coherent edit across files another unit owns
- another agent is already doing that work
- the unit's verification command is missing — report the gap and stop instead

Running everything on the main agent in dependency order is a valid plan. Say so
plainly rather than reporting it as a failure to delegate.
