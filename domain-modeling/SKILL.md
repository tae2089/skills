---
name: domain-modeling
description: Build and sharpen a project's domain language and decision record. Use when terminology is ambiguous, the user wants canonical terms, glossary work, DDD-style ubiquitous language, ADRs, context docs, naming alignment, or when planning/design work depends on precise domain concepts before implementation.
---

# Domain Modeling

Use this skill when the project language itself is part of the work. The output is clearer terminology, better names, and durable context documents where appropriate.

Adapted from Matt Pocock's `domain-modeling` skill in `mattpocock/skills` at commit `5d78bd0903420f97c791f834201e550c765699f8`.

## Operating Mode

Actively sharpen the model while the design conversation happens:

1. Read existing domain docs if present: `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, `AGENTS.md`, or local repo guidance.
2. Identify terms that are overloaded, vague, contradictory, or missing.
3. Check user claims against code when the code can cheaply confirm or contradict them.
4. Stress-test terms with concrete edge-case scenarios.
5. Propose canonical terms and ask for confirmation when the choice affects design or implementation.
6. Update durable docs inline when a term or decision crystallizes and the user has asked for durable capture or the repo convention expects it.

Do not turn a glossary into a spec. Keep domain language separate from implementation details unless the document explicitly asks for both.

## Context Layouts

Use the repo's existing convention. Common layouts:

- Single-context repo: root `CONTEXT.md` plus root `docs/adr/`.
- Multi-context repo: root `CONTEXT-MAP.md` pointing to context-specific `CONTEXT.md` and ADR folders.
- Agent-instruction repo: root `AGENTS.md` may be the durable place for workspace rules, while domain terms live in a separate docs file.
- No convention: create files only after the user approves the location or after a repo-local convention makes the location obvious.

Read `references/context-format.md` before creating or rewriting a glossary-style context file. Read `references/adr-format.md` before creating an ADR.

## When To Challenge

Challenge immediately when:

- One word appears to name two different concepts.
- Two words appear to name the same concept.
- The user's term conflicts with an existing glossary or code name.
- A proposed name hides an important distinction.
- A domain rule has unclear boundaries, lifecycle states, or exceptions.

Use concrete scenarios instead of abstract debate. For example: "If an order is partially refunded and then cancelled, which concept owns the final state?"

## ADR Gate

Offer or write an ADR only when all are true:

- The decision is costly or confusing to reverse.
- Future maintainers would reasonably ask why this path was chosen.
- There was a real trade-off among alternatives.

Skip ADRs for obvious choices, temporary preferences, or implementation notes that belong near code.

## Done Criteria

End with:

- Canonical terms and rejected synonyms, if any.
- Any updated files.
- Any unresolved terminology questions.
- Any ADRs created or intentionally skipped.
