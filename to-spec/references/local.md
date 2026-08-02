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

## Test Cases
1. 실제 입력 → 실제 기대 출력
2. 실패 케이스 최소 하나

## Plan
- (filled by to-issues)

## Verification
- [ ] Todo — 고치기 전 TC-1 테스트가 실패하는 것 확인 (출력 남길 것)
- [ ] Todo — 프로젝트 전체 명령과 기대 결과
- [ ] Todo — TC-1을 실제로 한 번 실행

## Result
- (filled at completion)
```

Section rules are in `SKILL.md`, Step 2 — they are the same on every backend. Two
things are local-only:

- Drop the Non-Goals heading when nothing plausible is out of scope. Never drop
  Test Cases; if you cannot write one, the contract is not concrete enough yet.
- Nothing runs the Verification commands for you. The unchecked boxes are the
  reminder.

## `implementation.md`

Design approach, key assumptions, affected modules/files, risks and edge cases,
and approaches considered and dropped with the reason. Max 12 bullets unless
safety or contract completeness needs more.

Never restate the contract, the plan, or a code walkthrough. Only information
needed to implement.

## `walkthrough.md`

Format and content rules are in `SKILL.md`, Step 2. A filled example:

```
[14:32] decision: 낙관적 잠금 선택 — 쓰기 경합이 낮아 행 잠금은 과함
[14:51] error: `pytest tests/test_sync.py` 실패 — fixture가 닫힌 세션을 재사용
[15:10] verification: 전체 스위트 통과, 214 passed
```

## Promoting to a shared backend

If teammates start needing this task's state, write `github` into
`_workspace/<task-name>/.tracker` — the per-task file, not the repo-wide one.
Other tasks in this repo keep their own backend.

Then move the contract and the implementation notes into that backend and reduce
`task.md` to a link plus the plan. Do not keep both full copies. `walkthrough.md`
stays local either way.

## Pushing to a tracker with no backend here — Jira, Linear, Notion

No reference file, and `.tracker` stays `local`. When the user asks, push through
whatever MCP server is connected: a one-line problem statement, then Contract,
Non-Goals, Test Cases, Verification. A teammate opens the ticket cold and needs the
reason as well as the contract.

Then replace those four sections in `task.md` with the ticket link — the ticket is
canonical from there. Implementation notes stay in `implementation.md` unless the
user wants a design page. `walkthrough.md` never goes.
