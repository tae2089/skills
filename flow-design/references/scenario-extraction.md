# Scenario Extraction

Convert the branches of a complete trace or pseudocode block into a test scenario list.

Build the smallest scenario set that covers every branch arm at least once. Add scenarios beyond arm coverage only for risky combinations: later failure after earlier side effect, concurrency, or repeated calls.

Format:

```text
- [ ] <name>: given <input/state>, when <entry action>, then <observable terminal> (branch: <file:line or P-number>)
```

The `then` clause must state an observable terminal from the trace or pseudocode: response code, persisted row, published event, or error type. Do not assert internals. Arms with no handling stay as findings; do not write tests that freeze a defect as intended behavior.

If the project tracks TDD work in `task.md`, add scenarios there as Todo items; otherwise deliver them next to the diagram.
