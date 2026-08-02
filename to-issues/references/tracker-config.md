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
- `spec-target` is optional and valid only with `provider: jira`. It sends the spec to Confluence instead of a Jira issue — see "Jira with Confluence" below. Present with any other provider is malformed configuration.
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

## Jira with Confluence

A Jira issue is a poor container for a long spec, and a Confluence page cannot be the parent of a Jira issue. So `spec-target` splits the spec from the parent it needs, and `to-spec` creates both:

```text
provider: jira
target: your-company.atlassian.net/PROJ
spec-target: your-company.atlassian.net/wiki/spaces/ENG
ready-label: ready-for-agent
```

`target` and `spec-target` must be in whatever form the connected Atlassian tool accepts. The example above shows the shape, not a guaranteed format — if the tool rejects an identifier, report the rejection instead of reformatting and retrying blindly.

`spec-target` names either a Confluence space or one existing page inside it. A space means the spec pages hang under a **seed page** — one index page holding every spec, created on first use. A page means that page is the parent and nothing is seeded.

`to-spec` publishes in this order, and each step must succeed before the next:

1. **Seed page** — only when `spec-target` names a space and no page with the seed title exists in it. Give the page a title the team will recognise (`Specs` unless the user names another) and a body stating the convention: each child page is one spec, and the work breakdown lives in Jira. If two pages already carry that title, stop — an ambiguous parent is not a parent.
2. **Spec page** — the spec itself, as a child of the seed page or of the page `spec-target` named.
3. **Parent issue** — in `target`'s project, using the project's **default standard issue type** — Task, or Story when the project has no Task. Its description links the spec page rather than repeating it. Show the type in the approval preview; if the connected tool cannot tell you the project's default type, ask instead of guessing.

**Do not create an epic.** An epic is a planning-sized container the team already uses for something bigger, and creating one is often permission-restricted. One spec is one normal issue, and the tickets are its children.

Then link the parent issue on the spec page when the connected tool supports it. A missing link is reported, not a failure.

`to-issues` needs no change for this: the Jira parent issue is what it treats as the parent, exactly as when the spec itself was that issue. Its child tickets become sub-tasks of that issue where the tool supports them, and every child's body links the spec page.

## Failure rules

- Missing configuration is an intentional first-use path. After approval, create `provider: local` plus the local spec or tickets.
- Preserve malformed, unsupported, or unusable remote configuration so a temporary fallback does not silently change the team's intended tracker.
- Fall back only before the first remote issue or page is created.
- After partial remote success, stop and report created identifiers and page URLs. Do not create local duplicates, and do not delete what already exists to retry cleanly — a half-published spec the team can see beats a silent rollback.
