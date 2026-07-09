# Codex Adapter — Hook Registration

Host-specific packaging for Codex. Codex supports lifecycle hooks in
`hooks.json` or inline `[hooks]` tables in `config.toml`. This adapter records
the same prompt/action evidence as the Claude Code adapter, but writes under
`~/.codex/session-recipe/logs/`.

## Registration

For this skills repository, the project-local hook file is:

```text
.codex/hooks.json
```

Codex loads project-local hooks only when the project is trusted. After adding
or changing hooks, open `/hooks` in Codex and trust the new definitions before
expecting records to appear.

## Hook Configuration

Use this shape for a project-local `.codex/hooks.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "SESSION_RECIPE_LOG_ROOT=\"$HOME/.codex/session-recipe/logs\" python3 \"$(git rev-parse --show-toplevel)/session-recipe/scripts/record_action.py\"",
            "timeout": 10,
            "statusMessage": "Recording prompt"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash|apply_patch|Edit|Write|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "SESSION_RECIPE_LOG_ROOT=\"$HOME/.codex/session-recipe/logs\" python3 \"$(git rev-parse --show-toplevel)/session-recipe/scripts/record_action.py\"",
            "timeout": 10,
            "statusMessage": "Recording action"
          }
        ]
      }
    ]
  }
}
```

## Verify the Installation

After trusting the hook definitions:

1. Submit a new prompt in this repository.
2. Run a small command or make a tiny file edit.
3. Check the newest `.jsonl` under `~/.codex/session-recipe/logs/`.
4. Confirm it contains a `prompt` record and at least one `action` record.

The recorder is best-effort and silent: failures exit 0 so hooks never block a
Codex turn. If no records appear, inspect `/hooks` first, then check that this
project is trusted and that Python 3 is available on Codex's hook PATH.
