---
name: claude-sessions-manager
description: >
  Manages Claude Code sessions stored on disk. Only applies to Claude Code (the
  Anthropic CLI and VS Code extension) — not Cursor, Windsurf, Antigravity, or
  other agents. Currently supports listing all sessions. Use this skill whenever
  the user asks to list sessions, show session IDs, map UUIDs to session names,
  find a past session, or asks anything like "what sessions do I have", "list my
  Claude sessions", "show session ID to name mapping", or "which session is X".
  More session management operations (e.g., deleting sessions) will be added here
  in future.
license: Apache-2.0
metadata:
  author: Vincent Yin
  version: "1.0.1"
  requires:
    bins:
      - python3
---

# Claude Sessions Manager

Manages Claude Code sessions stored on disk under `~/.claude/projects/`.

Each session is a `.jsonl` file named by UUID. The session name is resolved by
preferring the user-set custom title (`custom-title` record) over the
AI-generated title (`ai-title` record). Both are tracked across the full file
so the last occurrence of each type wins; custom title always beats AI title
when both exist.

## List all sessions

Run the bundled script:

```bash
python3 "$SKILL_DIR/scripts/list_sessions.py"
```

where `$SKILL_DIR` is the base directory of this skill (provided at the top of
the skill context when invoked). For example:

```bash
python3 ~/.agents/skills/claude-sessions-manager/scripts/list_sessions.py
```

The output is a table sorted newest-first with columns:

| Column | Description |
|---|---|
| Last Modified | File modification timestamp (`YYYY-MM-DD HH:MM`) |
| Session UUID | The UUID filename of the `.jsonl` session file |
| Session Name | Custom title if set; otherwise AI-generated title; otherwise `(no title)` |
| Project | The `~/.claude/projects/` subdirectory slug (derived from the working directory path) |

To resume a session after finding its UUID:

```bash
claude --resume <session-uuid>
```

## Platform notes

- **Claude Code only.** This skill reads session files written by the Anthropic
  Claude Code CLI and VS Code extension. It does not apply to Cursor, Windsurf,
  Antigravity, or any other agent that uses different session storage.
- Works on macOS and Linux where Claude Code stores sessions under `~/.claude/projects/`.
- Requires Python 3 (standard on both platforms).
- Windows is not supported (different session storage path).
