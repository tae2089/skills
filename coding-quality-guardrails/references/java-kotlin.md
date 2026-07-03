# Java/Kotlin Reference

Read this for Java or Kotlin code generation, review, refactoring, or test fixes.

## JVM Style

- Match the repository's framework, layering, package structure, naming, nullability style, logging, tests, and dependency choices.
- Follow the configured formatter and static analysis tools. If unknown, avoid formatting churn outside touched lines.
- Keep controllers, routes, and handlers thin. Put business logic in existing service, domain, or use-case layers.
- Prefer explicit domain types over stringly typed maps for meaningful data.
- Do not add dependencies casually. Prefer the JDK, Kotlin standard library, framework utilities, or existing dependencies.
- Do not add interfaces, abstract base classes, or extra layers for a single implementation. Introduce them only when a second implementation or a real seam exists.
- Keep Java and Kotlin interop intentional: verify nullability annotations, platform types, checked exceptions, visibility, and generated method names.
- Close `AutoCloseable`/`Closeable` resources deterministically with try-with-resources (Java) or `use { }` (Kotlin) rather than manual try/finally, so resources close and a close-time error does not mask the original failure.
- Do not expose internal mutable collections by reference; return read-only views (`Collections.unmodifiableList`, Kotlin `List`/`Map` interfaces) or defensive copies so callers cannot mutate hidden state.

## Java

- Use modern Java features only when supported by the project's configured source and target compatibility.
- Prefer immutable data shapes such as records or final fields when they match the existing style.
- Use `Optional` for return values when the project already uses it; do not use it for fields, parameters, or serialization models unless it is already the local convention.
- Avoid broad reflection, global singletons, and static mutable state unless the framework requires them.
- When overriding `equals`, always override `hashCode` (and usually `toString`) from the same significant fields, so equal objects share a hash code and hash-based collections behave.

## Kotlin

- Make nullability explicit and avoid `!!` except at proven framework boundaries with a short explanation.
- Prefer immutable `val` and read-only collection interfaces unless mutation is required.
- Use data classes, sealed classes, and extension functions when they clarify the domain and match local style.
- Avoid clever scope-function chains when straightforward code is easier to review.
- Keep coroutine code structured: do not use `GlobalScope`; propagate cancellation; use dispatcher choices already established by the project.
- Declare identity-bearing fields in a data class's primary constructor: `equals`/`hashCode`/`toString`/`copy` ignore body-declared properties. Keep invariants in `init` (which `copy()` runs); `copy()` bypasses validation placed only in factory functions or secondary constructors.
- Use `when` as an expression over sealed types and enums without an `else`, so adding a new subtype or constant becomes a compile error instead of silently hitting a catch-all.
- Remember declarations are `public` by default; mark implementation details `internal`/`private` rather than leaking them as API, and omit redundant `public`.
- When (de)serializing Kotlin types, register the Jackson Kotlin module and `FAIL_ON_NULL_FOR_PRIMITIVES`; otherwise missing or `null` JSON can be forced into a non-null property and surface as an NPE away from the boundary.

## Errors And Boundaries

- Preserve existing exception, result, and error-response conventions.
- Add context at service or boundary layers without swallowing causes.
- Do not log and rethrow the same failure unless the log adds operational context the caller will not provide.
- Do not leak secrets, tokens, credentials, or personal data into logs, exceptions, metrics, or API responses.
- Keep transaction, retry, and idempotency behavior explicit when touching persistence or external calls.
- Do not base entity `equals`/`hashCode` on a database-generated id; use a stable business key and keep the hash code constant across the persist lifecycle so the entity stays findable in a `Set` after saving.

## Tests

- Add or update focused tests for behavior changes using the project's test stack, such as JUnit, Kotest, Mockito, MockK, Spring test support, or Testcontainers.
- Prefer behavior tests at the right boundary over private implementation assertions.
- Mock external systems and expensive boundaries. Avoid mocking the code under test or framework wiring that the test is meant to verify.
- Cover nullability, validation, error mapping, persistence, and concurrency edge cases proportional to risk.
- Run the narrowest relevant test first, then broader checks when risk warrants it.
