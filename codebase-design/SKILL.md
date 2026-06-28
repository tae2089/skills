---
name: codebase-design
description: Shared discipline for designing deep modules, small interfaces, clean seams, adapters, test surfaces, and architecture improvements. Use when designing or reviewing module boundaries, refactors, controller/service composition, interface shape, testability, coupling, dependency injection, or when another skill needs architecture vocabulary for deepening code.
---

# Codebase Design

Use this skill to reason about code shape before or during implementation. Favor deep modules: a lot of behavior behind a small, stable interface, placed at a seam that improves locality and testability.

Adapted from Matt Pocock's `codebase-design` skill in `mattpocock/skills` at commit `5d78bd0903420f97c791f834201e550c765699f8`.

## Vocabulary

Use these terms consistently:

- `module`: something with an interface and an implementation. It may be a function, package, class, service slice, or tier-spanning workflow.
- `interface`: everything a caller must know to use a module correctly, including types, invariants, ordering, errors, config, and performance.
- `implementation`: what lives behind the interface.
- `seam`: the place where behavior can vary without editing the caller.
- `adapter`: a concrete implementation that satisfies a seam.
- `depth`: leverage at the interface. A deep module exposes a small interface and hides meaningful behavior.
- `locality`: the degree to which changes, bugs, and knowledge are concentrated instead of scattered through callers.
- `leverage`: the capability callers gain per unit of interface they learn.

Prefer these words over vague substitutes such as component, service, API, or boundary when the design concern is module shape.

## Design Checks

When evaluating a design, ask:

- Does the interface hide complexity or merely pass it through?
- Would deleting the module remove complexity, or spread that complexity across callers?
- Are tests able to verify behavior through the same interface callers use?
- Is a seam real because at least two adapters or modes justify it, or is it speculative indirection?
- Do dependencies enter the module from the outside, or does the module secretly construct hard-to-test dependencies?
- Does the module return observable results where possible, instead of scattering side effects?
- Can a caller use the common case without knowing rare-case machinery?

## Deepening Workflow

1. Identify the cluster that feels shallow, scattered, or hard to test.
2. Name the domain concept it should represent. Use the `domain-modeling` skill if available and the term is unclear.
3. Classify its dependencies and test strategy. Read `references/deepening.md` when dependencies drive the design.
4. Propose the smallest interface that gives callers leverage.
5. Place the seam where behavior genuinely varies.
6. Design tests through the proposed interface, not through internals.
7. Prefer replacing shallow tests with interface-level tests once the deep module exists.

When alternatives matter, read `references/design-it-twice.md` and compare distinct interface candidates before choosing.

## Output Shape

For design or review work, return:

- Current friction: where complexity, coupling, or testing pain shows up.
- Proposed module and interface.
- What the implementation hides.
- Seam and adapter strategy, if any.
- Test surface.
- Trade-offs and migration steps.

Keep the recommendation opinionated. The user needs a design judgment, not a menu of equal options.
