# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""An agent that can delete a record will one day delete the wrong one.

The fix, a rule on every destructive tool on our MCP server: it takes a
`confirm` argument that must equal the exact id of the record being changed.
A refusal tells the agent what to do. The agent has to look the record up and
name it, so a vague instruction cannot turn into a wrong delete.

Run:  ANTHROPIC_API_KEY=... uv run confirm.py
"""
import json
import anthropic

client = anthropic.Anthropic()
INVOICES = {"INV-0410": ("Acme Trading", 1200.0), "INV-0411": ("Acme Trading", 1200.0), "INV-0412": ("Acme Trading", 860.0)}


def list_invoices(customer):
    return [{"id": k, "customer": c, "amount": a} for k, (c, a) in INVOICES.items() if c == customer]


def delete_invoice(invoice_id, confirm=""):
    if invoice_id not in INVOICES:
        return {"error": f"No invoice {invoice_id}."}
    if confirm != invoice_id:
        return {"refused": f"Deleting is permanent. Look the invoice up, then call again with confirm set to exactly '{invoice_id}'."}
    del INVOICES[invoice_id]
    return {"deleted": invoice_id}


TOOLS = [
    {"name": "list_invoices", "description": "List a customer's invoices.",
     "input_schema": {"type": "object", "properties": {"customer": {"type": "string"}}, "required": ["customer"]}},
    {"name": "delete_invoice", "description": "Permanently delete one invoice. Requires confirm equal to the exact invoice id.",
     "input_schema": {"type": "object", "properties": {"invoice_id": {"type": "string"}, "confirm": {"type": "string"}}, "required": ["invoice_id"]}},
]
FUNCS = {"list_invoices": list_invoices, "delete_invoice": delete_invoice}
print("a delete with no confirm:", json.dumps(delete_invoice("INV-0412")))
print("a delete with the wrong confirm:", json.dumps(delete_invoice("INV-0412", confirm="INV-0410")), "\n")
messages = [{"role": "user", "content": "Acme Trading was invoiced twice for the same 1,200 AED order. Delete the duplicate."}]
while True:
    r = client.messages.create(model="claude-opus-5-5", max_tokens=4096, output_config={"effort": "low"}, tools=TOOLS, messages=messages)
    messages.append({"role": "assistant", "content": r.content})
    uses = [b for b in r.content if b.type == "tool_use"]
    if not uses:
        break
    results = []
    for u in uses:
        out = FUNCS[u.name](**u.input)
        print(f"{u.name}({json.dumps(u.input)}) -> {json.dumps(out)}")
        results.append({"type": "tool_result", "tool_use_id": u.id, "content": json.dumps(out)})
    messages.append({"role": "user", "content": results})
print("\nagent:", "".join(b.text for b in r.content if b.type == "text"))
print("invoices left:", list(INVOICES))
