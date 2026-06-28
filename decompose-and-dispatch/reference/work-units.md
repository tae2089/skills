# Work Units And Quality Gate

## Atomic Work Units

Make each work unit small enough that one executor can complete it independently and report a concrete output.

A good work unit has:

- A single objective.
- Clear inputs.
- Clear output.
- A bounded read or write scope.
- Explicit dependencies.
- A verification expectation when applicable.

Avoid units such as "implement the whole feature" or "review everything" unless the user's task is already that small. Split broad work by module, concern, artifact, or phase.

## Work Unit Quality Gate

Before dispatching, check every work unit:

- `objective`: Can the executor finish it without solving a different problem first?
- `scope`: Is the read or write area explicit enough to prevent drift?
- `ownership`: For write tasks, is the file, module, artifact, or responsibility boundary clear?
- `dependencies`: Are prerequisites listed by work-unit id?
- `output`: Is the expected return artifact concrete enough to integrate?
- `verification`: Is there a command, check, review criterion, or evidence expectation?
- `blast_radius`: Is the impact small, medium, or large?
- `conflict_risk`: Is overlapping work impossible, unlikely, or likely?

If a unit fails the gate, split it, narrow it, or keep it with the orchestrator until enough context exists.

Use this schema when precision matters:

```yaml
id: W1
objective: "Find where authentication state is stored"
capability: researcher
scope: "read-only repository search"
ownership: "authentication state discovery only"
inputs:
  - "current repository"
outputs:
  - "file references"
  - "short data-flow summary"
dependencies: []
parallelizable: true
risk: low
blast_radius: small
conflict_risk: unlikely
executor:
  selected: "main-agent"
  capability: researcher
  confidence: medium
  evidence:
    - "no dedicated research executor is available"
  fallback: "main-agent"
  needs_user_mapping: false
verification:
  expected: "file references are concrete and sufficient for implementation"
```
