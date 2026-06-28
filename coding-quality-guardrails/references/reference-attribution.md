# Reference Attribution Reference

Read this when external docs, specs, issues, articles, community posts, or standards materially influence implementation or handoff notes.

## Attribution Rules

- In the final response, PR description, or handoff note, list external references that materially influenced implementation decisions.
- Prefer primary and stable sources: official documentation, specs, repository docs, release notes, source code, or canonical issues.
- Avoid citing generic tutorials when a primary source exists.
- Add a code comment with a link only when the implementation would be hard to understand or safely change without that source, such as a protocol requirement, wire format, runtime quirk, security rule, algorithm, or compatibility workaround.
- Keep source comments short and behavior-focused. Explain the constraint, not the research journey.
- Do not put broad reading lists, rationale essays, generic best-practice links, or "I used this source" notes into production code.
- Do not cite a source as implementation support if it was checked but not relied on.
- If a source might be stale, name the exact version, date, or API surface used when practical.

