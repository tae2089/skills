# Engineering Principles Reference

Read this when design judgment matters, principles conflict, or a change touches API shape, module boundaries, persistence, configuration, or architecture.

## Core Principles

- KISS: use the simplest design that preserves correctness, observability, and domain rules.
- YAGNI: avoid speculative future flexibility. Add extension points only when current requirements need them.
- DRY: remove duplicated knowledge. Repeated lines are acceptable when the concepts are not truly shared.
- Separation of concerns: keep parsing, validation, authorization, orchestration, domain behavior, persistence, transport, and presentation in their established layers.
- Single responsibility: group code that changes for the same reason; separate code that changes for different policies, users, data sources, or release cadences.
- High cohesion, low coupling: keep related behavior together and avoid dependencies that force unrelated modules to change together.
- Least astonishment: preserve expected behavior for APIs, commands, errors, defaults, logs, side effects, and compatibility.
- Explicit contracts: make inputs, outputs, invariants, ownership, cancellation, errors/exceptions, and side effects clear.
- Fail clearly: prefer early validation and contextual errors over silent fallback, partial success, or ambiguous zero/`None` values.
- Optimize last: add caching, concurrency, batching, pooling, vectorization, or clever data structures only with evidence or clear need.

## Conflict Resolution

- Correctness beats simplicity.
- Existing user-visible contracts beat internal tidiness.
- Clear duplication beats wrong abstraction.
- Local consistency beats introducing a new pattern, unless the existing pattern is actively harmful.
- Security, data integrity, and error semantics beat speed of implementation.
- Small reversible changes beat large impressive rewrites.

## AI-Agent Misuse To Avoid

- Do not cite SOLID to justify unnecessary interfaces, base classes, factories, decorators, or dependency graphs.
- Do not use DRY to merge code with different domain meanings.
- Do not use KISS as an excuse to skip edge cases or validation.
- Do not use YAGNI to avoid designing the contract needed by the current task.
- Do not use consistency to spread a harmful legacy pattern beyond the touched area.

