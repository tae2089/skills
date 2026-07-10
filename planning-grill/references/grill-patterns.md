# Planning Grill Patterns

Use these when a plan needs more structure than one or two clarifying questions.

## Decision Dimensions

Check the plan across these dimensions:

- **Goal**: the user-visible outcome and why it matters.
- **Scope**: what is included, what is explicitly out of scope, and which files
  or systems are likely affected.
- **Vocabulary**: terms that must be canonical before work starts.
- **Constraints**: compatibility, runtime state, artifact layout, permissions,
  safety, data, and release constraints.
- **Dependencies**: upstream decisions, task ordering, external services, and
  prerequisite artifacts.
- **Acceptance**: observable conditions that prove the work is complete.
- **Implementation detail**: the concrete decisions a worker would otherwise
  guess silently — data shapes, edge-case behavior, defaults, error and response
  formats, storage, config keys, boundary values. Pin any whose wrong guess is
  costly; mark a genuinely free choice as explicit worker latitude.
- **Failure Modes**: likely ways the plan can fail, drift, or be misinterpreted.
- **Handoff**: which skill or worker consumes the plan next.

## Example Probe

The Probe Format template and its rules live in SKILL.md (Question Discipline).
A worked example:

```md
Current understanding: add rate limiting to the public API without breaking existing clients.
Blocked decision: limit key — per-IP vs per-API-key changes middleware shape and the test matrix.
Recommended answer: per-API-key with a per-IP fallback for unauthenticated routes (if wrong: authed clients sharing an IP throttle each other).
Question: should the limit be keyed on the API key rather than the source IP?
```

## Decision Log Pattern

Format for the decision recorded in Workflow step 5:

```markdown
- Decision: limit keyed on API key, per-IP fallback for unauthenticated routes.
  Reason: authed clients behind shared NAT must not throttle each other.
  Impacts: middleware reads the key first; test matrix needs a shared-IP case.
```

## Stop Conditions

In-loop signals that it is time to stop probing and move to the Completion gate
in SKILL.md — stop asking further questions when:

- the remaining unknowns are implementation details left to explicit worker latitude
- further questions would not change task boundaries or acceptance criteria
- unresolved risks are already recorded and acceptable
