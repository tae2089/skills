# Context Format

Use this format for glossary-style domain context. Keep it free of implementation plans, task lists, and scratch notes.

```md
# Context

## Purpose

One paragraph describing the domain this context covers.

## Terms

### Canonical Term

Definition in domain language.

- Avoid: rejected or ambiguous alternatives.
- Related: other canonical terms.
- Notes: edge cases or invariants that define the concept.
```

Guidelines:

- Prefer short definitions that help future agents name code, docs, and tests consistently.
- Include only terms that have been resolved enough to be useful.
- Put implementation decisions in ADRs, not in the glossary.
- If multiple bounded contexts exist, keep each context's terms in its own file and maintain a root `CONTEXT-MAP.md`.
