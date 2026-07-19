# Capture Format

Structure for `_workspace/<task-name>/compound-learning.md`:

```markdown
# Compound Learning
## Summary
## Track
## Evidence
## What Happened
## What Worked
## What Did Not Work
## Reusable Guidance
## Future Search Terms
## Solution Doc Decision
## Follow-Ups
```

Keep it concise. Link to source artifacts by path instead of copying long excerpts.

## Field Guidance

- **Track**: `bug` or `knowledge`, one line.
- **Evidence**: paths to state files, test or validation output, review artifacts, and relevant diffs. Every claim elsewhere in the file must trace to an entry here.
- **What Did Not Work**: failed approaches with the reason each failed. This section prevents the next agent from retrying dead ends — do not leave it empty when failures occurred.
- **Future Search Terms**: terms a future agent is likely to search when facing the same issue — concrete command names, file paths, error codes, API names, module names, domain terms, and symptom phrases. Avoid generic terms such as "bug", "fix", "error", "issue", or "broken" unless paired with a concrete identifier.
- **Solution Doc Decision**: exactly one of `promote`, `update_existing`, `skip`, plus one sentence explaining the choice.

## Downstream Contract

When a later task should consume the learning, pass compact metadata only:

- `compound_learning_ref` — path to the capture file
- `solution_doc_ref` — path to the solution doc, if any
- `learning_track` — `bug` or `knowledge`
- `refresh_scope` — what the consumer should re-check, if anything

Do not duplicate the full learning in task metadata. Full prose lives in the artifacts.
