# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""One of our MCP tools once returned 2 MB in a single reply. The agent never finished.

The fix, a rule on every list tool we ship: return one page, the true total,
and where the next page starts. The agent sees that more exists and asks for
it, or answers from the total without reading every row.

Run:  ANTHROPIC_API_KEY=... uv run paged.py
"""
import json
import random
import anthropic

client = anthropic.Anthropic()
random.seed(7)
INVOICES = [{"id": f"INV-{i:05d}", "customer": f"Customer {i % 900}", "amount": round(random.uniform(50, 9000), 2),
             "status": random.choice(["paid", "paid", "paid", "overdue", "draft"])} for i in range(20000)]


def list_invoices_dump():
    return INVOICES  # the tool as first written: everything, every time


def list_invoices(status=None, sort_by_amount=False, limit=20, offset=0):
    rows = [r for r in INVOICES if status in (None, "any") or r["status"] == status]
    if sort_by_amount:
        rows = sorted(rows, key=lambda r: r["amount"], reverse=True)
    page = rows[offset:offset + limit]
    nxt = offset + len(page)
    return {"rows": page, "total": len(rows), "next_offset": nxt if nxt < len(rows) else None}


def size(payload):
    msg = [{"role": "user", "content": json.dumps(payload)}]
    return client.messages.count_tokens(model="claude-opus-5-5", messages=msg).input_tokens


print(f"full dump as a tool reply: {size(list_invoices_dump()):,} tokens")
print(f"one page with the total:   {size(list_invoices(limit=20)):,} tokens\n")

TOOL = {
    "name": "list_invoices",
    "description": "List invoices one page at a time. Returns rows, the true total matching the filter, and next_offset (null on the last page).",
    "strict": True,
    "input_schema": {
        "type": "object", "additionalProperties": False,
        "properties": {
            "status": {"type": "string", "enum": ["any", "paid", "overdue", "draft"]},
            "sort_by_amount": {"type": "boolean"},
            "limit": {"type": "integer"},
            "offset": {"type": "integer"},
        },
        "required": ["status", "sort_by_amount", "limit", "offset"],
    },
}
messages = [{"role": "user", "content": "How many invoices are overdue, and which three overdue invoices are largest?"}]
used = 0
while True:
    r = client.messages.create(model="claude-opus-5-5", max_tokens=4096, output_config={"effort": "low"}, tools=[TOOL], messages=messages)
    used += r.usage.input_tokens + r.usage.output_tokens
    messages.append({"role": "assistant", "content": r.content})
    calls = [b for b in r.content if b.type == "tool_use"]
    if not calls:
        break
    messages.append({"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": c.id, "content": json.dumps(list_invoices(**c.input))} for c in calls]})
    for c in calls:
        print("tool call:", json.dumps(c.input))

print(f"\nwhole agent run: {used:,} tokens")
print("agent:", "".join(b.text for b in r.content if b.type == "text"))
