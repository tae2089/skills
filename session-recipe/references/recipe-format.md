# Recipe Format

A recipe is one YAML document with three top-level keys: `recipe`, `steps`, `replay`.

The evidence model: packet fields are instructions for the future; `provenance` is a receipt about the past. Every claim in a receipt must point at evidence that can be re-checked mechanically (a log line range, a commit, an exact command), and every piece of evidence is valid only for the state it was captured against.

## `recipe` — metadata

| Field | Meaning |
| --- | --- |
| `name` | Kebab-case task name; matches the `_workspace/<task-name>/` folder when one exists |
| `created` | ISO timestamp of distillation |
| `source.session_ids` | Session ids the recipe was distilled from |
| `source.log_files` | Action logs used as ground truth: a list of `{path, sha256}` objects (empty if none existed). `sha256` is the file hash at distillation time; it pins the log so `log_refs` line ranges stay meaningful and later tampering or regeneration is detectable. Basenames must be unique across entries — `log_refs` address files by basename (disambiguation procedure in `distillation.md`) |
| `source.repo` | Origin URL, or absolute path when there is no remote |
| `source.base_commit` | Git head at the first recorded prompt; replay preconditions check against this |
| `environment` | Runtime requirements replay needs (toolchain versions, cluster context, env var *names* — never values) |
| `notes` | Optional free-form list: unassignable commits, exact-mode unavailability, dropped-group summaries, other distillation caveats |

## `steps` — dispatch packets with provenance receipts

Each step is a dispatch packet in the format `execute-dispatch-unit` consumes, executable as-is: `unit_id`, `objective`, `capability`, `allowed_scope`, `forbidden_scope`, `non_goals`, `dependencies`, `acceptance_criteria`, `verification`, `return_contract`. `dependencies` entries are bare step ids; the "output" a later step consumes is the repository state its dependencies left behind.

Use `R1`, `R2`, ... for `unit_id` so recipe steps are distinguishable from live dispatch plans (`W1`, ...).

Each step adds one block the packet format does not have:

```yaml
provenance:
  prompt_excerpt: "what the user actually asked (truncated/redacted is fine)"
  changed_files:
    - "path confirmed by the action log or git"
  commands:
    - "key commands actually run in the original session"
  commits:
    - "abc1234"        # checkpoint commits created by this step
  log_refs:            # pointers to the log records that confirm this step's claims
    - "9f4c2a1e-1234-4abc-9def-56789abcdef0.jsonl#L12-L48"
  validation:          # what actually validated this step in the original session
    command: "go test ./src/api/projects/..."   # exact command as run, or null
    commit: "4d5e6f7"                            # the commit state it validated, or null
    result: "pass: 12 ok, includes TestCreateMissingSlug"
  confidence: verified   # verified | unverified
```

Semantics:

- `log_refs` entries are `<log file basename>#L<start>-L<end>` 1-based line ranges into a `source.log_files` entry. They are trustworthy only while that file's `sha256` still matches; a hash mismatch downgrades every ref into that file.
- `confidence: verified` requires both: every `changed_files` entry confirmed by the action log or git history, **and** at least one `log_refs` entry pointing at the confirming records. A step whose facts are confirmed but whose confirming records are not pointed at is `unverified` — the claim must be auditable from the recipe alone. Anything reconstructed from memory is `unverified`. `confidence` covers the provenance facts only — it is independent of `validation` (a step can be `verified` yet never have been validated by tests).
- `validation.command` is the command exactly as the original session ran it — not a cleaned-up equivalent. `validation.commit` is the commit whose state that run validated. When the step was validated against uncommitted state, set `commit: null` and say so in `result`.
- `validation.result` must reflect what actually ran. When the original session never validated the step, write `command: null`, `commit: null`, `result: "not verified in original session"` — never invent a result.
- Freshness: `validation.result` is evidence about `validation.commit` only. It never counts as verification of a replay — replay must re-run the packet's `verification` against the current state, regardless of mode.
- No provenance field may contain a secret value. Reference secrets by env var name or key name only.

## `replay` — execution contract

| Field | Meaning |
| --- | --- |
| `mode` | `intent` (default): re-execute each packet against the current codebase. `exact`: cherry-pick `provenance.commits` per step; only valid when every step has commits |
| `order` | Step ids in execution order; must be consistent with each step's `dependencies` |
