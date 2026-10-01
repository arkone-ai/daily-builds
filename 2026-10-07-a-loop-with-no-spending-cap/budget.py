# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""An agent loop with no budget does not stop when the money runs out. It stops when you notice.

The fix: a task budget the model can see. It is told how many tokens the whole
loop may use (tool calls, results and answer), sees a countdown, and paces
itself to finish inside it. This runs the same audit over 60 files with and
without a 30,000-token budget.

Run:  ANTHROPIC_API_KEY=... uv run budget.py
"""
import anthropic

client = anthropic.Anthropic()
FILES = {f"services/module_{i:02d}.py": (
    f"def handle_{i}(payload):\n"
    + ("    amount = payload['amount']\n" if i % 3 else "    amount = float(payload.get('amount', 0))\n    if amount < 0: raise ValueError('negative')\n")
    + "    return save(amount)\n" + "# helper code\n" * 120) for i in range(60)}
TOOLS = [
    {"name": "list_files", "description": "List every file in the repository.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "read_file", "description": "Read one file.", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
]
TASK = "Audit this repository: which modules read payload['amount'] without validating it? Give the list."


def run(budget):
    output_config = {"effort": "medium"}
    if budget:
        output_config["task_budget"] = {"type": "tokens", "total": budget}
    messages, used, calls = [{"role": "user", "content": TASK}], 0, 0
    for _ in range(80):
        with client.beta.messages.stream(model="claude-opus-5-5", max_tokens=32000, betas=["task-budgets-2026-03-13"],
                                         output_config=output_config, tools=TOOLS, messages=messages) as s:
            r = s.get_final_message()
        used += r.usage.input_tokens + r.usage.output_tokens
        messages.append({"role": "assistant", "content": r.content})
        uses = [b for b in r.content if b.type == "tool_use"]
        if not uses:
            break
        calls += len(uses)
        messages.append({"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": u.id,
             "content": "\n".join(FILES) if u.name == "list_files" else FILES.get(u.input["path"], "not found")} for u in uses]})
    answer = "".join(b.text for b in r.content if b.type == "text")
    return used, calls, answer


for label, budget in (("no budget", None), ("30,000-token budget", 30000)):
    used, calls, answer = run(budget)
    print(f"\n=== {label}: {used:,} tokens over the loop, {calls} tool calls ===\n{answer.strip()[:600]}")
