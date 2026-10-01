# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""Give an agent 300 tools and it pays for every definition on every turn.

The fix: mark the tools defer_loading and add a tool search tool. The model
starts with only the search tool, finds the few it needs, and those are loaded
on demand. This compares the input tokens of both setups and then runs a task.

Run:  ANTHROPIC_API_KEY=... uv run search.py
"""
import anthropic

client = anthropic.Anthropic()
DOMAINS = ["invoice", "customer", "shipment", "ticket", "employee", "contract", "payment", "refund", "product", "warehouse",
           "supplier", "lead", "campaign", "subscription", "asset", "expense", "timesheet", "order", "quote", "license"]
VERBS = ["get", "list", "create", "update", "archive", "export", "search", "merge", "assign", "audit", "restore", "summarise",
         "approve", "reject", "tag"]
TOOLS = [{"name": f"{v}_{d}", "description": f"{v.capitalize()} a {d} record in the ERP. Takes the {d} id and options.",
          "input_schema": {"type": "object", "properties": {"id": {"type": "string"}, "options": {"type": "object"}}, "required": ["id"]}}
         for d in DOMAINS for v in VERBS]
SEARCH = {"type": "tool_search_tool_bm25_20251119", "name": "tool_search_tool_bm25"}
DEFERRED = [SEARCH] + [dict(t, defer_loading=True) for t in TOOLS]
ASK = [{"role": "user", "content": "Refund REF-2291 was approved by mistake. Reject it."}]

loaded = client.messages.count_tokens(model="claude-opus-5-5", tools=TOOLS, messages=ASK).input_tokens
deferred = client.messages.count_tokens(model="claude-opus-5-5", tools=DEFERRED, messages=ASK).input_tokens
print(f"{len(TOOLS)} tools loaded up front: {loaded:,} input tokens per turn")
print(f"{len(TOOLS)} tools deferred + search: {deferred:,} input tokens per turn\n")

r = client.messages.create(model="claude-opus-5-5", max_tokens=4096, output_config={"effort": "low"}, tools=DEFERRED, messages=ASK)
for b in r.content:
    if b.type == "server_tool_use":
        print("searched for:", b.input)
    elif b.type == "tool_use":
        print("then called:", b.name, b.input)
print("stop_reason:", r.stop_reason)
