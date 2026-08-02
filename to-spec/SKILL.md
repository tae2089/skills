---
name: to-spec
description: Turn the current conversation into a spec and publish it to the issue tracker configured in `.scratch/.tracker` — no interview, just synthesis of what you've already discussed. Writes the spec only; `to-issues` breaks it into tickets.
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec (you may know this document as a PRD). Do NOT interview the user — just synthesize what you already know.

The publication destination and the triage label come from `.scratch/.tracker` — the shared project file described in [the tracker configuration](../to-issues/references/tracker-config.md). Read it in step 4; never infer a tracker from the git remote, and never ask for a credential.

Adapted from Matt Pocock's `to-spec` skill in `mattpocock/skills`.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Check with the user that these seams match their expectations.

3. Write the spec using the template below. The spec is one document — do not split it into a work breakdown here. That is `to-issues`' job.

4. Select the publication destination, then get approval before writing anything.

Read [the tracker configuration](../to-issues/references/tracker-config.md), then read `.scratch/.tracker` when it exists.

- **Credentials in the configuration** → stop without writing anything. Name the unsafe key only; never print its value.
- **Missing configuration** → publish locally. The approval preview must say it will also create `.scratch/.tracker` with `provider: local`.
- **`provider: local`** → publish locally.
- **Valid `github`, `gitlab`, or `jira` configuration** → use its exact `target`, and only when the matching tool is available and already authenticated.
- **`provider: jira` with `spec-target`** → the spec becomes a Confluence page and one normal Jira issue links it. Follow "Jira with Confluence" in the tracker configuration.
- **Malformed configuration, unsupported provider, missing remote target, or unavailable tool** → explain why remote publication stopped, preserve the existing configuration, and publish locally.

Show the provider and every object you will create, so nothing team-visible appears unannounced. For Jira with Confluence that is the seed page when one is missing, the spec page and the page it goes under, and the Jira project plus the issue type — the project's default standard type, never an epic. Otherwise it is the destination and the spec title. Always show the label you will apply, and the reason when local is a fallback.

Get the user's approval before the first configuration write or publication — the seam check in step 2 does not approve this write. If the user does not approve, stop without writing anything.

5. Publish the spec.

- **Remote tracker** → create one issue holding the whole spec.
- **Jira with `spec-target`** → the three ordered writes in "Jira with Confluence": the seed page when one is missing, then the spec page under it, then one parent issue at the project's default standard type whose description links that page. Stop at the first failure and report what already exists.
- **Local** → when the configuration was missing, first write `.scratch/.tracker` with only `provider: local`. Then write the spec to `.scratch/<feature-slug>/spec.md`.

Apply the configured `ready-label` — on a remote issue as the tracker's own label, on a Confluence page as a page label when the connected tool supports one, in `spec.md` as a `**Status:** <ready-label>` line under the title. With no `ready-label` key, apply no label and no status line. Never create a label that does not exist, and no further triage is needed.

Before publishing locally in a Git repository, check that neither `.scratch/.tracker` nor `.scratch/<feature-slug>/spec.md` is ignored. If either is, stop before writing and explain that the team cannot share the spec until the ignore rule changes.

`<feature-slug>` is the same slug `to-issues` uses, so the spec and its tickets share one folder — `.scratch/<feature-slug>/spec.md` beside `.scratch/<feature-slug>/issues/`.

If a publication fails, stop and report what was created plus the failure. Once a remote issue exists, never write a local copy as a fallback.

6. Report where the spec landed. Stop there. Hand the spec to `to-issues` only when the user explicitly asks for the work breakdown.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>

Write the spec's prose in the user's language — the spec is read by people. Section headings, commands, and file paths stay verbatim; they are searchable strings, not prose.
