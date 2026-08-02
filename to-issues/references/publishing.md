# Publishing work units to a tracker

Only when `to-spec` published the spec. The `task.md` Plan is written either way,
and it stays the local index.

Creating issues is visible to the team and awkward to undo. The user already
approved the breakdown in Step 3; confirm the write itself — count, titles, parent —
before the first one.

## Shape

One child per unit, under the spec's issue:

```
#11  the spec — problem, solution, user stories, out of scope
 ├─ #12  01 parse the config file
 ├─ #13  02 wire the parser into startup
 └─ #14  03 document the config keys
```

Children carry no label. The parent/child link already says what they are.

## GitHub

For each unit, in dependency order, so later units can reference real numbers:

```
gh issue create --title "01 parse the config file" --body "$(cat <<'EOF'
Parent: #11

**Covers**: US-1, US-3
**Verify**: `go test ./internal/config/...` — 전부 통과
**Depends on**: none
EOF
)"
```

Then link each as a native sub-issue of the parent. The `Parent: #11` line is the
only link a unit needs — the spec is not copied down.

`Depends on` uses issue numbers once they exist: `Depends on: #12`.

## Jira, Linear, Notion, anything else

Push through whatever MCP server is connected. Same four fields, same dependency
order, the tracker's own native parent/child link where it has one.

## Back in `task.md`

Add the reference to each Plan line. Nothing else changes:

```markdown
## Plan
- [ ] Todo — 01 parse the config file (#12)
      covers: US-1, US-3
      verify: `go test ./internal/config/...` — 전부 통과
      needs: —
```

## Closing

A finished unit closes its issue and flips its Plan line to `Done`. Closing every
child does **not** close the parent — the parent shows progress, and how it gets
closed is the team's own configuration.
