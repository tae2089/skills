# False-positive Patterns

Use this file to suppress or downgrade repeated AI review mistakes. Keep only portable pattern classes in this global file.

Store repo-specific suppressions inside the reviewed repository. Examples:

- `.github/review-suppressions.md`
- `docs/review-suppressions.md`
- a clearly named section in `AGENTS.md`

When repo-local suppressions exist, merge them with these global patterns and include only relevant suppressions in reviewer prompts.

## Configuration And Operational Contracts

- Treat roles, modes, features, and integrations explicitly set by startup flags, environment variables, config files, or deployment manifests as repeated false-positive candidates.
- Use the "Operator Error vs Code Defect" section in `severity-rubric.md` as the source of truth for whether these are code defects or operator/configuration feedback.

## Generated Or Mechanical Files

- Do not review generated files for style or hand-written maintainability unless the generated file is checked in as the source of truth and the generator is out of scope.
- Prefer reviewing the schema, generator input, or generation command over generated output itself.

## Compatibility Shims

- Do not suggest removing compatibility code unless the PR explicitly removes the compatibility contract.
- Treat awkward naming or duplicated paths in compatibility layers as intentional unless docs or tests say otherwise.

## Existing Local Convention

- Do not raise findings for patterns that match nearby code and do not create a new correctness risk.
- Suggest broader cleanup only as a non-blocking follow-up.

## Weak-evidence Severity Escalation

- Do not assign P1 merely because a path is theoretically possible.
- Escalate only when the path is supported, normal, documented, or directly implied by tests and product behavior.
