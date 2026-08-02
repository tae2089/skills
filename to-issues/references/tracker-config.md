# Tracker configuration

`.scratch/.tracker` is a shared project file. It selects one publication destination for both `to-spec` and `to-issues`; it is not an authentication file. `to-spec` reads this file at `../to-issues/references/tracker-config.md`.

## Format

Use one `key: value` pair per line:

```text
provider: github
target: owner/repository
ready-label: ready-for-agent
```

- `provider` is required: `local`, `github`, `gitlab`, or `jira`.
- `target` is required for remote providers and forbidden for `local`.
- `ready-label` is optional. When omitted, create no status field or label on the spec or on any ticket.
- Reject unknown keys, duplicate keys, empty values, and lines that are not `key: value` pairs as malformed configuration.
- Never store tokens, passwords, private keys, webhook URLs, or credential-bearing connection strings. If a credential key or value is present, stop without echoing the value.

Keep `.scratch/.tracker`, the local spec, and local tickets in version control so the team shares the same choice and work queue. Before local publication in a Git repository, check that no path you are about to write is ignored. If one is, stop before writing and ask the user to make the paths trackable.

## Providers

| `provider` | `target` | Publication tool |
| --- | --- | --- |
| `local` | Omit | Files under `.scratch/<feature-slug>/` — `spec.md` for the spec, `issues/<NN>-<slug>.md` for the tickets |
| `github` | `owner/repository` | Connected GitHub tool; otherwise an already-authenticated `gh` CLI |
| `gitlab` | `namespace/project` | Connected GitLab tool; otherwise an already-authenticated `glab` CLI |
| `jira` | An unambiguous site and project identifier accepted by the connected Jira tool | Connected Jira tool |

Do not install a CLI, start an authentication flow, or ask for a secret. Treat the provider as unavailable when no listed tool is ready, then follow the local fallback in the calling skill's `SKILL.md`.

Use the tool's native parent, sub-issue, and blocking relationships when available. If a relationship is unsupported, keep the same reference in the issue body and report that no native link was created.

## Failure rules

- Missing configuration is an intentional first-use path. After approval, create `provider: local` plus the local spec or tickets.
- Preserve malformed, unsupported, or unusable remote configuration so a temporary fallback does not silently change the team's intended tracker.
- Fall back only before the first remote issue is created.
- After partial remote success, stop and report created identifiers. Do not create local duplicates.
