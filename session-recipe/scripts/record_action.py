#!/usr/bin/env python3
"""Hook recorder for the session-recipe skill.

Reads one hook event payload (JSON) from stdin and appends a compact record to
``<log-root>/<cwd-slug>/<session-id>.jsonl``. The default log root is
``~/.claude/session-recipe/logs``; Codex hooks should set
``SESSION_RECIPE_LOG_ROOT`` to ``~/.codex/session-recipe/logs``.

Register it for prompt-submission and post-tool-use hook events; host-specific
registration snippets live under ``../agents/``.

Recording is best-effort by design: the script always exits 0 and never writes
to stdout, so a recorder failure can neither block nor pollute the session.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

LOG_ROOT = Path(
    os.environ.get(
        "SESSION_RECIPE_LOG_ROOT",
        str(Path.home() / ".claude" / "session-recipe" / "logs"),
    )
).expanduser()
RECORDED_TOOLS = {"Edit", "Write", "NotebookEdit", "Bash", "apply_patch"}
PROMPT_LIMIT = 4000
COMMAND_LIMIT = 2000
_SECRET_KEYWORDS = (
    r"(?:password|passwd|secret|token|api[_-]?key|access[_-]?key|"
    r"private[_-]?key|credential|authorization|bearer)"
)
# Keyword may sit inside an identifier (AWS_SECRET_ACCESS_KEY=...), so no \b
# around the key part; the =/: separator is what keeps prose out.
SECRET_KV_PATTERN = re.compile(
    rf"(?i)([A-Za-z0-9_\-]*{_SECRET_KEYWORDS}[A-Za-z0-9_\-]*)"
    rf"(\s*[=:]\s*)(\"[^\"]*\"|'[^']*'|bearer\s+\S+|\S+)"
)
# Whitespace-separated values ("Bearer eyJ...", "--password s3cr3t99") redact
# only when the value looks like a secret (>= 8 chars containing a digit), so
# prose like "the token is stored" survives.
SECRET_WS_PATTERN = re.compile(
    rf"(?i)\b(bearer|authorization|password|passwd|secret|token|api[_-]?key)"
    rf"(\s+)((?=\S*\d)\S{{8,}})"
)


def redact(text: str) -> str:
    text = SECRET_KV_PATTERN.sub(lambda m: f"{m.group(1)}{m.group(2)}[REDACTED]", text)
    return SECRET_WS_PATTERN.sub(lambda m: f"{m.group(1)}{m.group(2)}[REDACTED]", text)


def as_text(value) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, default=str)


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"...[truncated {len(text) - limit} chars]"


def first_text(payload: dict, *keys: str) -> str:
    for key in keys:
        value = payload.get(key)
        if value not in (None, ""):
            return as_text(value)
    return ""


def event_name(payload: dict) -> str:
    event = first_text(payload, "hook_event_name", "event", "event_name", "hookEventName")
    normalized = re.sub(r"[^a-z0-9]+", "", event.lower())
    if normalized == "userpromptsubmit":
        return "UserPromptSubmit"
    if normalized == "posttooluse":
        return "PostToolUse"
    return event


def tool_name(payload: dict) -> str:
    tool = payload.get("tool")
    if isinstance(tool, dict):
        return first_text(tool, "name", "tool_name")
    if isinstance(tool, str):
        return tool
    return first_text(payload, "tool_name", "toolName", "tool")


def tool_input(payload: dict) -> dict:
    for key in ("tool_input", "toolInput", "input", "arguments", "args"):
        value = payload.get(key)
        if isinstance(value, dict):
            return value
    tool = payload.get("tool")
    if isinstance(tool, dict):
        for key in ("input", "arguments", "args"):
            value = tool.get(key)
            if isinstance(value, dict):
                return value
    return {}


def cwd_value(payload: dict) -> str:
    cwd = first_text(payload, "cwd", "working_directory", "workingDirectory")
    return cwd or os.getcwd()


def session_id_value(payload: dict) -> str:
    return first_text(
        payload,
        "session_id",
        "sessionId",
        "thread_id",
        "threadId",
        "conversation_id",
        "conversationId",
    )


def git_head(cwd: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def build_record(payload: dict) -> Optional[dict]:
    event = event_name(payload)
    cwd = cwd_value(payload)
    base = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "cwd": cwd,
    }
    if event == "UserPromptSubmit":
        base["event"] = "prompt"
        prompt = first_text(payload, "prompt", "user_prompt", "userPrompt", "input")
        base["prompt"] = redact(truncate(prompt, PROMPT_LIMIT))
        base["git_head"] = git_head(cwd)
        return base
    if event == "PostToolUse":
        tool = tool_name(payload)
        if tool not in RECORDED_TOOLS:
            return None
        input_payload = tool_input(payload)
        base["event"] = "action"
        base["tool"] = tool
        if tool == "Bash":
            command = first_text(input_payload, "command", "cmd")
            base["command"] = redact(truncate(command, COMMAND_LIMIT))
            if input_payload.get("description"):
                base["description"] = redact(as_text(input_payload["description"]))
        elif tool == "apply_patch":
            base["operation"] = "patch"
        else:
            base["file_path"] = (
                input_payload.get("file_path")
                or input_payload.get("filePath")
                or input_payload.get("notebook_path")
                or input_payload.get("notebookPath")
            )
        return base
    return None


def log_path(payload: dict) -> Path:
    # \w keeps Unicode letters, so Korean/Japanese path segments stay distinct
    # instead of collapsing distinct projects into one slug directory.
    slug = re.sub(r"[^\w]+", "-", cwd_value(payload)).strip("-") or "unknown"
    session_id = re.sub(r"[^A-Za-z0-9_-]+", "-", session_id_value(payload)) or "unknown"
    return LOG_ROOT / slug / f"{session_id}.jsonl"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        record = build_record(payload)
        if record is None:
            return 0
        path = log_path(payload)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        # Recording must never block or pollute the session; drop the record.
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
