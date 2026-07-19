---
name: overengineering-review
description: Review a code change for unnecessary abstractions, duplicated durable policy, compatibility cascades, oversized integration-test matrices, and scope expansion. Use during implementation when one new abstraction causes three or more follow-up regressions, or after tests are green and before commit when a change adds persisted fields, interface methods, lifecycle states, compatibility branches, destructive-operation safeguards, or substantially more test code than production code; keep the review read-only unless simplification is explicitly requested.
---

# Overengineering Review

Classify complexity by the contract it protects. Prefer the smallest design that preserves correctness, security, data integrity, authorization, error semantics, and destructive-operation safety.

## Workflow

1. Reconstruct the scope.
   - State the original contract and each directly reproduced defect.
   - Include only regressions caused by the fix itself; label unrelated hardening as scope expansion.
   - Identify the diff base and list changed production and test files.

2. Inventory material added concepts.
   - List new interface methods, persisted fields, lifecycle states, adapters, compatibility branches, external dependencies, and helpers that centralize domain policy.
   - Group low-risk local and test helpers instead of enumerating each one.
   - Rank candidates by destructive risk, persistence impact, public surface, duplicated policy, and maintenance cost. Deep-review the top three by default; group the remainder as not individually reviewed unless the user requests an exhaustive audit.
   - For each concept, name the current requirement that needs it and why an existing shape cannot satisfy that requirement.
   - Apply this ladder: need it, existing pattern, standard library, native platform, installed dependency, one local helper, minimum new code.

3. Check durable authority and duplication.
   - Declare one authoritative source for every durable identity and state.
   - Treat duplicated fields as derived projections unless an explicit threat model requires independent validation.
   - Flag pairwise reconciliation, migration, or compatibility logic created only because authority is ambiguous.
   - Keep duplicated validation when it independently prevents authorization bypass, data loss, or deletion of a foreign resource.

4. Detect patch cascades.
   - Trace follow-up fixes back to the abstraction or compatibility behavior that caused them.
   - If one new abstraction causes three or more follow-up regressions, stop adding branches and compare at least two simpler designs.
   - Reject another branch unless evidence shows both simpler designs violate a required contract.

5. Audit test layering.
   - Put exhaustive field and state combinations in pure validator or unit tests.
   - Use integration tests for distinct seams and observable lifecycle paths, not the Cartesian product of backend, field, state, and operation when behavior is identical.
   - Preserve every security and data-integrity boundary while consolidating repeated setup with focused fixtures or tables.
   - Calculate added production and test lines separately. When test additions exceed twice production additions, require a simplification review; never treat the ratio as automatic failure.

6. Compare the smallest viable alternative.
   - Describe the current design and at least one smaller design that preserves the same invariants.
   - Compare interface size, branches, durable fields, failure behavior, compatibility burden, test surface, and expected deletion.
   - Prefer clear duplication over a speculative shared abstraction, but prefer one helper when it removes duplicated domain policy.

7. Classify each candidate.
   - `required`: removing it weakens a verified contract or safeguard.
   - `simplify`: behavior is required but structure or test setup is duplicated.
   - `remove`: behavior is speculative, unrelated, or already guaranteed elsewhere.
   - `insufficient evidence`: the alleged simplification has not been shown to preserve the contract.

## Hard Boundaries

- Keep the review read-only unless the user explicitly asks to implement simplifications.
- Never weaken security, authorization, persistence, cleanup ownership, destructive-operation validation, or test assertions merely to reduce line count.
- Never classify code from line count alone.
- Never add an abstraction solely to remove repeated lines.
- Never replace real local behavior with mocks to make the test suite smaller.
- Treat missing design context as unknown, not as proof that a constraint does not exist.

## Output

Report in this order:

1. Overall judgment: required complexity, simplification opportunity, removable behavior, and review coverage.
2. Up to three findings ordered by expected maintenance cost, each with file and line evidence, unless the user requested an exhaustive audit.
3. The protected invariant and the smaller design for every `simplify` or `remove` item.
4. Estimated production and test lines that can be removed without reducing coverage.
5. Safeguards explicitly retained.
6. Verification and unavailable evidence.

## Completion Criteria

- The top three material candidates are classified; remaining concepts are grouped and explicitly listed as not individually reviewed.
- Every simplification preserves named invariants and observable behavior.
- Exhaustive combinations and integration seams are assigned to the correct test layer.
- Patch cascades are counted and trigger redesign at three follow-up regressions.
- Production and test diff sizes are reported separately when available.
- No recommendation relies only on aesthetics, preference, or line count.
