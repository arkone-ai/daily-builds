# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""An agent that runs all day eventually forgets the start of its own task.

The fix: compact on demand. The harness decides when the history becomes a
signed summary, sends that summary first on every later request, and drops
the turns it replaced. Here a goal and a hard constraint are set in turn 1,
buried under a long session, then compacted. The agent is asked about both.

Run:  ANTHROPIC_API_KEY=... uv run compact.py
"""
import anthropic

client = anthropic.Anthropic()
BETA = ["compact-2026-09-04"]
SYSTEM = "You are a migration agent. Keep answers to two sentences."

history = [{"role": "user", "content": "Goal: migrate the invoices table from MySQL to Postgres. Hard constraint: never drop the legacy_tax_code column, finance still reads it."}]
log_lines = "\n".join(f"row batch {i}: copied 5,000 rows, 0 errors, checksum ok" for i in range(1, 600))
history += [
    {"role": "assistant", "content": "Understood. Starting the copy."},
    {"role": "user", "content": f"Progress log so far:\n{log_lines}\nKeep going."},
]


def tokens(messages):
    return client.beta.messages.count_tokens(model="claude-opus-5-5", system=SYSTEM, messages=messages, betas=BETA).input_tokens


before = tokens(history)
summary = client.beta.messages.create(
    model="claude-opus-5-5", max_tokens=4096, system=SYSTEM, betas=BETA,
    messages=history, compaction={"type": "summarize"},
)
if summary.stop_reason != "compaction":
    raise SystemExit(f"no summary this time: {summary.stop_reason}")

history = [{"role": "assistant", "content": summary.content}]
history.append({"role": "user", "content": "Before you continue: what is the goal, and what must you never do?"})
after = tokens(history)

answer = client.beta.messages.create(model="claude-opus-5-5", max_tokens=1024, system=SYSTEM, betas=BETA, messages=history)
print(f"history before compaction: {before:,} tokens")
print(f"history after compaction:  {after:,} tokens\n")
print("agent:", "".join(b.text for b in answer.content if b.type == "text"))
