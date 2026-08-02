# Backend: local

There is no issue tracker. A `task.md` Plan line **is** the issue.

Do not create separate files per unit. A subagent reads the Contract in
`task.md` and its own Plan line — that is the whole issue. The Plan line's
`scope:` and `verify:` are already what `implementation.md` boiled down to; the
subagent does not go read the original.

## Shape

Fill the Plan section `to-spec` left empty:

```markdown
## Plan
- [ ] Todo — 01 설정 파일 파싱
      scope: internal/config/**
      covers: TC-1, TC-3
      verify: `go test ./internal/config/...` — 전부 통과
      needs: —
- [ ] Todo — 02 시작 시점에 파서 연결
      scope: cmd/server/main.go
      covers: TC-1
      verify: `go test ./cmd/server/...` — 전부 통과
      needs: 01
```

Number units `01`, `02`, … so a subagent can be pointed at one by number.

`covers:` cites the spec's `## Test Cases` numbers. Every `TC-n` in the spec must
appear in at least one unit's `covers:`. Grep it before you finish:
`grep -o 'TC-[0-9]*' task.md | sort -u`.

`needs:` lists the numbers that must finish first, or `—` for none. Units with
`needs: —` can run at the same time.

## Statuses

`Todo` → `In Progress` → `Done`. Only the subagent working a unit changes its
status, and only after that unit's `verify` command passes.

## Amending

Edit the Plan line in place and append one line to `walkthrough.md`:

```
[16:20] decision: split unit 02 — startup wiring and flag parsing are separate reviews
```

Never delete a unit that turned out wrong. Set it back to `Todo` with a corrected
description, so the history stays readable.
