# Parallelism And Conflict Rules

Each parallel subagent gets its own git worktree. Two units writing the same file
produce two branches that conflict at merge, not a race. Two units likely to touch
the same code is not a reason to serialize them.

Good parallel candidates:

- Read-only research over different modules or questions.
- Review passes with different concerns — security, correctness, tests.
- Test or reproduction work that can run while implementation proceeds.
- Implementation work on separate modules.

Do not parallelize when:

- One unit needs a decision from another before it can start.
- The work needs one coherent design choice across both units.
- The units share state a worktree does not copy — the same database, the same
  port, the same external service. A worktree copies the repo, not the world.
- The runtime cannot give each subagent a worktree. Run in sequence instead.
- The runtime is short on agent slots, budget, approvals, or access.

State each group explicitly before dispatching:

```yaml
parallel_groups:
  - id: P1
    units: [01, 02, 03]
    reason: "read-only discovery"
  - id: P2
    units: [05, 06]
    reason: "independent verification after 04 lands"
```

## The break a worktree hides

Two units can each pass alone and break together with no file in common. One
renames a symbol in `config`; the other adds a call to the old name in `server`.
Both worktrees are green and neither ever sees the other. Isolation makes a unit's
green light weaker evidence, not stronger.

Only the project's whole verification command, run once on the merged tree, catches
it. Say that in the report every time parallel units land.

## When not to delegate a unit at all

Keep a unit on the main agent when:

- the change needs one coherent edit that another unit is also making
- another agent is already doing that work

Running everything on the main agent in dependency order is a valid plan. Say so
plainly rather than reporting it as a failure to delegate.
