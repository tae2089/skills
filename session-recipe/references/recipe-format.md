# Recipe Format

A recipe is one YAML document with three top-level keys: `recipe`, `steps`, `replay`.

## `recipe` — metadata

| Field | Meaning |
| --- | --- |
| `name` | Kebab-case task name; matches the `_workspace/<task-name>/` folder when one exists |
| `created` | ISO timestamp of distillation |
| `source.session_ids` | Session ids the recipe was distilled from |
| `source.log_files` | Action-log paths used as ground truth (empty if none existed) |
| `source.repo` | Origin URL, or absolute path when there is no remote |
| `source.base_commit` | Git head at the first recorded prompt; replay preconditions check against this |
| `environment` | Runtime requirements replay needs (toolchain versions, cluster context, env var *names* — never values) |
| `notes` | Optional free-form list: unassignable commits, exact-mode unavailability, dropped-group summaries, other distillation caveats |

## `steps` — dispatch packets with provenance

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
  verification_evidence: "short summary of the original verification result"
  confidence: verified   # verified | unverified
```

Semantics:

- `provenance` is evidence about the past; the packet fields are instructions for the future. Replay reads the packet fields and consults provenance only for `exact` mode and drift reporting.
- `confidence: verified` requires every `changed_files` entry to be confirmed by the action log or git history. Anything reconstructed from memory is `unverified`. `confidence` covers the provenance facts only — it is independent of `verification_evidence` (a step can be `verified` yet never have been verified by tests).
- `verification_evidence` must reflect what actually ran. When the original session never verified the step, write `"not verified in original session"` — never invent a result.
- No provenance field may contain a secret value. Reference secrets by env var name or key name only.

## `replay` — execution contract

| Field | Meaning |
| --- | --- |
| `mode` | `intent` (default): re-execute each packet against the current codebase. `exact`: cherry-pick `provenance.commits` per step; only valid when every step has commits |
| `order` | Step ids in execution order; must be consistent with each step's `dependencies` |
