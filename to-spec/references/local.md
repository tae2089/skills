# Backend: local

Everything lives in `_workspace/<task-name>/` (kebab-case). Nothing is published.
Three files, always.

## `task.md`

`to-issues` fills the Plan section later.

```markdown
# <task-name>

## Contract
- 기대 동작 / 수용 기준

## Non-Goals
- 범위 안이라고 오해할 만하지만 아닌 것

## Plan
- (filled by to-issues)

## Verification
- [ ] Todo — 전체 실행 명령과 기대 결과

## Result
- (filled at completion)
```

Max 5 bullets in Contract, 3 in Non-Goals. Drop the Non-Goals heading entirely
when nothing plausible is out of scope — an empty section reads as "no bounds".

The Verification command covers the whole project. A unit's `verify:` covers a
part. Never point this line at a unit — if it can be satisfied by one unit's
command, it is not checking the whole task.

Nothing runs this command for you. The unchecked box is the reminder.

## `implementation.md`

Design approach, key assumptions, affected modules/files, risks and edge cases,
and approaches considered and dropped with the reason. Max 12 bullets unless
safety or contract completeness needs more.

Never restate the contract, the plan, or a code walkthrough. Only information
needed to implement.

A dropped approach is an implementation note, not a non-goal. Non-goals say what
is out of scope; this says why the chosen route beat the one next to it.

## `walkthrough.md`

Append-only. One line per event:

```
[14:32] decision: 낙관적 잠금 선택 — 쓰기 경합이 낮아 행 잠금은 과함
[14:51] error: `pytest tests/test_sync.py` 실패 — fixture가 닫힌 세션을 재사용
[15:10] verification: 전체 스위트 통과, 214 passed
```

Only failed verifications with cause, scope changes, and the final verification
result. Decisions made before the work started belong in `implementation.md`.
Read only the tail (~20 lines).

## Promoting to a shared backend

If teammates start needing this task's state, write `jira` or `github` into
`_workspace/<task-name>/.tracker` — the per-task file, not the repo-wide one.
Other tasks in this repo keep their own backend.

Then move the contract and the implementation notes into that backend and reduce
`task.md` to a link plus the plan. Do not keep both full copies. `walkthrough.md`
stays local either way.
