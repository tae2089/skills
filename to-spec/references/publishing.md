# Publishing the spec to a tracker

The three `_workspace/` files are written first, always. Publishing copies the
`task.md` sections to a tracker so teammates can read them, and leaves a link
behind.

Publishing is visible to the team and awkward to undo. Say what you are about to
create and get the user's confirmation before the first write.

## What goes up

Problem Statement, Solution, User Stories, Out of Scope — the `task.md` sections, in
that order. Someone opens the ticket cold and needs the reason as well as the
behavior.

**Verification stays local.** It is a checklist someone ticks off, and unchecked
boxes are the only signal that the work is not finished — they belong where the work
happens, not on a ticket nobody re-opens. The child issues carry the per-unit verify
commands, so the ticket is not left without one.

`implementation.md` stays local unless the user wants a design page for it.
`walkthrough.md` never goes.

## Then shrink the local copy

Replace those four sections in `task.md` with the link. The ticket is canonical from
there; two full copies drift. Keep Verification, Plan, and Result local.

```markdown
# <task-name>

Spec: #11

## Verification
- [ ] Todo — 고치기 전 US-1의 검사가 실패하는 것 확인 (출력 남길 것)
- [ ] Todo — 프로젝트 전체 명령과 기대 결과
- [ ] Todo — 실물을 손으로 한 번

## Plan
- (filled by to-issues)

## Result
- (filled at completion)
```

## GitHub

Use `gh`. One issue, labeled `type:prd`:

```
gh issue create --label type:prd --title "<task-name>" --body-file <(...)
```

Confirm the label exists first — `gh label list --search type:` — and create it with
`gh label create` if it does not. If the org has native **Issue Types** configured,
use those instead of a `type:*` label.

`to-issues` creates one native sub-issue per work unit under this one. Hand it the
issue number.

## Jira, Linear, Notion, anything else

Push through whatever MCP server is connected. Same sections, same order, same
shrink afterwards. There is no per-tracker procedure here — the tracker's own MCP
tools describe themselves.

## Starting from a ticket that already exists

Read it, write `_workspace/<task-name>/task.md` with its reference and the Plan and
Result sections, and put the implementation and testing decisions in
`implementation.md`. Do not restate the ticket's body locally.
