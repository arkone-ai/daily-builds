# Three hundred tools, one wrong pick: let the model search

[Anthropic docs: tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)

**The failure.** An enterprise agent connected to an ERP, a CRM and a ticketing system ends up with hundreds of tools. Every definition is sent on every turn, and the more similar tools there are, the easier it is to pick the wrong one.

**The fix.** Mark the tools `defer_loading: true` and add the tool search tool (`tool_search_tool_bm25_20251119`). The model starts with the search tool alone, finds the few tools it needs, and only those are loaded.

```bash
ANTHROPIC_API_KEY=... uv run search.py
```

**Our run, 2 October 2026**, 300 ERP tools:

| | Input tokens per turn |
|---|---|
| All 300 loaded up front | 29,811 |
| Deferred, with search | 673 |

Asked to reject refund REF-2291, the model searched for "reject refund" and called `reject_refund` with `id: "REF-2291"`.

> Never defer everything: the search tool itself and at least one tool must stay loaded.

Needs: an Anthropic API key and [uv](https://docs.astral.sh/uv/).
