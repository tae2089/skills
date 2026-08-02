---
name: to-issues
description: Break a plan, spec, or the current conversation into tracer-bullet issues with blocking edges, then publish them through the shared `.scratch/.tracker` configuration or as shared local Markdown tickets. Use only when explicitly invoked.
disable-model-invocation: true
---

# To Issues

Break a plan, spec, or conversation into a set of **issues** — tracer-bullet vertical slices, each declaring the issues that **block** it.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** issues.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests) — vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges** — the other issues that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change — rename a column, retype a shared symbol — whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket — green is promised only there.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other issues (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct — does each ticket only depend on issues that genuinely gate it?
- Should any issues be merged or split further?

Iterate until the user approves the breakdown.

### 5. Select the publication destination

Read [the tracker configuration](references/tracker-config.md), then read `.scratch/.tracker` when it exists. Never infer a tracker from the git remote.

- **Credentials in the configuration** → stop without writing anything. Name the unsafe key only; never print its value.
- **Missing configuration** → select local Markdown. The approval preview must say it will also create `.scratch/.tracker` with `provider: local`.
- **`provider: local`** → select local Markdown.
- **Valid `github`, `gitlab`, or `jira` configuration** → use its exact `target` only when the matching tool is available and authenticated.
- **Malformed configuration, unsupported provider, missing remote target, or unavailable tool** → explain why remote publication stopped, preserve the existing configuration, and select local Markdown.

Before selecting local Markdown, verify that `.scratch/.tracker` and `.scratch/<feature-slug>/issues/` can be tracked by Git. If either path is ignored, stop and explain that the team cannot share the tickets until the ignore rule changes.

### 6. Confirm the write

Show the selected provider and destination, parent issue when one exists, ticket count, titles, and dependency order. If local Markdown is a fallback, show the reason and the `.scratch/<feature-slug>/issues/` path.

Get the user's approval before the first configuration write, local ticket write, or remote publication. Approval of the breakdown in step 4 does not approve this write. If the user does not approve, stop without writing anything.

### 7. Publish the issues

- **Local Markdown** → when the configuration was missing, first write `.scratch/.tracker` with only `provider: local`. Then write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order. Each file's "Blocked by" lists the numbers/titles it depends on. Use the per-ticket file template below — one ticket per file, never a combined file.
- **Remote tracker** → publish one issue per ticket in dependency order so later blocking edges can use real identifiers. Use native parent and blocking relationships when the selected tool supports them; otherwise keep those references in the issue body. Apply `ready-label` only when the configuration contains it; never assume or create a label.

If a write or publication fails, stop and report what was created plus the failure. After any remote ticket exists, never create local copies as a fallback.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

<local-ticket-template>

# <NN> — <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective — not a layer-by-layer implementation list.

**Blocked by:** the numbers/titles of the issues that gate this one, or "None — can start immediately".

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective — not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None — can start immediately".

</issue-template>

In either form, avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

When `ready-label` is configured, add `**Status:** <ready-label>` to local tickets and the matching label to remote tickets. Otherwise omit status and labels.

Done when every approved ticket has a local path or remote identifier, every blocking edge points to a created ticket, and any missing native link or label is reported. Do NOT close or otherwise modify a parent issue.
