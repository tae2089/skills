---
name: coding-quality-guardrails
description: Coding quality guardrails for AI agents working on Go, Python, Java/Kotlin, or TypeScript. Use when Codex is coding, reviewing, refactoring, fixing tests, debugging regressions, preparing AI coding-agent prompts, or evaluating changes where AI slop, test gaming, over-abstraction, weak verification claims, or quality debt must be prevented.
---

# Coding Quality Guardrails

Use this skill as a compact quality gate for Go, Python, Java/Kotlin, and TypeScript work. Apply the core rules for every coding task, then load only the smallest reference set needed.

## Progressive Loading

| Situation | Read additionally |
|---|---|
| Any supported-language code generation or edit | None unless a row below applies |
| Go code | `references/go.md` |
| Python code | `references/python.md` |
| Java or Kotlin code | `references/java-kotlin.md` |
| TypeScript code | `references/typescript.md` |
| Test failure, refactor, large diff, complex change, or legacy hot spot | `references/quality-debt.md` plus language reference |
| API, CLI, config, schema, persistence, security, auth, validation, or error-semantics change | `references/engineering-principles.md` plus language reference |
| External docs, specs, issues, articles, or community references materially influence the implementation or handoff | `references/reference-attribution.md` |
| User asks for rationale, source-informed prompt design, or why these rules exist | `references/research-notes.md` |

Do not read research notes during ordinary coding. They are background rationale, not execution guidance.

## Core Rules

- Read relevant code and nearby tests before editing.
- Identify the user-visible contract and make the smallest safe, reversible change.
- Verify real symbols, APIs, config keys, file paths, command flags, and data shapes before relying on them.
- Do not invent test results, logs, benchmark numbers, issue links, docs claims, or runtime behavior.
- Keep diffs reviewable: avoid broad rewrites, noisy formatting churn, speculative abstractions, and verbose low-value code.
- Use KISS, YAGNI, and cautious DRY: simple and current, but not under-specified; remove duplicated knowledge, not every repeated line.
- Before adding code, climb the reuse ladder: an existing helper or pattern in this codebase, then the standard library, then a native platform feature, then an already-installed dependency, then the fewest new lines. Never add a new dependency for what a few lines can do.
- Prefer deletion over addition; aim for the fewest files and the shortest change that fully solves the problem — decided after understanding the flow, not instead of it.
- Preserve contracts and invariants: validation, security, authorization, persistence, compatibility, observability, typing, and error semantics.
- Do not change production code only to satisfy tests; first decide whether the failure is product defect, stale expectation, flake, or setup issue.
- Treat test-gaming signals as suspicious: deleted assertions, weakened expected values, new skip/xfail, mocks replacing real local behavior, or production-only branches for tests.
- Avoid over-mocking; prefer tests that exercise real local behavior and mock only external boundaries.
- Leave touched code at least as maintainable as before; do not introduce hidden debt for speed.
- Do not leave dead code, unused helpers, debug prints, temporary flags, abandoned TODOs, or unexplained special cases.
- Be able to explain what changed, why it is correct, and what evidence supports it.
- Report verification honestly, including what was not checked.
- Name material external references used for implementation decisions; put links in code comments only when the source is needed to understand or safely maintain that code.

## Working Procedure

1. Select references using the progressive loading table.
2. Edit using the repository's existing architecture and language conventions.
3. Run the narrowest relevant verification first, then broader checks when risk warrants it.
4. Before final response, inspect the diff against anti-slop, test-integrity, quality-debt, and reference-attribution rules.
5. In the final response, include verification and any material external references used.
