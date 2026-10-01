# Write tools with no brakes: confirm equals the exact id

**A rule from ArkOne's production MCP server**, where every destructive tool works this way.

**The failure.** An agent with a delete tool acts on a vague instruction ("delete the duplicate", "clean up the old ones") and one day removes the wrong record. Nothing in the tool made it stop and name what it was about to destroy.

**The fix.** Every destructive tool takes a `confirm` argument that must equal the exact id of the record being changed. Without it the tool refuses, and the refusal says what to do. The agent has to look the record up and name it; a guess cannot pass. In a product with a human in the loop, `confirm` is what the human types.

```bash
ANTHROPIC_API_KEY=... uv run confirm.py
```

**Our run, 2 October 2026:** direct calls with no `confirm`, and with the wrong one, were refused. Asked to delete Acme Trading's duplicate 1,200 AED invoice, the agent listed the invoices, then called `delete_invoice(invoice_id="INV-0411", confirm="INV-0411")` and kept the original INV-0410.

Needs: an Anthropic API key and [uv](https://docs.astral.sh/uv/).
