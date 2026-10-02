---
name: setup-sdlc
description: Prepare a project for the `planning-grill` → `to-intent` → `to-spec` → `to-issues` → plan chain — the managed routing block in `AGENTS.md`, `.scratch/.tracker`, ignore rules for `.scratch/`, and plan storage. Safe to re-run; it refreshes only what it owns. Use only when explicitly invoked.
disable-model-invocation: true
---

# Setup SDLC

Do every check first, show every change in one preview, write only after approval. Never commit.

The project prompt file is `AGENTS.md`, or the file the project's runtime reads instead when the project already uses another name.

## Process

1. **Tracker.** Read [the tracker configuration](../to-issues/references/tracker-config.md), then `.scratch/.tracker` when it exists.
   - **Valid** → keep it and show it.
   - **Malformed or holding a credential** → report it without echoing any value, leave it untouched, and skip this step.
   - **Missing** → ask for the provider, defaulting to `local`. For a remote provider ask for `target`; for `jira` also offer `spec-target`. Check that the matching tool is connected and already authenticated; never start a login or ask for a secret. When it is not ready, say so — `to-spec` will fall back to local at publish time — and still plan the chosen configuration.

2. **Ignore rules.** In a Git repository, run `git check-ignore -v` on `.scratch/.tracker` and on probe paths for `intent.md`, `spec.md`, `issues/`, `plan.md`, and `plans/` under `.scratch/<probe>/`. For each ignored path, plan negation lines (`!…`) appended to the file holding the matching rule. Never delete an existing line. Outside Git, skip this step and say so.

3. **Routing block.** The block is [assets/agents-block.md](assets/agents-block.md), from `<!-- skills:begin -->` to `<!-- skills:end -->`. Everything outside the markers belongs to the team.
   - **No project prompt file** → plan a new file: a `# Project Guidance` title, the block, then an empty `## Project Notes` section.
   - **Exactly one pair of markers** → plan replacing the inside, or nothing when it is already identical.
   - **One marker, or more than one pair** → report the broken markers and skip this step.
   - **No markers** → plan appending the block at the end. List the existing lines outside it that cover the same topics, so the team can remove duplicates themselves.

4. **Plan storage (Claude Code only).** In other runtimes skip this step and say so. Read `.claude/settings.json`.
   - **Invalid JSON** → report it and skip this step.
   - **No `plansDirectory`** → plan adding `"plansDirectory": ".scratch/plans"` and nothing else.
   - **Another value** → report it and leave it.

5. **Preview.** If nothing is planned, report that the project is already set up and stop. Otherwise show every file, whether it is created or changed, and the exact lines added or replaced, plus every skipped step with its reason. If the user does not approve, stop without writing anything.

6. **Write** in this order, so later files land in trackable paths: ignore rules, `.scratch/.tracker`, the project prompt file, `.claude/settings.json`. If a write fails, stop and report which files were written and which were not.

7. **Verify.** Re-run step 2's `git check-ignore -v` probes. If a path is still ignored — a parent directory excluded so the negation cannot re-include it — report the blocking rule and stop.

8. **Report** the changed files, the skipped steps, and that the team still has to add `## Policy Skills` outside the block if it has policy skills. Do not commit.

## Completion

- Nothing was written before approval, and nothing outside the markers of an existing project prompt file changed.
- Every probe path passes `git check-ignore`, or the blocking rule was reported.
- Every skipped step is reported with its reason.
- Running the skill again plans no changes.
