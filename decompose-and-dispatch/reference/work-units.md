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
- A required executor spec, authored before checking what executors exist.

Avoid units such as "implement the whole feature" or "review everything" unless the user's task is already that small. Split broad work by module, concern, artifact, or phase.

## Work Unit Quality Gate

Before dispatching, check every work unit:

- `objective`: Can the executor finish it without solving a different problem first?
- `scope`: Is the read or write area explicit enough to prevent drift?
- `ownership`: For write tasks, is the file, module, artifact, or responsibility boundary clear?
- `spec`: Does the required executor spec state role, permissions, and needed context — not just a capability class?
- `dependencies`: Are prerequisites listed by work-unit id?
- `output`: Is the expected return artifact concrete enough to integrate?
- `verification`: Is there a command, check, review criterion, or evidence expectation?
- `blast_radius`: Is the impact small, medium, or large?
- `conflict_risk`: Is overlapping work impossible, unlikely, or likely?

If a unit fails the gate, split it, narrow it, or keep it with the orchestrator until enough context exists. Units created by a split get their own specs and resolutions — re-run those steps for them before dispatching.

## Required Executor Spec

Author the spec from the unit's needs, before and independent of the runtime inventory. The spec is what gets resolved (see `matching.md`) and what seeds the handoff prompt. Units with identical needs may share one spec; resolution is still recorded per unit.

- `role`: one line, usable verbatim as an agent preamble when instantiating.
- `capability`: one portable capability class, as shorthand.
- `tools`: what the executor must be able to do, described at capability level ("repository search", "run tests") — not runtime-specific tool names.
- `permissions`: `file_access` (`read-only` | `write-scoped` | `none`), `network` (`none` | `fetch` | `full`), `execution` (`none` | `commands`).
- `context`: inputs the executor must receive to work self-contained.
- `model_hint` (optional): `default` | `fast` | `strong` — only when the unit clearly warrants it.
- `verification`: the evidence the executor must return.

## Full Schema

Use this schema when precision matters:

```yaml
id: W1
objective: "Find where authentication state is stored"
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
required_executor_spec:
  role: "You are a read-only code researcher. You locate code and report references; you never edit files."
  capability: researcher
  tools:
    - "repository search"
    - "file read"
  permissions:
    file_access: read-only
    network: none
    execution: none
  context:
    - "the question to answer and the modules already suspected"
  verification: "file references concrete enough to implement against"
resolution:
  method: main-agent          # existing | instantiated | main-agent
  executor: "main-agent"
  confidence: medium
  evidence:
    - "no named executor satisfies the spec and instantiation is unavailable"
  unsatisfied: []             # spec requirements the selected executor cannot meet
  needs_user_mapping: false
```
