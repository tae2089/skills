---
name: to-intent
description: Turn the current conversation into an `intent.md` — the Plan-stage proto-spec from the AI-native SDLC playbook — and save it to `.scratch/<feature-slug>/intent.md` after approval. No interview, just synthesis of what was already discussed. Use only when explicitly invoked; `to-spec` turns the intent into a spec.
disable-model-invocation: true
---

# To Intent

Write down what is wanted, why, and under which constraints, in the originator's own terms. The file is the first link in the chain `intent.md` → `spec.md` → `issues/`, all in one folder.

Do NOT interview the user — synthesize what the conversation already settled. When the plan is still fuzzy, go back to the `planning-grill` skill if available.

Format follows the Plan stage of Anthropic's [AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), with the edge-case and verification checks of [IntentSpec](https://intentspec.org/intent-md).

## Process

1. Pick the `<feature-slug>` — the same slug `to-spec` and `to-issues` will use, so all three files share `.scratch/<feature-slug>/`. If `intent.md` already exists there, read it: this run revises it.

2. Sort every settled point before drafting. Nothing settled is dropped:
   - **What, why, under which constraints** → the intent body.
   - **How to build it** — schema, interfaces, technology choices → `## Notes for spec`. Readers of the intent skip it; `to-spec` reads it, even from a fresh conversation.
   - **Not doing this time** → `## Out of scope`, one line each.

   If the conversation holds two or more problems that could each ship on its own, propose one intent per problem, each with its own `<feature-slug>`. Show the split in the approval preview; the user approves it or merges back into one.

3. Write the intent using the template below. Prose goes in the user's language; headings, commands, and paths stay verbatim.

4. Run the six checks below against the draft. Fill a failing check from the conversation when the answer is already there. Otherwise leave it failing and add the missing decision to `## Open questions`. Never invent an outcome, edge case, or check to make it pass.

5. Get approval before writing. Show:
   - every path, and whether each file is new or a revision of an existing one
   - the proposed split, when there is more than one intent
   - each check as pass or fail
   - every open question

   In a Git repository, first check that the path is not ignored. If it is, stop before writing and explain that the team cannot share the intent until the ignore rule changes. If the user does not approve, stop without writing anything.

6. Write `.scratch/<feature-slug>/intent.md` for each approved intent. The intent is always a local file, whatever `.scratch/.tracker` selects — it is reviewed and committed with the code. Do not commit it: committing is the product owner's review.

7. Report each path and any failing checks. Stop there. Hand off to `to-spec` only when the user explicitly asks for the spec.

## Template

<intent-template>

# Intent: <specific noun phrase>

**Author:** <who raised the need> · **Source:** <idea | ticket | incident, with a link when one exists>

## Problem

Who is affected and what concretely fails or becomes possible for them today.

## Proposed outcome

- At least two outcomes, one per line, each checkable on its own — a threshold, an observable capability, or a state change.

## Affected users and systems

Who uses it, who supports it, and which systems it touches.

## Constraints

- Statements an implementation can obey or break: "Never double-charge a card on retry", not "secure".

## Edge cases

- <scenario> → <expected behavior>

## Verification

- A check concrete enough to run without asking the author what they meant.

## Open questions

- Decisions still owed, each with who should answer.

## Out of scope

- What was discussed and deliberately left out this time.

## Notes for spec

- How-to decisions the conversation settled, for `to-spec`. Not checked; omit the section when there are none.

</intent-template>

## Checks

Judge each from the file's own text. These are heuristics; report them as such.

1. **Title** — a specific noun phrase of two or more words, not a placeholder ("Checkout payment retry", not "New feature").
2. **Problem** — names who is affected and what concretely fails; buzzwords with no number fail.
3. **Outcomes** — at least two, and at least two thirds of them a threshold, observable capability, or state change ("Payment completes in under 3 seconds at p95", not "Checkout feels faster").
4. **Constraints** — at least one statement an implementation can obey or break.
5. **Edge cases** — at least one scenario paired with its expected behavior.
6. **Verification** — at least one check concrete enough to run ("test it" fails).

## Completion

- Each approved intent exists at `.scratch/<feature-slug>/intent.md` and was written only after approval, or nothing was written and the reason was reported.
- Every settled point landed in the body, `## Notes for spec`, or `## Out of scope`.
- The report lists every failing check and every open question.
