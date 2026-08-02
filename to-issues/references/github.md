# Backend: github

One native sub-issue per work unit, under the `type:prd` issue `to-spec` created.

```
[type:prd]   #11  problem, contract, acceptance criteria
             ├─ #12  01 parse the config file
             ├─ #13  02 wire the parser into startup
             └─ #14  03 document the config keys
```

Sub-issues carry no label — the native parent/child link already says what they
are.

## Prerequisites

Use `gh` for everything. You need the PRD issue number from `to-spec`.

## Creating

List the titles and the parent number, and get the user's confirmation before the
first `gh issue create`. Creating issues notifies watchers.

For each unit, in dependency order:

```
gh issue create --title "01 parse the config file" --body "$(cat <<'EOF'
Parent: #11

**Scope**: internal/config/**
**Accept**: malformed YAML returns a typed error, never panics
**Verify**: `go test ./internal/config/...` — all pass
**Depends on**: none
EOF
)"
```

Then link each one as a native sub-issue of the PRD. Do not copy the PRD's
contract into the body — the `Parent: #11` line is the link.

`Depends on` uses issue numbers once they exist: `Depends on: #12`.

## Local pointer

Fill the Plan section in `task.md` with numbers only:

```markdown
## Plan
- [ ] Todo — 01 parse the config file (#12)
- [ ] Todo — 02 wire the parser into startup (#13) — needs #12
```

Do not copy sub-issue bodies into `task.md`.

## Closing

- Unit finished → close its sub-issue, update the `task.md` line to `Done`.
- Closing every sub-issue does **not** auto-close the PRD. The parent only shows
  progress; how it gets closed is the team's own configuration.
