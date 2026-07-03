# Flow Tracing

Trace before drawing. The output of this procedure is the trace record that supports the diagram.

## Entry Points

If the user gives a feature name rather than an entry point, search route, command, consumer, or scheduler registration first, then confirm that the entry point matches the user's description.

## Tool Use

Use available code graph, LSP, or search tools, but confirm each hop in source before adding it to the trace. Tool output is a clue, not proof. Record `file:line` for places that may later carry weight: `unverified` targets, findings, and integration points.

## Hop Record

For each hop in the call chain, record:

- caller -> callee, with the call site
- data shape changes, if any: what is parsed, mapped, enriched, or dropped
- validation performed, or `none`
- error behavior: propagated, wrapped, swallowed, retried, or terminated
- side effects: DB writes, publishes, external calls, file/cache changes

## Branch Enumeration

For every condition, error return, early return, retry, and timeout on the path, record the condition and destination of each arm. Do not stop at the happy path. The trace is complete only when every arm reaches a terminal or an explicit boundary.

## Boundaries

At process or ownership boundaries (external services, third-party SDK internals, other-team systems), stop tracing and mark an explicit boundary node instead of guessing internals. Inside the codebase, do not stop early on the main line: "enters service layer" is not a terminal. Fold question-irrelevant side calls instead of tracing them; see Depth Control.

## Depth Control (summary boundaries)

Trace depth follows the fixed question: descend only when the callee can change the branch structure at the question's altitude.

For callees that cannot change it (common utilities, mappers, logging, generic repo/ORM internals, validation internals when the question only needs pass/fail), use a summary boundary node: cite the callee definition as `file:line`, record observable outcomes (success plus each failure arm the caller handles) as edges, and omit internals. Summary boundaries count as explicit boundaries for closure; list each folded callee in omissions.

Folding is for side calls. Never fold the call chain that carries the fixed question's data to completion.

## Unresolvable Targets

Dynamic dispatch, reflection, DI container wiring, and config-selected implementations can block static resolution. If possible, list candidate targets (interface implementations, registered handlers). If wiring evidence selects one, treat the hop as resolved and cite the wiring. Otherwise, record the hop at the interface/dynamic target level with the call site's `file:line`, mark it `unverified`, and leave candidates as notes. Do not promote guesses into the trace.
