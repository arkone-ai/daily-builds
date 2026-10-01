# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""Monday's session learned the customer's rules. Tuesday's session starts from zero.

The fix: a memory tool the agent reads and writes, backed by storage you
control. Here it is a folder (./memory); in production it would be your
database, scoped per customer. Session 1 is told the rules. Session 2 is a
fresh conversation with no history, and is only asked to do the work.

Run:  ANTHROPIC_API_KEY=... uv run memory.py
"""
import os
import anthropic
from anthropic.tools import BetaLocalFilesystemMemoryTool

client = anthropic.Anthropic()
memory = BetaLocalFilesystemMemoryTool(base_path="./memory")
SYSTEM = "You are an accounts-receivable agent. Check your memory before you act, and save customer rules you learn."


def session(prompt):
    runner = client.beta.messages.tool_runner(
        model="claude-opus-5-5", max_tokens=8000, system=SYSTEM, tools=[memory],
        output_config={"effort": "low"}, messages=[{"role": "user", "content": prompt}],
    )
    last = None
    for message in runner:
        for block in message.content:
            if block.type == "tool_use":
                print(f"  memory.{block.input.get('command')} {block.input.get('path', '')}")
        last = message
    return "".join(b.text for b in last.content if b.type == "text")


print("SESSION 1")
print(session("Rules for Acme Trading: invoice in AED, payment terms net-45, and never email their finance team before 9am Gulf time."))
print("\nSESSION 2 (new conversation, no history)")
print(session("Draft tomorrow's payment reminder for Acme Trading's overdue invoice INV-0412, and say when to send it."))
print("\nmemory on disk:")
for root, _, files in os.walk("memory"):
    for f in files:
        print(" ", os.path.join(root, f))
