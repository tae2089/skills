---
name: flow-design
description: Structure designs as pseudocode and Mermaid diagrams to expose implementation failure points before code exists and document existing flows after code exists. Use when the user asks for pseudocode or a logic/flow plan, a design diagram, an existing-code diagram (sequence, flowchart, state, component, ER), or immediately before implementing new logic with branches or side effects.
---

# Flow Design

1. Claims about existing code must come only from what was read. Do not infer from names or plausibility.
2. One artifact answers one question. Detail unrelated to the question is scope to cut, not value to add.
3. Closure: every path reaches a terminal and every branch shows every arm. An arm with no handling is a finding, not a scenario.
4. Declare what was not verified. Use `unverified` labels and omission notes; do not silently draw or silently omit.

## Design Path (Default)

1. Summarize the work unit and acceptance criteria in a few lines. Pull them from the task/spec, or restate the user's request as verifiable criteria.
2. Verify integration points in actual code and cite them as `file:line`: the existing entry point, callable function, and data to read or write. If no code exists yet, state that there are no existing integration points to cite. If the surrounding flow is unclear, trace the current flow first with `references/flow-tracing.md`.
3. If the logic is non-trivial, write numbered pseudocode with `references/pseudocode.md` and run its completeness check.
4. Render a diagram when the user asks for one, or when pseudocode has at least 3 non-validation branches or at least 2 side effects. Choose the type from the table below, read only that reference, and title it as a proposal (for example, "Proposed: order refund flow"). If pseudocode exists, it is the source.
5. Report **implementation risks**: gaps from the pseudocode completeness check, branch arms with no handling, and discovered ordering/concurrency risks. Cite each item with a `P` number or `file:line`.
6. Follow `references/scenario-extraction.md` only when the user asks for tests/scenarios or when the current task has a `task.md`.

Treat new logic as non-trivial when it adds branch logic or a side effect (`WRITE`, external/IO `CALL`, or `PUBLISH`). Skip this path for one-line edits, renames, config-only changes, and other changes with no new branches or side effects.

## Current-State Diagrams (Existing Code)

Use this when the user asks for an existing-code diagram, or when the design path needs the current flow as input.

- First, fix the question the diagram must answer in one sentence.
- For sequence/flowchart, follow `references/flow-tracing.md`.
- For state/component/ER, declare the scope implied by the question first; anything outside it goes to omissions without analysis.
- Report findings only inside the traced scope. Do not hunt for defects outside scope.
- Do not answer "how does the existing code work?" with a proposed diagram.

## Diagram Selection

| Question Shape | Diagram | Reference |
|---|---|---|
| Who calls whom, in what order, over time | Sequence | `references/types/sequence.md` |
| Which branches exist and where each path goes | Flowchart | `references/types/flowchart.md` |
| How an entity's state changes through its lifecycle | State | `references/types/state.md` |
| Which modules depend on which others, and where the seams are | Component | `references/types/component.md` |
| How persisted data relates | ER | `references/types/er.md` |

Common rules for all diagram types:

- Type reference `Notation` sections always apply. `Trace Completion` sections apply to current-state diagrams only.
- Evidence is the trace record or pseudocode source reformatted as citation lists. Put inline citations next to entry/integration points, `unverified` elements, findings, and implementation risks; provide the full Evidence block only when asked.
- Add a `?` suffix to labels for `unverified` elements.
- Add a `(proposed)` suffix to labels for not-yet-existing elements.
- If a diagram is titled `Proposed:` and every element is new, omit the `(proposed)` suffix.
- Label every decision edge with its condition.
- For proposed diagrams, Evidence uses pseudocode line numbers such as `P12` instead of `file:line`; without pseudocode, cite the work unit/spec source or state `greenfield proposal; no evidence yet`.

## Scale

If a diagram has roughly more than 15 elements or more than 3 levels of nesting, split by abstraction level: one overview plus sub-flow details. Do not produce one diagram that tries to hold everything.

## Completion Criteria

- The artifact answers the fixed question or work unit by itself; if split, the overview answers it.
- Closure is satisfied; omissions, declared scope, and `unverified` elements are explicit.
- For the design path: implementation risks were reported with `P` numbers or `file:line`, integration points were verified and cited in actual code, the `references/pseudocode.md` completeness check was reported if pseudocode was used, and new elements are visibly proposed by title or suffix.
- For current-state diagrams: out-of-scope defect hunting was avoided, and traced/proposed status is visible in the title.
- If Mermaid was produced, render it when `mmdc` or a repo script exists; fix syntax until it renders without errors. If no renderer is available, state that Mermaid syntax was not verified.
