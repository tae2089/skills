# Backend: local

Everything lives in `_workspace/<task-name>/` (kebab-case). Nothing is published.

## Fast tier — one file

`task.md`, contract only. `to-issues` fills the Plan section later.

```markdown
# <task-name>

## Contract
- expected behavior / acceptance criteria

## Plan
- (filled by to-issues)

## Result
- (filled at completion)
```

Max 5 bullets in Contract.

## Full tier — three files

### `task.md`

Same shape as Fast tier, plus a Verification section:

```markdown
# <task-name>

## Contract
- expected behavior / acceptance criteria

## Plan
- (filled by to-issues)

## Verification
- [ ] Todo — command and expected result

## Result
- (filled at completion)
```

Max 5 bullets per section.

### `implementation.md`

Design approach, key assumptions, affected modules/files, risks and edge cases.
Max 12 bullets unless safety or contract completeness needs more.

Never restate the contract, the plan, or a code walkthrough. Only information
needed to implement.

### `walkthrough.md`

Append-only. One line per event:

```
[14:32] decision: chose optimistic locking over row lock — write contention is low
[14:51] error: `pytest tests/test_sync.py` failed — fixture reused a closed session
[15:10] verification: full suite green, 214 passed
```

Only design decisions, failed verifications with cause, scope changes, and the
final verification result. Read only the tail (~20 lines).

## Promoting to a shared backend

If teammates start needing this task's state, switch `_workspace/.tracker` to
`jira` or `github`, move the contract and design into that backend, and reduce
`task.md` to a link plus the plan. Do not keep both full copies.
