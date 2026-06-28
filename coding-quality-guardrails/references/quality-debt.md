# Quality Debt Reference

Read this for refactors, test-failure fixes, large diffs, legacy hot spots, hard-to-test code, security-sensitive code, or any change where maintainability risk is meaningful.

## Quality Debt Rules

- Quality debt is future change cost created by unclear, coupled, duplicated, fragile, or misleading code.
- Prevention is usually cheaper than repayment. Prefer small quality-preserving decisions while editing.
- High-churn, user-critical, security-sensitive, and hard-to-test areas have low tolerance for new debt.
- Reviewability is quality control. Split mechanical edits from behavior changes when practical.
- Hidden debt is worse than intentional debt. If a compromise is necessary, make the reason and payback path visible.

## Common AI-Created Debt

- Large functions with one more branch added each time.
- Copy-paste growth with slightly divergent validation or error behavior.
- Premature abstractions that freeze accidental similarities.
- Broad utility modules or helpers that hide domain meaning.
- Tests that validate mocks rather than product behavior.
- Relaxed validation, swallowed errors, broad fallbacks, or weaker invariants.
- Public API or config expansion for a local implementation convenience.

## Test-Gaming Signals

- Deleted or weakened assertions without a product-contract reason.
- Expected values changed to match current output without explaining why the old expectation was wrong.
- New `skip`, `xfail`, `t.Skip`, or broad test filtering that hides the failing behavior.
- Production code branches keyed on test-only environment variables, file names, clocks, or magic constants.
- Mocks replacing real local parsing, validation, serialization, state transitions, or error mapping.
- Tests asserting implementation details because observable behavior is inconvenient to verify.
- Fixture changes that remove the edge case the test was meant to cover.
- Relaxed validation or broader exception swallowing introduced alongside a test fix.

## Diff Review Checklist

- Did the change increase branches, hidden state, or coupling without clarifying structure?
- Did it add a shared abstraction before the shared concept was stable?
- Did it duplicate domain rules, validation, serialization, authorization, or error mapping?
- Did it make failure behavior less explicit?
- Did it add mocks that reduce confidence in real behavior?
- Did it remove or weaken assertions, expected values, or failure coverage?
- Did it add skip/xfail/filtering instead of explaining or fixing the behavior?
- Did it leave cleanup for an unnamed future maintainer?
- Can this change be reviewed, tested, rolled back, or split easily?
