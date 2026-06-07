#!/usr/bin/env python3
"""Claude Sessions Manager — list all sessions with UUID, name, and project."""
import json
import os
import glob
from datetime import datetime, timezone

projects_dir = os.path.expanduser("~/.claude/projects")
rows = []

for jsonl_path in glob.glob(os.path.join(projects_dir, "*", "*.jsonl")):
    project_slug = os.path.basename(os.path.dirname(jsonl_path))
    uuid = os.path.basename(jsonl_path).replace(".jsonl", "")
    title = None
    mtime = os.path.getmtime(jsonl_path)

    ai_title = None
    custom_title = None
    try:
        with open(jsonl_path) as f:
            for line in f:
                try:
                    d = json.loads(line)
                    if d.get("type") == "ai-title":
                        ai_title = d.get("aiTitle", "").strip()
                    elif d.get("type") == "custom-title":
                        custom_title = d.get("customTitle", "").strip()
                except Exception:
                    pass
    except Exception:
        pass
    title = custom_title or ai_title

    rows.append((mtime, uuid, title or "(no title)", project_slug))

rows.sort(reverse=True)

if not rows:
    print("No Claude sessions found under ~/.claude/projects/")
else:
    col_uuid   = max(len("Session UUID"), max(len(r[1]) for r in rows))
    col_title  = max(len("Session Name"), max(len(r[2]) for r in rows))
    col_proj   = max(len("Project"), max(len(r[3]) for r in rows))

    header = f"{'Last Modified':<16}  {'Session UUID':<{col_uuid}}  {'Session Name':<{col_title}}  {'Project'}"
    sep    = "-" * len(header)
    print(header)
    print(sep)

    for mtime, uuid, title, proj in rows:
        ts = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        print(f"{ts:<16}  {uuid:<{col_uuid}}  {title:<{col_title}}  {proj}")

    print(f"\n{len(rows)} session(s) found.")
