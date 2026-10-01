# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""A score regenerated on every page load costs money each time and reads differently each time.

The fix, a rule on ArkOne's platform: the agent computes a judgement once and
writes it through a tool, with the value, the reason, who wrote it and when.
Every later read is free and identical. A judgement nobody has written renders
as absent, never as 0.

Run:  ANTHROPIC_API_KEY=... uv run judgements.py
"""
import json
import sqlite3
from datetime import datetime, timezone
import anthropic

client = anthropic.Anthropic()
db = sqlite3.connect("judgements.db")
db.execute("create table if not exists judgement (record text primary key, value integer, reason text, author text, written_at text)")
ACCOUNT = {"id": "acct-118", "name": "Gulf Freight LLC", "employees": 340, "uses_spreadsheets_for": "quotes and fleet scheduling", "replied_to_last_email": False}


def read(record):
    row = db.execute("select value, reason, author, written_at from judgement where record = ?", (record,)).fetchone()
    return dict(zip(("value", "reason", "author", "written_at"), row)) if row else None


def write(record, value, reason, author):
    db.execute("insert or replace into judgement values (?, ?, ?, ?, ?)", (record, value, reason, author, datetime.now(timezone.utc).isoformat(timespec="seconds")))
    db.commit()


print("before any agent has scored it:", read(ACCOUNT["id"]) or "absent (shown as —, never 0)")

TOOL = {"name": "write_fit_score", "description": "Store a 0-100 fit score for an account, with the reason.", "strict": True,
        "input_schema": {"type": "object", "additionalProperties": False, "required": ["value", "reason"],
                         "properties": {"value": {"type": "integer"}, "reason": {"type": "string"}}}}
r = client.messages.create(model="claude-opus-5-5", max_tokens=2048, output_config={"effort": "low"}, tools=[TOOL],
                           messages=[{"role": "user", "content": f"Score how well this account fits an AI automation offer, then store it.\n{json.dumps(ACCOUNT)}"}])
for b in r.content:
    if b.type == "tool_use":
        write(ACCOUNT["id"], b.input["value"], b.input["reason"], author=f"{r.model} (agent)")

for n in (1, 2):
    print(f"page load {n}:", json.dumps(read(ACCOUNT["id"])), "(0 model calls)")
