# Design It Twice

Use this when the interface is consequential and the first plausible design may anchor the work too early.

## Process

1. Frame the problem: constraints, callers, invariants, dependency categories, and what the module must hide.
2. Generate at least two substantially different interface candidates. Use more candidates when the design is high-risk.
3. Compare candidates by depth, locality, seam placement, adapter strategy, and test surface.
4. Recommend one design or a deliberate hybrid.

## Candidate Prompts

Use different constraints for each candidate:

- Minimize interface size: 1-3 entry points if possible.
- Optimize the common caller path.
- Maximize extension and configuration.
- Design around ports and adapters for cross-seam dependencies.

Each candidate should include:

- Interface shape, including invariants and error modes.
- Example caller usage.
- Hidden implementation responsibilities.
- Dependency and adapter strategy.
- Trade-offs and failure modes.
