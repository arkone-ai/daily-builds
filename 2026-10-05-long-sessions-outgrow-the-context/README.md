# Long sessions outgrow the context: compact on demand

**Beta** since 14 September 2026 · [Anthropic docs](https://platform.claude.com/docs/en/build-with-claude/compaction-on-demand)

**The failure.** An agent that runs all day fills its context window. Either the request fails, or the harness drops old turns and the agent forgets what it was told at the start.

**The fix.** Your harness decides when to compact. Send the conversation with `compaction: {"type": "summarize"}` and the `compact-2026-09-04` beta header; the API returns one signed `compaction` block. Put that block first in `messages`, drop the turns it replaced, and keep sending it on every later request.

```bash
ANTHROPIC_API_KEY=... uv run compact.py
```

**Our run, 2 October 2026:** a migration agent was given a goal and a hard constraint, then 599 lines of progress log. Compaction took the history from 16,879 tokens to 226. Asked afterwards, the agent named the goal, the constraint ("never drop `legacy_tax_code`") and the batch to resume from.

> Compact before you hit the limit, not after: the request that asks for the summary still has to fit.

Needs: an Anthropic API key and [uv](https://docs.astral.sh/uv/).
