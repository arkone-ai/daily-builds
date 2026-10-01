# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""The first question after an agent mistake is what it did. Most harnesses cannot answer it.

The fix: every tool call goes through one wrapper that writes an event before
and after: run id, tool, arguments, result, duration, time. The log is
append-only JSON lines, so a run can be replayed step by step afterwards.

Run:  ANTHROPIC_API_KEY=... uv run audit.py
"""
import json
import time
import uuid
from datetime import datetime, timezone
import anthropic

client = anthropic.Anthropic()
RUN = uuid.uuid4().hex[:8]
LOG = "events.jsonl"
STOCK = {"SKU-1": 40, "SKU-2": 0, "SKU-3": 12}


def event(kind, **data):
    with open(LOG, "a") as f:
        f.write(json.dumps({"run": RUN, "at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "event": kind, **data}) + "\n")


def audited(name, fn):
    def call(**args):
        event("tool_call", tool=name, args=args)
        start = time.perf_counter()
        try:
            result = fn(**args)
            event("tool_result", tool=name, result=result, ms=round((time.perf_counter() - start) * 1000))
            return result
        except Exception as e:
            event("tool_error", tool=name, error=str(e))
            raise
    return call


def check_stock(sku):
    return {"sku": sku, "on_hand": STOCK.get(sku, 0)}


def reserve(sku, qty):
    if STOCK.get(sku, 0) < qty:
        return {"reserved": 0, "reason": "not enough stock"}
    STOCK[sku] -= qty
    return {"reserved": qty}


FUNCS = {"check_stock": audited("check_stock", check_stock), "reserve": audited("reserve", reserve)}
TOOLS = [
    {"name": "check_stock", "description": "Units on hand for a SKU.", "input_schema": {"type": "object", "properties": {"sku": {"type": "string"}}, "required": ["sku"]}},
    {"name": "reserve", "description": "Reserve units of a SKU for an order.", "input_schema": {"type": "object", "properties": {"sku": {"type": "string"}, "qty": {"type": "integer"}}, "required": ["sku", "qty"]}},
]
event("run_started", task="Reserve 5 of SKU-1, 3 of SKU-2 and 5 of SKU-3 for order 7781")
messages = [{"role": "user", "content": "Reserve 5 of SKU-1, 3 of SKU-2 and 5 of SKU-3 for order 7781. Report what was and was not reserved."}]
while True:
    r = client.messages.create(model="claude-opus-5-5", max_tokens=4096, output_config={"effort": "low"}, tools=TOOLS, messages=messages)
    messages.append({"role": "assistant", "content": r.content})
    uses = [b for b in r.content if b.type == "tool_use"]
    if not uses:
        break
    messages.append({"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": u.id, "content": json.dumps(FUNCS[u.name](**u.input))} for u in uses]})
event("run_finished", answer="".join(b.text for b in r.content if b.type == "text"))

print(f"replay of run {RUN}:")
for line in open(LOG):
    e = json.loads(line)
    if e["run"] == RUN and e["event"] != "run_finished":
        detail = e.get("args") or e.get("result") or e.get("task") or e.get("error")
        print(f"  {e['at'][11:19]}  {e['event']:<12} {e.get('tool', ''):<12} {json.dumps(detail)}")
