# ADR Format

Use ADRs for durable architectural or product decisions that involve meaningful trade-offs.

```md
# ADR NNNN: Decision Title

## Status

Accepted

## Context

What forced the decision, including constraints and relevant domain terms.

## Decision

The choice made.

## Alternatives Considered

- Option A: trade-off.
- Option B: trade-off.

## Consequences

- Positive consequence.
- Negative or risky consequence.
- Follow-up needed, if any.
```

Guidelines:

- Keep the title specific enough that future readers know when to open it.
- Record why the decision was made, not just what changed.
- Link to issues, PRs, or docs when those links are needed to understand the decision.
- Do not use ADRs for obvious implementation steps or reversible preferences.
