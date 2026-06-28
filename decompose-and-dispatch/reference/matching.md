# Executor Matching And Runtime Discovery

## Runtime Discovery Checklist

Use the discovery methods that exist in the current environment. Do not fail the plan just because one method is unavailable.

Check, when available:

- User-provided executor mappings in the prompt or project instructions.
- Runtime-visible agent, worker, subtask, or thread tools.
- Local or project agent configuration files.
- Tool and connector lists that imply operator, tester, researcher, or implementer capabilities.
- Sandbox, approval, network, and write permissions.
- Existing plan, task, issue, or run state that already assigns ownership.

Record the discovery source in the mapping evidence. If the runtime cannot expose executor metadata, write `unknown` rather than guessing.

## Executor Matching

Do not infer capability from executor name alone.

Match executors by evidence in this order:

1. Explicit user-provided mapping.
2. Runtime-provided executor metadata.
3. Agent description, system prompt, or developer instructions.
4. Tool access, permissions, sandbox mode, write capability, network access, and connector access.
5. Naming hints as weak evidence only.

When multiple executors fit:

- Prefer the narrowest specialist for read-only research, review, or domain analysis.
- Prefer implementers for bounded edits with clear ownership.
- Prefer testers for independent reproduction or verification work.
- Keep orchestration, cross-cutting integration, and final decisions with the main agent unless the user explicitly requests another orchestration model.
- Avoid assigning two write-capable executors to overlapping files or modules.

Record confidence for each mapping:

- `high`: strong description, metadata, or tool evidence.
- `medium`: plausible fit with partial evidence.
- `low`: weak name-based or inferred fit.

If confidence is low, assign `main-agent` as fallback and set `needs_user_mapping: true` when delegation would edit files, consume meaningful budget, or affect external systems.

## Runtime Adapter Notes

Use these as examples, not as fixed mappings:

| Portable Capability | Example Runtime Mapping |
| --- | --- |
| `researcher` | explorer, search agent, read-only worker, repo-reader, main agent |
| `implementer` | worker, coding agent, patch agent, builder, main agent |
| `tester` | worker, shell runner, CI agent, QA agent, main agent |
| `reviewer` | reviewer, critic, security reviewer, code review agent, main agent |
| `operator` | browser agent, MCP operator, cloud agent, app-control agent, main agent |
| `documenter` | docs agent, tech writer, spec writer, main agent |
| `orchestrator` | main agent, lead agent, planner, coordinator |

If local custom agent names are opaque, read their descriptions or instructions before mapping. For example, an executor named `blueprint` may be a planner or researcher if its description says it explores architecture and writes plans. An executor named `knife` may be an implementer if its description says it makes minimal code edits.

## Host Adapter Config

The `agents/` directory holds host-specific UI metadata for surfacing this skill.

- `agents/openai.yaml` — Codex app UI metadata: `display_name`, `short_description`, and a `default_prompt` that invokes the skill via Codex's `$skill` syntax.

This is host-runtime configuration, not portable capability semantics. Other hosts add their own files here as needed.
