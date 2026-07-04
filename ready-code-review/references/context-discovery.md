# Context Discovery

Review judgment depends on evidence sufficiency, not tool availability. Even without Git, PR, or repository access, proceed when provided evidence and filesystem evidence are sufficient.

## Evidence Source

### Provided Evidence

Materials provided directly by the user:

- diff or patch
- old/new snippet
- file content
- change description
- logs, error messages, test results
- screenshot or recording

### Repository Evidence

Materials obtained from a repository or PR system:

- PR URL, PR description, PR files
- commit, branch comparison
- `git diff`, `git show`, `git log`
- `git status`

`git status` is orientation evidence. It does not show changed behavior and cannot support a review finding by itself.

### Filesystem Evidence

Materials readable from the current working directory:

- touched files or related files
- tests
- `AGENTS.md`, `README*`
- `docs/**`, runbook, ADR, design note
- `.github/**`
- `_workspace/**/task.md`, `_workspace/**/implementation.md`, `_workspace/**/walkthrough.md`
- config, schema, migration, generated source inputs

### External Or Referenced Evidence

External materials referenced by the request:

- issue, ticket, design doc, wiki
- API documentation
- deployment/runbook documentation
- incident or support context

If external material is needed but unavailable, leave that item as a targeted question.

## Evidence Classification

### Orientation Evidence

Materials that orient review scope and direction:

- `git status`
- file tree or touched file list
- PR title
- task description
- issue title
- high-level changelog

Do not establish before/after behavior from orientation evidence alone.

### Change Evidence

Materials that directly show changed lines, changed files, or old/new behavior:

- diff, patch, commit, PR files
- old/new snippet
- before/after file content

Do not assert changed behavior without change evidence.

### Supporting Evidence

Materials that support a finding's contract, failure mode, or verification alongside change evidence:

- test changes and execution results
- logs or reproduction results
- docs, runbook, incident, support context
- command output

Supporting evidence does not create changed-line relevance by itself. If only supporting evidence is available without change evidence, ask for the needed change evidence instead of creating a finding.

## Sufficiency Rules

- Future findings must have a changed line or nearby line, plus at least one concrete supporting evidence source such as related code path, test, docs, log, or runbook.
- If supported behavior is unclear, write a question instead of a finding.
- Lack of Git is not a blocker. Missing change evidence is the blocker.
- If repository access is unavailable, record `N/A: no repository access` and proceed with provided, filesystem, or external evidence.
- If both repository and filesystem access are unavailable, record `N/A: no repository or filesystem access` and state what can be judged from user-provided materials only.
- Do not attach severity to items with insufficient evidence.

## Targeted Question Shape

```md
Question: Is <condition> a supported path? If yes, <evidence location> may violate <contract>. If not, I will treat it as an operator requirement or non-goal for this review.
```
