# Deepening Reference

Use this when a shallow cluster should become a deeper module.

## Dependency Categories

- `in-process`: pure computation or in-memory state. Deepen directly and test through the new interface.
- `local-substitutable`: filesystem, database, or queue behavior with local stand-ins. Use the local stand-in in tests when it preserves the real behavior.
- `remote-owned`: internal services across a network boundary. Define a port at the seam; production gets HTTP/gRPC/queue adapters, tests get an in-memory adapter.
- `true-external`: third-party services. Inject a port and use a mock or fake adapter in tests.

## Seam Discipline

- One adapter usually means a hypothetical seam. Two adapters usually means a real seam.
- Keep internal seams private to the implementation when only the module's own tests need them.
- Do not expose internal seams just to make caller tests easier.

## Testing Strategy

- The module interface is the primary test surface.
- Tests should assert observable behavior, not internal state or call order.
- Once interface-level tests cover the behavior, delete obsolete tests that only pin shallow internal helpers.
- If no good test seam exists, treat that as design feedback.
