---
name: flow-design
description: Structure designs as pseudocode and Mermaid diagrams to expose implementation failure points before code exists. Use when the user asks for pseudocode or a logic/flow plan, a design diagram, an existing-code diagram (sequence, flowchart, state, component, ER), or immediately before implementing new logic with branches or side effects.
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
4. If the user wants a diagram or a structural review would benefit from one, render it: choose the type from the table below, read only that reference, and title it as a proposal (for example, "Proposed: order refund flow"). If pseudocode exists, it is the source.
5. Report discovered failure points as an **implementation risks** list.
6. Follow `references/scenario-extraction.md` only when the user asks for tests/scenarios or when handing off to an existing test list such as `task.md`.

Treat new logic as non-trivial when it adds branch logic or a side effect (`WRITE`, external/IO `CALL`, or `PUBLISH`). Skip this path for one-line edits, renames, config-only changes, and other changes with no new branches or side effects.

## Current-State Diagrams (Existing Code)

Use this when the user asks for an existing-code diagram, or when the design path needs the current flow as input.

- For sequence/flowchart, follow `references/flow-tracing.md`.
- For component/ER, declare the scope implied by the question first; anything outside it goes to omissions without analysis.
- Cite `file:line` only where it carries weight: `unverified` elements, findings, and integration points. Put required citations in text next to the diagram; provide the full Evidence block only when asked.
- Report findings only inside the traced scope. Do not hunt for defects outside scope.
- Do not answer "how does the existing code work?" with a proposed diagram. A diagram is either traced or proposed, and its title says which.

## Diagram Selection

| Question Shape | Diagram | Reference |
|---|---|---|
| Who calls whom, in what order, over time | Sequence | `references/types/sequence.md` |
| Which branches exist and where each path goes | Flowchart | `references/types/flowchart.md` |
| How an entity's state changes through its lifecycle | State | `references/types/state.md` |
| Which modules depend on which others, and where the seams are | Component | `references/types/component.md` |
| How persisted data relates | ER | `references/types/er.md` |

Common rules for all diagram types:

- Add a `?` suffix to labels for `unverified` elements.
- Add a `(proposed)` suffix to labels for not-yet-existing elements.
- Label every decision edge with its condition.
- For proposed diagrams, Evidence uses pseudocode line numbers such as `P12` instead of `file:line`; without pseudocode, cite the work unit/spec source or state `greenfield proposal; no evidence yet`.

## Scale

If a diagram has roughly more than 15 elements or more than 3 levels of nesting, split by abstraction level: one overview plus sub-flow details (one artifact, one question). Do not produce one diagram that tries to hold everything.

## Completion Criteria

- The artifact answers the fixed question or work unit by itself; if split, the overview answers it.
- Closure is satisfied; omissions, declared scope, and `unverified` elements are explicit.
- For the design path: implementation risks were reported, integration points were verified and cited in actual code, the `references/pseudocode.md` completeness check was reported if pseudocode was used, and all new elements carry the `(proposed)` suffix.
- For current-state diagrams: out-of-scope defect hunting was avoided, and traced/proposed status is visible in the title.
- If Mermaid was produced, render it when `mmdc` or a repo script exists; otherwise state that Mermaid syntax was not verified.
