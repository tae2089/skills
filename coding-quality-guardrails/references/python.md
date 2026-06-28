# Python Reference

Read this for Python code generation, review, refactoring, or test fixes.

## Python Style

- Match existing architecture, naming, typing level, logging, tests, and dependency choices.
- Follow the repository formatter and linter. If unknown, prefer `ruff format`/`ruff check` when configured, otherwise Black-compatible formatting.
- Use type hints for new or changed public functions and complex internal code.
- Prefer `pathlib.Path` over raw string path manipulation.
- Avoid mutable default arguments.
- Keep import side effects minimal; do not perform network calls, filesystem writes, or heavyweight initialization at import time.
- Prefer dataclasses, Pydantic models, or TypedDict only when they match the project and the data benefits from structure.
- Do not add dependencies casually. Prefer the standard library or existing dependencies.

## Errors And Logging

- Let exceptions propagate when the caller has the right context to handle them.
- Convert exceptions at boundaries such as CLI output, HTTP responses, worker retries, or user-facing APIs.
- Preserve original exceptions with `raise ... from exc` when adding context.
- Avoid broad `except Exception`; when unavoidable, log or convert intentionally.
- Do not log and re-raise the same exception unless the log provides operational context that would otherwise be lost.
- Do not leak secrets, credentials, tokens, or personal data into logs or exception messages.

## Typing

- Prefer precise, readable types over clever type gymnastics.
- Use `Sequence[T]` and `Mapping[K, V]` for read-only inputs; use concrete `list`/`dict` when mutation matters.
- Use `T | None` or `Optional[T]` according to repository style and Python version.
- Avoid `Any` except at genuinely dynamic boundaries; normalize into typed data quickly.

## Tests

- Use pytest style if the repo uses pytest; use unittest only when it is the local standard.
- Use fixtures for meaningful shared setup and one-off setup inside the test.
- Use `tmp_path` for temporary files.
- Mock external boundaries such as network, time, subprocesses, filesystem side effects, or third-party services. Avoid mocking the code under test.
- Cover success, failure, and edge cases proportional to risk.

## Async

- Do not introduce async unless the surrounding stack is already async or the task clearly needs concurrency.
- Never block the event loop with synchronous network, filesystem, or sleep calls in async paths.
- Use cancellation-aware code where tasks may outlive a request or job.
- Use the project's existing async test setup.

