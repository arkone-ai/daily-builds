# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""Same task, same model, two effort settings. Watch the token count.

Claude Opus 5.5 always thinks; you steer how much with output_config.effort
(low, medium, high, xhigh, max). Its default is medium. This runs one code
review at medium and at max and prints what each cost in tokens and time.

Run:  ANTHROPIC_API_KEY=... uv run effort.py
"""
import time
import anthropic

TASK = """Review this function. List every bug, one line each, most serious first.

def average_order_value(orders):
    total = 0
    for o in orders:
        if o["status"] != "refunded":
            total += o["amount"]
    return round(total / len(orders), 2)
"""

client = anthropic.Anthropic()


def run(effort: str):
    start = time.perf_counter()
    with client.beta.messages.stream(
        model="claude-opus-5-5",
        max_tokens=64000,
        output_config={"effort": effort},
        # If a request is ever declined, the API retries it on a fallback model.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[{"role": "user", "content": TASK}],
    ) as stream:
        message = stream.get_final_message()
    seconds = time.perf_counter() - start
    if message.stop_reason == "refusal":
        raise SystemExit(f"{effort}: declined ({message.stop_details})")
    text = "".join(b.text for b in message.content if b.type == "text")
    return message.usage.output_tokens, seconds, text


results = {effort: run(effort) for effort in ("medium", "max")}

for effort, (tokens, seconds, text) in results.items():
    print(f"\n=== effort={effort}: {tokens} output tokens, {seconds:.1f}s ===\n{text.strip()}")

(m_tokens, m_s, _), (x_tokens, x_s, _) = results["medium"], results["max"]
print(f"\nmax used {x_tokens / m_tokens:.1f}x the tokens and {x_s / m_s:.1f}x the time of medium.")
