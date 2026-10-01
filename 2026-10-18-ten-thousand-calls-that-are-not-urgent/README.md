# Ten thousand calls that are not urgent: send them as a batch

[Anthropic docs: Message Batches](https://platform.claude.com/docs/en/build-with-claude/batch-processing)

**The failure.** Backfills, nightly re-scoring and bulk classification go through the live API one request at a time: full price, fighting live traffic for rate limits, and a retry loop to babysit.

**The fix.** Anything that can wait goes into one Message Batch. Each request is billed at half the standard price, batches do not compete with live traffic, and results come back keyed by your own `custom_id`, in any order, so match on the id, never on position.

```bash
ANTHROPIC_API_KEY=... uv run batch.py
```

**Our run, 2 October 2026:** 48 ticket-labelling requests in one batch, ended after 225 seconds, 48 of 48 succeeded. Labels came back as 16 bug, 17 account and 15 billing; the inputs had 16 billing tickets, so one landed as account, which is why bulk labels still deserve a spot check.

Needs: an Anthropic API key and [uv](https://docs.astral.sh/uv/). Most batches end within an hour; the limit is 24 hours.
