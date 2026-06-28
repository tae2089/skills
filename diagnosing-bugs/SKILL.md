---
name: diagnosing-bugs
description: Disciplined diagnosis loop for hard bugs, regressions, flaky behavior, failing tests, broken UI flows, performance regressions, and user-reported failures. Use when the user asks to debug, diagnose, investigate, reproduce, find root cause, or fix something broken, slow, failing, throwing, intermittent, or behaviorally wrong.
---

# Diagnosing Bugs

Use this skill to debug from evidence instead of vibes. Build a tight feedback loop first, then reproduce, minimize, hypothesize, instrument, fix, and regression-test.

Adapted from Matt Pocock's `diagnosing-bugs` skill in `mattpocock/skills` at commit `5d78bd0903420f97c791f834201e550c765699f8`.

## Core Rule

Do not start by changing code. First create or identify a feedback loop that can catch the user's exact symptom.

A usable loop is:

- `red-capable`: it drives the actual failing path and can fail for this bug.
- `specific`: it asserts the reported symptom, not merely "does not crash".
- `repeatable`: deterministic, or high-reproduction for flaky bugs.
- `fast enough`: narrow enough to run repeatedly while debugging.
- `agent-runnable`: runnable by command, script, test, browser automation, or a clearly bounded manual loop.

If no loop can be built, stop and report what was tried. Ask for missing reproduction access, logs, traces, recordings, fixtures, or permission to add temporary instrumentation.

## Diagnosis Loop

1. Build the feedback loop.
2. Run it and confirm it reproduces the user's symptom.
3. Minimize the repro until only load-bearing steps, inputs, config, or data remain.
4. Write 3-5 ranked hypotheses before testing any one of them.
5. Instrument one hypothesis at a time.
6. Fix the confirmed cause with the smallest change that preserves contracts.
7. Add or keep a regression check at the correct seam.
8. Clean up debug artifacts and rerun the original loop.

## Feedback Loop Options

Prefer the narrowest loop that still catches the real bug:

- A failing unit, integration, or end-to-end test.
- A CLI command with a fixture and expected output.
- A curl or HTTP script against a running service.
- A browser automation script that checks DOM, console, or network behavior.
- A replay of a captured request, event, trace, or payload.
- A throwaway harness around the smallest runnable subset of the system.
- A property, fuzz, stress, or repeated-run loop for nondeterministic behavior.
- A differential loop comparing old vs new commit, version, data, or config.
- `git bisect run` when the regression window is known.

For flaky bugs, the first goal is not perfect determinism. Raise the reproduction rate enough to debug: loop many times, parallelize, pin seeds or time, add stress, narrow the timing window, and capture failure counts.

## Hypothesis Discipline

Each hypothesis must be falsifiable:

```text
If <cause> is responsible, then <probe or change> should make <observable result> happen.
```

Test one variable at a time. Prefer debugger or REPL inspection when available, then targeted logs. Tag temporary logs with a unique prefix such as `[DEBUG-abc123]` so cleanup is grep-able.

For performance regressions, measure before fixing. Establish a baseline with a timing harness, profiler, query plan, or trace, then change one variable at a time.

## Regression Check

Turn the minimized repro into a regression test when there is a correct seam.

A correct seam exercises the bug pattern as it happens in real use. Avoid false confidence from tests that only cover an internal helper when the failure requires a caller chain, state sequence, or integration boundary.

If no correct seam exists, document that as an architecture finding and recommend follow-up design work after the fix.

## Done Criteria

Before claiming the bug is fixed:

- Re-run the original feedback loop and report the result.
- Run the regression check, or state why no correct seam exists.
- Remove temporary `[DEBUG-...]` logs and throwaway debugging code.
- Explain the confirmed root cause and why the fix addresses it.
- State any remaining verification gaps honestly.
