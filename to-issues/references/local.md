# Backend: local

There is no issue tracker. A `task.md` Plan line **is** the issue.

Do not create separate files per unit. A subagent reads the Contract in
`task.md` and its own Plan line — that is the whole issue. The Plan line's
`scope:`, `accept:`, and `verify:` are already what `implementation.md` boiled
down to; the subagent does not go read the original.

## Shape

Fill the Plan section `to-spec` left empty:

```markdown
## Plan
- [ ] Todo — 01 parse the config file
      scope: internal/config/**
      accept: malformed YAML returns a typed error, never panics
      verify: `go test ./internal/config/...` — all pass
      needs: —
- [ ] Todo — 02 wire the parser into startup
      scope: cmd/server/main.go
      accept: server exits 1 with the parse error on bad config
      verify: `go test ./cmd/server/...` — all pass
      needs: 01
```

Number units `01`, `02`, … so a subagent can be pointed at one by number.

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
