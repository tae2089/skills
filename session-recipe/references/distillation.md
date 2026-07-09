# Distillation Procedure

Input evidence, in priority order (higher wins on conflict):

1. Action log records (`event: prompt` / `event: action` lines).
2. Git history between `source.base_commit` and the current head.
3. `_workspace/<task>/` notes: `task.md` for intended units, `walkthrough.md` for decisions and errors, `implementation.md` for design rationale.
4. Session memory — usable for `objective` and `acceptance_criteria` wording, but any fact taken only from memory makes the step `confidence: unverified`.

## Grouping Log Events Into Steps

- Each `prompt` record opens a candidate step; the `action` records until the next `prompt` belong to it.
- Merge a group into the previous step when its prompt is a correction or continuation of the same objective ("fix the failing test", "continue", "also handle X in the same place") rather than a new goal.
- Split a group into multiple steps when it contains independent objectives with disjoint file sets.
- Drop groups that produced no recipe-relevant work: pure Q&A, exploration-only commands, aborted attempts fully superseded later. List dropped groups in one line each so the omission is visible, not silent.

## Deriving Packet Fields

| Field | Derive from |
| --- | --- |
| `objective` | The group's prompt plus what the diff actually did — not memory alone |
| `capability` | Dominant action type: edits → `implementer`, ran commands to check → `tester`, read-and-judged only → `reviewer`, docs/changelogs/specs → `documenter`, external systems → `operator`; anything else uses the capability classes in the `decompose-and-dispatch` skill |
| `allowed_scope` | Observed `changed_files`, generalized into the tightest patterns that cover them |
| `forbidden_scope` / `non_goals` | Boundaries the original session respected or the user stated ("don't touch the UI") |
| `dependencies` | Earlier step ids whose outputs this step consumed |
| `acceptance_criteria` | What the original verification actually asserted, restated as observable outcomes |
| `verification` | The narrowest command(s) that actually verified the step, and that can run again at replay time |

## Mapping Checkpoints

- List commits between `base_commit` and head (`git log --oneline --name-only`), and assign each commit to the step whose files and time window it matches. Record them in `provenance.commits`.
- Commits that mix steps or belong to none: note them under the recipe-level `notes` rather than forcing an assignment.
- When the session created no commits, `replay.mode: exact` is unavailable — state this in the recipe.

## Honesty Rules

- Apply the field semantics in `recipe-format.md` when writing each step: `confidence` and `verification_evidence` are defined there, evidence-first.
- The recorder redacts common secret patterns, but redaction is keyword-based: re-scan `commands` and `prompt_excerpt` before saving, and replace any surviving secret with a placeholder plus a note naming the env var or key.
