# Go Reference

Read this for Go code generation, review, refactoring, or test fixes.

## Go Style

- Format with `gofmt` or `go fmt`.
- Match existing package structure, naming, error handling, logging, tests, and dependency choices.
- Keep `cmd/` thin. Put business logic in existing internal/domain packages.
- Use clear package-level names and avoid stutter.
- Prefer concrete types internally. Keep interfaces small and consumer-owned.
- Do not create an interface just because one implementation exists.
- Accept `context.Context` as the first parameter for context-aware functions.
- Do not store `context.Context` in structs.
- Avoid package-level mutable state; inject dependencies through constructors.
- Do not add dependencies casually. Prefer the standard library or existing dependencies.

## Errors

- Always check returned errors.
- Return errors instead of panicking except for unrecoverable initialization failures.
- Add context near the failing operation and wrap inspectable causes with `%w`.
- Keep error messages lowercase and without trailing punctuation.
- Do not log and return the same error unless the log adds operational value the caller will not provide.
- Use sentinel or typed errors only when callers need programmatic branching.

## Concurrency

- Do not introduce goroutines unless there is a clear latency, throughput, or isolation need.
- Every goroutine must have a bounded lifetime or cancellation path.
- Protect shared mutable state with mutexes or channel ownership. Make ownership obvious.
- Avoid time-based synchronization in tests; use channels, contexts, fakes, or explicit hooks.

## Tests

- Add or update focused tests for behavior changes.
- Prefer externally observable behavior over private implementation details.
- Use table-driven tests when they improve readability.
- Use `t.Helper()` in helpers and `t.TempDir()` for temporary files.
- Avoid sleeps in tests. If unavoidable, keep them tiny and explain why.
- Run the narrowest relevant package test first, then broader tests when risk warrants it.

