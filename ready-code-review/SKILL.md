---
name: ready-code-review
description: Prepare code-review context briefs, PR/diff context packages, severity rubrics, false-positive suppressions, reusable reviewer instructions, and AI reviewer prompts. Use for AI review preparation, PR or diff review context, review invariants/non-goals, P0/P1/P2/P3 calibration, and instructions for Codex, GitHub Copilot, CodeRabbit, Cursor, or other reviewers. Do not use when the user asks to perform the code review itself.
---

# Review Context Preparation

## Purpose

Attach the evidence, intent, contracts, tests, and operational context a reviewer needs so they do not have to infer intent from a diff, file list, or short description alone. Git, PR, and repository access are possible evidence sources, not hard requirements.

## Workflow

1. Choose the requested output mode: review context brief, PR/diff-specific context package, severity/suppression calibration note, reusable reviewer instruction, or AI reviewer prompt. If the request is clear, follow it without asking. Ask a targeted question only when multiple modes would produce meaningfully different outputs. If the user asks for review findings themselves, do not perform that review with this skill; say that a separate review procedure is needed.
2. Use `references/context-discovery.md` to find and record evidence sources. If Git is unavailable, use provided diffs, old/new snippets, file content, change descriptions, logs, screenshots, the current filesystem, docs, tests, and runbooks.
3. Classify evidence as orientation evidence or change evidence. `git status`, file lists, PR titles, and task descriptions orient the work. Diffs, patches, commits, PR files, old/new snippets, and before/after file content establish changed behavior.
4. Change-specific context and change-specific reviewer prompts require change evidence. If change evidence is missing, do not create future-finding instructions; ask for the needed input as a targeted question. Do not stop only because Git is unavailable.
5. If repository or filesystem access is available, run `rg --files` for standard candidates: `AGENTS.md`, `README*`, `docs/**`, `.github/**`, `_workspace/**/task.md`, runbooks, design notes, tests, and config. Record found and absent candidates in Source Discovery. If access is unavailable, record `N/A: no repository or filesystem access`.
6. From collected evidence and nearby context, reconstruct change intent, affected contracts, invariants, tests/verification, operational assumptions, and non-goals. Label any unverified assumption that determines whether a finding exists with `Assumption:` and turn it into a targeted question instead of a finding.
7. When creating a review context brief, follow the section structure in `references/context-brief.md`.
8. When creating a PR/diff-specific context package, follow the section structure in `references/context-package.md`. Use that reference for the Non-Goal section structure and empty-value conventions.
9. When creating a severity/suppression calibration note, use `references/severity-calibration.md`, `references/severity-rubric.md`, `references/finding-contract.md`, and `references/false-positive-patterns.md`. Do not force diff-specific sections to be filled with `N/A`.
10. When creating reusable reviewer instructions, use `references/reusable-instruction.md` and `references/severity-rubric.md`, and include the reviewer investigation protocol from `references/investigation-protocol.md`. Do not force diff-specific sections to be filled with `N/A`.
11. When judging P0/P1/P2/P3, blocking/non-blocking, confidence, or reviewer instructions, calibrate with `references/severity-rubric.md`.
12. Define the required finding shape and rejection rules for future human or AI reviewers with `references/finding-contract.md`.
13. Use `references/false-positive-patterns.md` to fill False-positive Suppression or Suppression Policy sections. If nothing applies, write `none known`. If repository access is available, check `.github/review-suppressions.md`, `docs/review-suppressions.md`, and relevant `AGENTS.md` sections, then merge repo-local suppressions with the global patterns.
14. If the output will be pasted into another AI reviewer, use `references/reviewer-prompt-template.md` to create a reviewer-ready prompt. Do not rely on filenames or repository access; embed the context package or brief, severity summary, finding contract, rejection rules, relevant suppressions, the reviewer investigation protocol from `references/investigation-protocol.md`, and concrete change evidence directly in the prompt.

## Completion Criteria

- Source Discovery records checked standard candidate files, absent candidates, or the reason repository/filesystem access is unavailable.
- Each evidence source used is classified as provided evidence, repository evidence, filesystem evidence, or external/referenced evidence.
- Change-specific context and change-specific reviewer prompts record at least one change-evidence source: diff, patch, commit, PR files, old/new snippet, or before/after file content.
- If only `git status`, file lists, PR titles, or task descriptions are available, no future-finding instructions are created; the missing change evidence is requested as a question.
- Brief mode: every required section in `references/context-brief.md` is filled and includes Source Discovery, Evidence Source, Review Focus, Non-Goal, False-positive Suppression, and Open Questions.
- Context package mode: every required section in `references/context-package.md` is filled, or each missing section is marked `N/A` with a reason.
- Severity/suppression calibration mode: every required section in `references/severity-calibration.md` is filled, or each missing section is marked `N/A` with a reason.
- Reusable instruction mode: every required section in `references/reusable-instruction.md` is filled, or each missing section is marked `N/A` with a reason.
- Reviewer prompt mode: the prompt is paste-ready and directly includes the context package or brief, severity summary, finding contract, rejection rules, false-positive suppression, the reviewer investigation protocol (diff-anchored, narrow-before-read, batched navigation), and concrete change evidence. The Evidence placeholder may contain only a diff, patch, PR files, old/new snippet, or changed file excerpt; do not use repository-access placeholders.
- For PR/diff-specific work, changed behavior, affected contracts, tests, and operational assumptions are identified from change evidence plus nearby context, or turned into targeted questions.
- For reusable reviewer-instruction work, durable review invariants, repo conventions, operational contracts, severity policies, and suppressions are identified without a diff, or turned into targeted questions.
- Every assumption that determines whether a finding exists is labeled and either verified or turned into a question.
- Non-goals and false-positive suppressions are present even when empty, using `none known`.
- Any P0/P1/P2/P3 or blocking label in the output is grounded in the severity rubric.
- Future findings have changed-line relevance and an evidence contract: they are directly related to a changed line or nearby line, and they include at least one supporting evidence source such as nearby code path, documented contract, test, log, or runbook.
- If producing a reviewer prompt, the prompt includes the rubric summary and suppressions directly instead of depending on external references.

## Output Rules

- Match the final output to the requested preparation mode: a context brief is a short review briefing, a calibration note is a severity/suppression calibration table, a reviewer prompt is paste-ready, and reusable instructions are durable reviewer guidance.
- Do not turn areas with insufficient context into finding instructions; separate them into Open Questions.
