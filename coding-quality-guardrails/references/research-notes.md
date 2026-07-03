# Research Notes

Read this only when the user asks for rationale, source-informed prompt design, or why these guardrails exist. These notes are background evidence, not implementation support for product code; cite the primary source itself when making an external claim.

Sources checked on 2026-06-28:

- Google Engineering Practices, Code Review: https://google.github.io/eng-practices/review/
  - Used for code health, small changes, reviewability, and what reviewers should inspect.
- Martin Fowler, Technical Debt: https://martinfowler.com/bliki/TechnicalDebt.html
  - Used for the future-change-cost framing of quality debt.
- Martin Fowler, Technical Debt Quadrant: https://martinfowler.com/bliki/TechnicalDebtQuadrant.html
  - Used for deliberate/inadvertent and prudent/reckless debt distinctions.
- Martin Fowler, Yagni: https://martinfowler.com/bliki/Yagni.html
  - Used for anti-speculative design guidance.
- SlopCodeBench: https://arxiv.org/abs/2603.24755
  - Used for the risk that agents pass checks while increasing verbosity and structural erosion.
- Are Coding Agents Generating Over-Mocked Tests?: https://arxiv.org/abs/2602.00409
  - Used for over-mocking guidance in agent-generated tests.
- An Endless Stream of AI Slop: https://arxiv.org/abs/2603.27249
  - Used for review friction, quality degradation, and maintainer burden themes from Reddit and Hacker News analysis.
- 9.6 Million Links in Source Code Comments: https://arxiv.org/abs/1901.07440
  - Used for caution around link rot in production comments.
- Comments on Comments: Where Code Review and Documentation Meet: https://arxiv.org/abs/2204.00107
  - Used for the role of comments in shared understanding during review.

Language-reference rules (added 2026-07-01) are grounded in primary language sources:

- Java/Kotlin: Effective Java (equals/hashCode contract, try-with-resources, defensive copies), Kotlin official docs (data classes, sealed `when` exhaustiveness, visibility modifiers, coding conventions), Hibernate/JPA guidance (entity equality), and the jackson-module-kotlin README (non-null deserialization).
- TypeScript: TypeScript Handbook and tsconfig docs (`useUnknownInCatchVariables`, `noUncheckedIndexedAccess`, `never` exhaustiveness, enums vs `as const`, `readonly`, `@ts-expect-error`), typescript-eslint (`prefer-nullish-coalescing`, `switch-exhaustiveness-check`), and MDN (equality coercion, `Promise.all`/`allSettled`).

Practical translation:

- Keep `SKILL.md` short enough to load for every supported-language coding task.
- Move language-specific details into separate references.
- Treat anti-slop and engineering-principle cores as generation-time guardrails, not review-only guidance.
- Use progressive loading so context cost scales with task risk.
- Keep attribution rules lightweight in `SKILL.md`; load `references/reference-attribution.md` only when external sources materially influence implementation or handoff.
