# Why the prompt cache missed: ask the API

**Generally available** 23 September 2026 · [Anthropic release notes](https://platform.claude.com/docs/en/release-notes/api)

Pass `diagnostics: {previous_message_id: ...}` on a Messages request and, when the prompt cache misses, the response says what changed since that previous request (the model, the system prompt, the tools or the message history) and how many tokens missed.

```bash
ANTHROPIC_API_KEY=... uv run cache.py
```

**Our run, 2 October 2026:** request 1 wrote 11,084 tokens to the cache, request 2 read all 11,084, and after one word changed in the system prompt request 3 read none and reported `system_changed`, 9,500 tokens missed.

> A cache miss costs the full input price again. Diagnostics turns "why is this expensive" into one field.

Needs: an Anthropic API key and [uv](https://docs.astral.sh/uv/). Cost of one run at list price: about $0.15.
