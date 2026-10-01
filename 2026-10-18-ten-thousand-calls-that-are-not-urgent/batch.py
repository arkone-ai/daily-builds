# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""Running a nightly backfill through the live API pays full price to wait in a queue.

The fix: send work that can wait as one Message Batch. Each request is billed
at half the standard price, it does not compete with live traffic for rate
limits, and results come back keyed by your own custom_id, in any order.

Run:  ANTHROPIC_API_KEY=... uv run batch.py
"""
import time
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

client = anthropic.Anthropic()
TICKETS = [
    "Charged twice for order 5521", "App crashes when I open settings", "Cannot log in after password reset",
    "Need a VAT invoice for March", "Export to CSV is missing columns", "Please close my account",
    "Refund still not received after 10 days", "Dashboard loads blank in Safari", "Two-factor codes never arrive",
    "Change billing email to finance@", "API returns 500 on /orders", "Add a new admin user",
] * 4  # 48 tickets, a stand-in for a night's backlog

batch = client.messages.batches.create(requests=[
    Request(custom_id=f"ticket-{i:03d}", params=MessageCreateParamsNonStreaming(
        model="claude-opus-5-5", max_tokens=512, output_config={"effort": "low"},
        messages=[{"role": "user", "content": f"Label this support ticket as billing, bug or account. Reply with the label only.\n\n{t}"}]))
    for i, t in enumerate(TICKETS)])
print(f"batch {batch.id}: {len(TICKETS)} requests submitted")

start = time.time()
while client.messages.batches.retrieve(batch.id).processing_status != "ended":
    time.sleep(20)
print(f"ended after {time.time() - start:.0f}s")

labels, ok = {}, 0
for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        ok += 1
        text = "".join(b.text for b in result.result.message.content if b.type == "text").strip().lower()
        labels[text] = labels.get(text, 0) + 1
print(f"{ok} of {len(TICKETS)} succeeded; labels: {labels}")
