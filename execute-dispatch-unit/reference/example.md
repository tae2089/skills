# Worked Example

End-to-end run of the Execution Loop for one dispatch packet. Use it as a shape, not a fixed answer.

## Received packet

```yaml
unit_id: W3
objective: "Add validation for missing project slug"
capability: implementer
allowed_scope:
  - "src/api/projects/*"
  - "tests/api/projects/*"
forbidden_scope:
  - "database migrations"
  - "frontend UI"
non_goals:
  - "Do not redesign project routing"
dependencies:
  - "W1 discovery summary: slug parsed in src/api/projects/handler.ts"
acceptance_criteria:
  - "Missing slug returns a typed validation error"
  - "Existing valid slug behavior remains unchanged"
verification:
  - "Run targeted project API tests if available"
return_contract: completion_report
```

## 1-3. Parse, confirm, identify boundaries

- Objective clear; W1 dependency output present (handler location known).
- Allowed: `src/api/projects/*`, `tests/api/projects/*`. Forbidden: migrations, frontend.
- Executable with provided context → proceed (no `BLOCKED`).

## 4. Perform only the assigned work

- Add a typed validation error for missing slug in `src/api/projects/handler.ts`.
- Add a test in `tests/api/projects/handler.test.ts` for missing slug.
- Discovered: routing has an unrelated rough edge → do NOT fix; record as follow-up.

## 5. Verify

- Run `tests/api/projects/` targeted suite. New test passes; existing slug tests still pass.

## 6. Completion report

```yaml
unit_id: W3
status: DONE
summary:
  - "Missing project slug now returns a typed ValidationError before handler logic"
  - "Existing valid-slug path unchanged"
changed_files:
  - "src/api/projects/handler.ts"
  - "tests/api/projects/handler.test.ts"
verification:
  attempted:
    - "targeted test run: tests/api/projects/"
  result: "pass"
  evidence:
    - "new missing-slug test passes; 12 existing project tests still pass"
blockers: []
follow_ups:
  - "Project routing has duplicated slug parsing in two handlers — candidate for a separate cleanup unit"
notes:
  - "Validation runs before auth side effects; no forbidden_scope touched"
```

## Blocked variant

If W1's discovery output were missing and the slug parse location were unknown, the objective's safe scope would be unclear:

```yaml
unit_id: W3
status: BLOCKED
blockers:
  - "Missing W1 discovery: cannot locate where slug is parsed without it; guessing risks editing outside intended scope"
```
