# Distillation Procedure

Input evidence, in priority order (higher wins on conflict):

1. Action log records (`event: prompt` / `event: action` lines).
2. Git observations: history between `source.base_commit` and the current head, plus the uncommitted working-tree diff. A working-tree confirmation is valid only at distillation time — when `changed_files` rest on it alone, say so in `notes`.
3. `agent-team` ledger, when the work ran under one (`agent-team event log --run <RUN_ID>`, task evidence/artifact fields): append-only and timestamped, but self-reported by executors — it ranks below observed evidence (log, git) and above unversioned notes.
4. `_workspace/<task>/` notes: `task.md` for intended units, `walkthrough.md` for decisions and errors, `implementation.md` for design rationale.
5. Session memory — usable for `objective` and `acceptance_criteria` wording, but any fact taken only from memory makes the step `confidence: unverified`.

Ledger caveats belong in the recipe: when the run has stale or non-terminal tasks at distillation time, record each as a vanish caveat in `notes` — unit id, last ledger event, and whether its scope's changes ended up committed.

## Pinning the Ground Truth

Before grouping, hash every log file that will be cited (`shasum -a 256 <path>`) and record the results in `source.log_files` as `{path, sha256}`. Hash the file as-is at distillation time; if the session is still appending, note that in `notes` — refs into a still-growing file are valid for the hashed prefix only.

When merging logs of the same session from multiple roots (project-local plus a fallback or legacy root), their basenames collide, and `log_refs` address files by basename. Copy the non-project file into `_workspace/<task>/` under a distinct name (e.g. `<session-id>.legacy.jsonl`), then hash and cite the copy. Copy — never move or rename the recorder's own files.

## Grouping Log Events Into Steps

- Each `prompt` record opens a candidate step; the `action` records until the next `prompt` belong to it.
- While grouping, keep each group's line range in its log file — this becomes the step's `log_refs`. A merged or split group carries the union of the ranges that support it; discontiguous ranges become multiple `log_refs` entries.
- Merge a group into the previous step when its prompt is a correction or continuation of the same objective ("fix the failing test", "continue", "also handle X in the same place") rather than a new goal.
- Split a group into multiple steps when it contains independent objectives with disjoint file sets.
- Drop groups that produced no recipe-relevant work: pure Q&A, exploration-only commands, aborted attempts fully superseded later. List dropped groups in one line each so the omission is visible, not silent.
- Abrupt-end postmortem: a log whose final group ends with neither a checkpoint commit nor a recorded validation run may mean the session died mid-work. Record a vanish caveat in `notes` — the last record's timestamp and whether the group's files ended up committed by distillation time. If the group's work is incomplete, drop it as above instead of distilling a half-done packet.

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

## Deriving the Provenance Receipt

| Field | Derive from |
| --- | --- |
| `changed_files` | Write/edit `action` records in the group, cross-checked against git history |
| `commands` | Command `action` records in the group, key ones only |
| `log_refs` | The line ranges kept during grouping, as `<log basename>#L<start>-L<end>` |
| `validation.command` | The last command in the group that checked the step's outcome, copied exactly as run — not normalized, not the packet's `verification` restated. When the check was an inline/ephemeral script, record the interpreter invocation and describe the script in angle brackets (e.g. `python3 - <<schema assertions over example.yaml>`); never present a cleaned-up one-liner as what ran |
| `validation.commit` | The checkpoint commit whose state that command ran against (usually the step's own commit); `null` when the run happened on uncommitted state, saying so in `result` |
| `validation.result` | The observed outcome of that run, from the log record; `"not verified in original session"` with `command`/`commit` null when nothing validated the step |
| `confidence` | `verified` only when every `changed_files` entry is confirmed by log or git **and** `log_refs` points at the confirming records; otherwise `unverified` |

## Mapping Checkpoints

- List commits between `base_commit` and head (`git log --oneline --name-only`), and assign each commit to the step whose files and time window it matches. Record them in `provenance.commits`.
- Commits that mix steps or belong to none: note them under the recipe-level `notes` rather than forcing an assignment.
- When the session created no commits, `replay.mode: exact` is unavailable — state this in the recipe.

## Honesty Rules

- Apply the field semantics in `recipe-format.md` when writing each step: `confidence` and `validation` are defined there, evidence-first.
- The recorder redacts common secret patterns, but redaction is keyword-based: re-scan `commands`, `prompt_excerpt`, and `validation.command` before saving, and replace any surviving secret with a placeholder plus a note naming the env var or key.
