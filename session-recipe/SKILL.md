---
name: session-recipe
description: Set up and verify ground-truth session recording, distill a finished session into a replayable recipe of dispatch packets, and replay a saved recipe step by step. Use when the user asks to record a session, turn completed work into a recipe, replay a recipe.yaml, or set up session-recording hooks.
---

# Session Recipe

Turn a real working session into a replayable recipe. A recipe is an ordered list of dispatch packets — the packet format `execute-dispatch-unit` consumes, i.e. the executable form of a `decompose-and-dispatch` work unit — where each packet carries a `provenance` block of evidence from the session that originally produced it.

The pipeline is: prompt → recorded actions → touched files → checkpoints → verification → recipe. Recording captures ground truth, distillation compresses it into intent, replay re-executes the intent.

Pick exactly one mode per invocation.

## Mode: Record

Recording is passive; this mode only sets up or checks it.

1. Recording is provided by the standalone `session-recorder` hook tool, managed outside this repository — locate the installed copy from the host's registered hook command (e.g. the `hooks` entries in Claude Code's `settings.json`, Codex's `.codex/hooks.json`, or Antigravity's `~/.gemini/antigravity-cli/hooks.json`); its `README.md`, kept alongside the script, covers installation for Claude Code, Codex, and Antigravity (agy). If it is not installed anywhere, or the host has no lifecycle-hook mechanism, recording is unavailable — say so and rely on step 3's fallback.
2. Verify recording works: the current session's log is `_workspace/session-logs/<session-id>.jsonl` at the repository root (non-repo working directories fall back to `~/.session-recipe/logs/<cwd-slug>/` — full resolution rules in the recorder README) — confirm its latest `prompt` record matches this conversation and that recent writes appear as `action` records. On a fresh install, a just-registered hook may not have fired yet: submit a fresh prompt or restart the session (see the recorder README's verification notes) before concluding recording is broken.
3. Report the log path. If the hook cannot be installed, say so; distillation then falls back to lower-evidence sources and must label provenance `unverified`.

## Mode: Distill

1. Fix the recipe scope: which session(s) and which task. Ask only if the current session does not identify it.
2. Collect evidence in the priority order defined in `references/distillation.md` (higher wins on conflict). To locate action logs: `_workspace/session-logs/<session-id>.jsonl` at the repo root (all of a session's in-repo work lands in one file). Sessions in non-repo directories, and sessions recorded before the project-local layout, live under the recorder README's fallback and legacy roots — glob `<root>/*/<session-id>.jsonl` there and merge by session id, confirming `prompt` records match the work being distilled.
3. Group log events into work units and derive packet fields per `references/distillation.md`.
4. Write the recipe per `references/recipe-format.md` to `_workspace/<task-name>/recipe.yaml`, or to a tracked path the user names.
5. Validate before finishing: every step has every packet field listed in `references/recipe-format.md` (`unit_id` through `return_contract`) plus `provenance`; `dependencies` reference earlier steps only; `replay.order` covers every step id; no provenance field contains a secret value.

## Mode: Replay

1. Parse the recipe and check preconditions:
   - `environment`: confirm each entry with the cheapest mechanical probe (version command, `printenv <NAME>`, context check); an entry that cannot be mechanically checked is reported as unverified, not assumed satisfied. An unsatisfied entry blocks replay — report it and stop unless the user explicitly accepts proceeding without it.
   - Drift: run `git diff --stat <base_commit>..HEAD` passing each step's `allowed_scope` patterns as git pathspecs (`-- <pattern>`). Report drift; drift alone never blocks replay and never changes `replay.mode` — heavy drift inside a step's scope just predicts that an `exact` cherry-pick will fall back per step 3.
2. Execute steps in `replay.order`. Treat each step as a dispatch packet: use the `execute-dispatch-unit` skill if available, otherwise apply its boundary rules directly (edit only `allowed_scope`, run the packet's `verification`, report per-step status).
3. `replay.mode: exact` additionally cherry-picks the step's `provenance.commits` instead of re-implementing; fall back to intent replay per step when a cherry-pick does not apply cleanly, and say so.
4. Stop at the first `BLOCKED` or `FAILED` step and report; do not improvise past a broken step.
5. Finish with a per-step status table (step id, status, verification result) plus any deviations from the original provenance.

## Completion Criteria

- Record: the log path was reported and a real record was observed; or recording is installed but unconfirmed pending a fresh prompt/restart and that was reported; or the missing-hook fallback was stated.
- Distill: the recipe file exists, passed the step-5 validation, and every step reconstructed from memory carries `confidence: unverified`.
- Replay: every executed step has a completion status backed by its packet verification, and unexecuted steps are listed with the blocking reason.

## Reference Files

- `references/recipe-format.md` — recipe YAML schema and field semantics.
- `references/distillation.md` — event grouping, packet-field derivation, checkpoint mapping, honesty rules.
- `examples/recipe.example.yaml` — a small two-step recipe.
- `session-recorder` README (managed outside this repository, alongside the hook script the host's hook config invokes) — the standalone recorder this skill consumes: record-format contract, prerequisites, per-host installation, troubleshooting.
