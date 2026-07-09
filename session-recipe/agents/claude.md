# Claude Code Adapter — Hook Registration

Host-specific packaging for Claude Code. Other runtimes need their own adapter that feeds equivalent JSON events to `scripts/record_action.py` or a port of it.

## Prerequisite

The recorder needs Python 3.9+ on the hook's PATH (stdlib only, no packages). macOS and most Linux distributions ship `python3`; native Windows does not — install Python (or run Claude Code under WSL/Git Bash, where `python3` is available) and adjust the hook command to `python` or `py -3` if `python3` is not aliased.

## Registration

Add to `~/.claude/settings.json` (all projects) or `<repo>/.claude/settings.json` (one project). Merge into an existing `hooks` key rather than replacing it. Prefer configuring this through Claude Code's own settings tooling (e.g. the `update-config` skill) when available.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 <skills-repo>/session-recipe/scripts/record_action.py",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|NotebookEdit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 <skills-repo>/session-recipe/scripts/record_action.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Replace `<skills-repo>` with the absolute path of this skills repository. Claude Code watches registered settings files, so a running session usually picks the hooks up on save; if records do not appear, open `/hooks` once or restart the session.

## Event Contract

Claude Code sends one JSON payload on stdin per event. The recorder uses:

| Field | Events | Use |
| --- | --- | --- |
| `hook_event_name` | both | Dispatch: `UserPromptSubmit` → prompt record, `PostToolUse` → action record |
| `session_id`, `cwd` | both | Log file location: `~/.claude/session-recipe/logs/<cwd-slug>/<session-id>.jsonl` |
| `prompt` | UserPromptSubmit | Stored redacted and truncated |
| `tool_name`, `tool_input` | PostToolUse | Only `Edit`, `Write`, `NotebookEdit`, `Bash` are recorded; file paths and commands only, never file contents |

## Constraints Baked Into the Recorder

- **Never print to stdout.** `UserPromptSubmit` hook stdout is injected into the model's context; the recorder stays silent.
- **Always exit 0.** A recording failure drops the record instead of blocking the session.
- **Redaction is keyword-based**: `key=value` / `key: value` pairs redact when the key contains a secret keyword (`password`, `token`, `api_key`, `secret`, ...); whitespace-separated values (`Bearer eyJ...`) redact only when they look like a secret (≥ 8 chars with a digit). It is a safety net, not a guarantee — distillation re-scans before a recipe is saved.
- **Logs accumulate indefinitely.** They are the ground truth for distillation, so keep them until their sessions are distilled; after that, pruning old slug directories is safe.

## Verify the Installation

```sh
printf '{"hook_event_name":"UserPromptSubmit","session_id":"smoke-test","cwd":"%s","prompt":"hello"}' "$PWD" \
  | python3 <skills-repo>/session-recipe/scripts/record_action.py
```

Then confirm a `smoke-test.jsonl` appeared under `~/.claude/session-recipe/logs/` and delete it. In a live session, run any `Edit` or `Bash` action and check the session's log file gained an `action` line.
