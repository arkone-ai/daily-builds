# The agent forgets between sessions: a memory layer you control

[Anthropic docs: memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) · tool type `memory_20250818`

**The failure.** Every agent session starts from an empty context. Monday's session learned the customer's rules; Tuesday's has never heard of them, so the user repeats themselves or the agent gets it wrong.

**The fix.** Give the agent a memory tool: it can view, create, edit and delete files in a memory directory, and it checks that memory before it acts. The storage is yours. The Python SDK ships `BetaLocalFilesystemMemoryTool` for a local folder; in production, implement the same six commands over your database, scoped per customer or per tenant.

```bash
ANTHROPIC_API_KEY=... uv run memory.py
```

**Our run, 2 October 2026:** session 1 was told Acme Trading's rules (AED, net-45, no emails to finance before 9am Gulf time) and saved them to `memories/customers/acme_trading.md`. Session 2, a fresh conversation with no history, was asked only to draft a payment reminder. It read the file and wrote the reminder in AED, on net-45 terms, to be sent at 9am Gulf time or later.

> Memory is data. Decide what may be written, who can read it, and when it expires, as you would for any other table.

Needs: an Anthropic API key and [uv](https://docs.astral.sh/uv/).
