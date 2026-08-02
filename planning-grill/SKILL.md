---
name: planning-grill
description: Grill a fuzzy plan, decision, or idea into a shared understanding before execution — one question at a time, each with a recommended answer and the cost of being wrong. Use when scope, acceptance criteria, or failure modes are unclear, or when the user asks to stress-test their thinking. Skip concrete plans that already have testable acceptance criteria.
---

# Planning Grill

Interview the user relentlessly about every part of this until you reach a shared
understanding. Walk down each branch of the decision tree, resolving dependencies
between decisions one at a time.

Ask one question per turn and wait for the answer. Several at once is bewildering.

If a *fact* can be found in the environment — filesystem, code, docs, command
output — look it up instead of asking. The *decisions* are the user's: put each
one to them and wait.

For every question give your recommended answer and what goes wrong if it is wrong:

    Recommended: per-API-key, with a per-IP fallback for unauthenticated routes.
    If wrong: authed clients behind one shared IP throttle each other.

Stop asking once the remaining answers would not change scope, acceptance
criteria, or task boundaries.

Do not act until the user confirms the shared understanding. This skill writes no
files. When the plan should outlive this conversation, hand off to `to-spec`.
