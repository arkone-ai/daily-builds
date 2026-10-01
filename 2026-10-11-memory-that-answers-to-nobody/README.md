# Memory that answers to nobody: store the judgement, with its reason

**A rule from ArkOne's production platform:** the platform stores and serves; agents compute.

**The failure.** A harness asks a model for a score, a summary or a classification every time a page or another agent needs it. Each view costs money, the value changes from one view to the next, and nobody can say who decided it or why.

**The fix.** The agent computes the judgement once and writes it through a tool: the value, the reason, who wrote it, when. Every later read is free and identical. A judgement nobody has written yet renders as absent, never as 0, so "unknown" can never pass for "bad".

```bash
ANTHROPIC_API_KEY=... uv run judgements.py
```

**Our run, 2 October 2026:** before scoring, the account's fit score read as absent. One agent call stored 72 with its reason ("quotes and fleet scheduling still run in spreadsheets; lowered because they did not reply to the last email") and author `claude-opus-5-5 (agent)`. Two page loads then returned the same judgement with 0 model calls.

Needs: an Anthropic API key and [uv](https://docs.astral.sh/uv/).
