# TypeScript Reference

Read this for TypeScript code generation, review, refactoring, or test fixes.

## TypeScript Style

- Match the repository's framework, module boundaries, naming, typing strictness, lint rules, formatter, tests, and dependency choices.
- Preserve existing runtime targets, module format, bundler assumptions, and path alias conventions.
- Prefer precise, readable types over clever generic gymnastics.
- Avoid `any` except at genuinely dynamic boundaries; validate or normalize unknown data into typed shapes quickly.
- Avoid non-null assertions (`!`) and unsafe `as` casts except at proven boundaries; narrow with checks or schema validation instead.
- Use discriminated unions, branded types, or schema-derived types when they clarify important domain states.
- Use `===`/`!==` (loose `==` coerces types) and prefer `??` over `||` for defaults so valid falsy values like `0` or `""` are not silently overwritten.
- Add an exhaustiveness guard when branching over a discriminated union or literal type (assign the value to `never` in the `default`), so a new variant fails to compile until handled.
- Prefer `as const` objects or literal unions over `enum`s unless the repo already standardizes on enums; avoid numeric enums, which accept any number and emit runtime code.
- Do not silence type errors with `@ts-ignore`; if a suppression is truly needed, use `@ts-expect-error` with a comment so it fails once the underlying error is fixed.
- Do not add dependencies casually. Prefer platform APIs, framework utilities, or existing dependencies.

## Runtime Safety

- Remember that TypeScript types do not validate runtime inputs.
- Validate external data at boundaries such as HTTP requests, environment variables, storage, message queues, localStorage, and third-party APIs.
- Preserve API contracts, serialization formats, backward compatibility, and error semantics.
- Handle `undefined`, `null`, empty arrays, missing object keys, and async failure paths explicitly where they matter.
- Do not leak secrets, tokens, credentials, or personal data into logs, errors, telemetry, or client bundles.
- Treat caught errors as `unknown` and narrow (`instanceof Error`, schema checks) before using them; do not assume a thrown value is an `Error`.
- Treat array index access, `Record`/index-signature lookups, and `.find()`/`.pop()` results as possibly `undefined` and guard before use, even when `noUncheckedIndexedAccess` is off.
- Remember `readonly`/`ReadonlyArray` are erased at compile time and bypassed by aliasing; freeze or copy when you need a runtime immutability guarantee.

## Async And State

- Always await promises that must complete, return them intentionally, or document fire-and-forget behavior with a managed error path.
- Avoid floating promises, unhandled rejections, and race-prone shared mutable state.
- Use cancellation, abort signals, cleanup callbacks, or framework lifecycle hooks for work that may outlive a request, component, or job.
- Use `Promise.all` only when one failure should abort the batch (it rejects on the first rejection and drops other results); use `Promise.allSettled` when every outcome must be collected.
- Keep React, Vue, Svelte, or other UI state updates aligned with the local framework conventions when touching frontend code.

## Tests

- Add or update focused tests for behavior changes using the project's test stack, such as Vitest, Jest, Playwright, Testing Library, Cypress, or framework-native tools.
- Prefer observable behavior over private implementation details.
- Mock external boundaries such as network, time, storage, subprocesses, browser APIs, or third-party services. Avoid mocking the unit under test.
- Cover success, failure, loading, empty, validation, and permission states proportional to risk.
- Run the narrowest relevant test first, then broader checks when risk warrants it.
