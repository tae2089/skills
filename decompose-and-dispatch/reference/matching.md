# Spec Resolution And Runtime Discovery

## Runtime Discovery Checklist

Use the discovery methods that exist in the current environment. Do not fail the plan just because one method is unavailable.

Check, when available:

- User-provided executor mappings in the prompt or project instructions.
- Runtime-visible agent, worker, subtask, or thread tools.
- Whether the runtime can spawn arbitrary-prompt subagents (a general-purpose delegation mechanism) — this decides if the `instantiated` rung of the ladder exists.
- Local or project agent configuration files.
- Tool and connector lists that imply operator, tester, researcher, or implementer capabilities.
- Sandbox, approval, network, and write permissions.
- Existing plan, task, issue, or run state that already assigns ownership.

Record the discovery source in the resolution evidence. If the runtime cannot expose executor metadata, write `unknown` rather than guessing.

## Spec Satisfaction Check

Resolution starts from the unit's required executor spec, not from the executor list. For each named executor considered, ask: does the evidence show it can satisfy the spec's role, tools, and permissions?

Do not infer capability from executor name alone. Weigh evidence in this order:

1. Explicit user-provided mapping.
2. Runtime-provided executor metadata.
3. Agent description, system prompt, or developer instructions.
4. Tool access, permissions, sandbox mode, write capability, network access, and connector access.
5. Naming hints as weak evidence only.

An executor satisfies a spec when its evidenced tools and permissions cover the spec's requirements and its role does not conflict (e.g. a read-only explorer cannot satisfy a `write-scoped` implementer spec; a write-capable builder can satisfy a read-only research spec but a narrower read-only executor is safer). Record any requirement the executor cannot meet under `unsatisfied` — a non-empty list means it does not satisfy the spec. In a final plan, `unsatisfied` may stay non-empty only on a `main-agent` fallback or a user-confirmed mapping, where it documents the accepted gap.

## Resolution Ladder

Resolve each spec in this order:

1. **`existing`** — a named executor satisfies the spec. Prefer this rung when the fit is real: curated executors carry tuned prompts and tool restrictions that an ad-hoc spec will not replicate. When multiple executors satisfy the spec:
   - Prefer the narrowest one whose permissions still cover the spec (least privilege).
   - Prefer specialists for read-only research, review, or domain analysis.
   - Avoid assigning two write-capable executors to overlapping files or modules.
2. **`instantiated`** — nothing satisfies the spec, but the runtime supports arbitrary-prompt subagents that can carry the spec's tools and permissions (a subagent that cannot run commands cannot serve an `execution: commands` spec — treat instantiation as unavailable for that spec). Instantiate from the spec:
   - Ephemeral only: the spec's `role` line plus its permission constraints become a preamble in the handoff prompt (see `dispatch-format.md`). Do not create persistent agent definition files unless the user explicitly asks.
   - Enforce the spec's permissions in the prompt ("you are read-only; do not edit files") and, when the runtime supports it, in the spawn configuration. Apply the spec's `model_hint` at spawn when the runtime supports model selection; otherwise ignore it.
   - Instantiation resolves ambiguity: when it is unclear whether a named executor satisfies the spec, instantiating a known-good executor beats delegating to an uncertain one.
3. **`main-agent`** — delegation is not allowed (see the definition in `SKILL.md`), or no available mechanism can satisfy the spec. Keep the unit on the main agent. Preserve the spec in the plan: it still drives sequencing, scope, and verification.

Keep orchestration, cross-cutting integration, and final decisions with the main agent unless the user explicitly requests another orchestration model.

Record confidence for each resolution:

- `high`: strong description, metadata, or tool evidence that the spec is satisfied — or an instantiated executor whose preamble fully encodes the spec.
- `medium`: plausible fit with partial evidence, or an instantiated executor whose spec needs context the orchestrator may not fully possess.
- `low`: weak name-based or inferred fit.

Set `needs_user_mapping: true` only when all hold: the runtime offers named executors but cannot instantiate, spec satisfaction is ambiguous (`low` confidence), and the unit would edit files, consume meaningful budget, or affect external systems. When instantiation is available, instantiate instead of asking.

## Runtime Adapter Notes

Use these as examples of what may satisfy each capability's specs, not as fixed mappings:

| Portable Capability | Example Runtime Mapping |
| --- | --- |
| `researcher` | explorer, search agent, read-only worker, repo-reader, instantiated subagent, main agent |
| `implementer` | worker, coding agent, patch agent, builder, instantiated subagent, main agent |
| `tester` | worker, shell runner, CI agent, QA agent, instantiated subagent, main agent |
| `reviewer` | reviewer, critic, security reviewer, code review agent, instantiated subagent, main agent |
| `specialist` | security agent, frontend expert, data agent, framework-specific agent, instantiated subagent, main agent |
| `operator` | browser agent, MCP operator, cloud agent, app-control agent, main agent |
| `documenter` | docs agent, tech writer, spec writer, instantiated subagent, main agent |
| `orchestrator` | main agent, lead agent, planner, coordinator |

If local custom agent names are opaque, read their descriptions or instructions before checking satisfaction. For example, an executor named `blueprint` may satisfy a planner or researcher spec if its description says it explores architecture and writes plans. An executor named `knife` may satisfy an implementer spec if its description says it makes minimal code edits.
