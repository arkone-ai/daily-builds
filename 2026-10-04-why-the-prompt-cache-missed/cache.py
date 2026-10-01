# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""Your prompt cache missed. Now the API tells you why.

Three requests with the same long system prompt. The second reads the cache.
Before the third we change one word in the system prompt, and the response's
diagnostics object names what diverged from the previous request.

Run:  ANTHROPIC_API_KEY=... uv run cache.py
"""
import uuid
import anthropic

client = anthropic.Anthropic()
RUN = uuid.uuid4().hex[:8]  # a fresh prefix each run, so the demo always starts cold
POLICY = f"Policy version {RUN}\n" + "\n".join(f"Rule {i}: refunds over ${i * 10} need a manager's approval within {i} days." for i in range(1, 400))


def ask(system: str, previous_id):
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        output_config={"effort": "low"},
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": "Does a $35 refund need approval? One line."}],
        extra_body={"diagnostics": {"previous_message_id": previous_id}},
    )
    u = response.usage
    print(f"cache read {u.cache_read_input_tokens:>6} | cache write {u.cache_creation_input_tokens:>6}")
    reason = response.diagnostics and response.diagnostics.cache_miss_reason
    if reason:
        print(f"why it missed: {reason.type}, {reason.cache_missed_input_tokens} tokens not read from cache")
    return response.id


first = ask("You answer refund questions.\n" + POLICY, None)
second = ask("You answer refund questions.\n" + POLICY, first)
print("\nNow one word of the system prompt changes:")
ask("You answer refund questions briefly.\n" + POLICY, second)
