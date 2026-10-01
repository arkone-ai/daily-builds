# Nobody can say what the agent did: log every tool call

**A rule from ArkOne's production platform.**

**The failure.** After an agent mistake the first question is "what exactly did it do?" Without a record of every call, the answer is a guess reconstructed from side effects.

**The fix.** Route every tool through one wrapper that appends an event before and after the call: run id, tool, arguments, result or error, duration, time. Append-only JSON lines are enough to start; in production send the same events to your log store.

```bash
ANTHROPIC_API_KEY=... uv run audit.py
```

**Our run, 2 October 2026:** asked to reserve stock for an order, the agent reserved SKU-1 and SKU-3, was refused SKU-2 (not enough stock), then checked SKU-2's stock. The replay prints each of those events in order with its arguments and result.

> Log the arguments as the agent sent them, before your code changes anything. That is the record you need when a call went wrong.

Needs: an Anthropic API key and [uv](https://docs.astral.sh/uv/).
