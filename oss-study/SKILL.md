---
name: oss-study
description: Study an open-source codebase using a four-mode (Diátaxis-based) question structure that keeps each question to a single learning intent. Use when the user wants to study an unfamiliar repo or library for learning (e.g. "이 오픈소스로 스터디하자", "이 라이브러리 어떻게 동작하는지 공부하자"), or to understand a dependency's internals before adopting it. Not for shipping a fix.
---

# OSS Study

Guide structured study of an open-source codebase by asking one *kind* of question at a time — each question stays in a single mode.

## The Four Modes

Every question about the code fits one of four modes.

| Mode | Intent | Question shape |
|------|--------|----------------|
| **Explanation** | 왜 이런가 (설계 이해) | "이 모듈이 왜 이렇게 나뉘어 있어? 어떤 대안이 있었고 왜 이걸 골랐을까?" |
| **Tutorial** | 따라하며 감 잡기 | "가장 단순한 동작 하나를 처음부터 끝까지 돌리는 최소 예제를 만들어줘. 각 줄이 뭘 하는지 주석으로." |
| **Reference** | 정확한 사실 | "이 함수의 시그니처·입출력·예외 조건을 코드 근거로 정확히 정리해줘." |
| **How-to** | 응용/변경 | "X를 커스터마이즈하려면 어느 파일 어느 부분을 건드려야 해? 실제 확장 포인트를 짚어줘." |

## Procedure

1. **Confirm the target.** Identify the specific repo/library and whether it is available locally. If given only a URL, clone it with full history (not shallow). This step is complete when a local path exists. Do not proceed on a guessed target.
2. **Explanation first — the big picture.** Explain why the whole is structured the way it is: entry points, top-level module boundaries, how the core modules interact. "The whole" is the smallest unit containing the learner's stated interest — for a single function, its module. If several equal subsystems could be the target, list them and ask rather than choosing silently. Use a read-only exploration agent or codebase-summary skill if the host runtime provides one, to ground the answer in the actual tree, not assumptions.
3. **Tutorial — one representative flow.** Pick the single most representative use case — if none stands out, propose 2–3 candidates and let the learner pick. Walk one minimal end-to-end example, annotating each step: runnable if the project supports a trivial local run, otherwise an annotated code-path trace.
4. **Reference — the facts on that flow.** For the functions/types touched in step 3, state exact signatures, inputs/outputs, and error conditions.
5. **How-to — apply it.** Answer a concrete "how would I change/extend X here?" using the real extension points found above. If the learner has not named a change, propose one representative modification and answer it.

After each mode produces a concrete, evidence-backed answer, stop and take the learner's follow-ups; advance only when the learner is ready. The learner's own questions may target any mode at any time.

## Rules

- **One mode per question.** If a request bundles modes, split it and answer them separately, naming the mode each time.
- **Cite the code.** Reference and How-to answers must point to `file:line`; never present an unverified claim as fact.
- **Prefer history when it teaches.** For Explanation, use `git log`/`git blame` on the relevant lines to recover *why* it changed, not just its current state.

## Completion Criteria

The study of a chosen flow is complete when all of the following hold:

- The overall architecture (entry point + core module interactions) has been stated.
- One end-to-end flow has been walked with an annotated minimal example.
- Every function or type named in the step-3 walkthrough has a `file:line`-cited signature/definition and behavior note.
- At least one concrete "how to change X" answer points to a real extension point.
- The learner has confirmed the flow is understood, or named the next flow to study.
