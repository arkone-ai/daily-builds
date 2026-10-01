# A tool reply that eats the context: one page and the true total

**A rule from ArkOne's production MCP server**, which serves a CRM with tens of thousands of records to agents.

**The failure.** One of our list tools once returned 2 MB in a single reply. The agent could not finish its task, and the next tool had already copied the same habit.

**The fix.** Every list tool returns one page, the true `total` for the filter, and `next_offset` (null on the last page). The agent can see that more exists and ask for it, or answer from the total without reading every row. The total is not optional: it is what makes a missing page visible.

```bash
ANTHROPIC_API_KEY=... uv run paged.py
```

**Our run, 2 October 2026**, 20,000 invoices:

| | Tokens |
|---|---|
| The whole table as one tool reply | 821,862 |
| One page with the total | 846 |
| The full agent run answering "how many are overdue, and the three largest" | 1,659 |

The agent made one call (`status=overdue, sort_by_amount, limit=3`) and read the count from `total`.

Needs: an Anthropic API key and [uv](https://docs.astral.sh/uv/).
