# A human has to approve this step: typed interrupts

**Released** 21 September 2026 in LangGraph 1.2.12 · [release](https://github.com/langchain-ai/langgraph/releases/tag/1.2.12)

**The failure.** An agent pauses for approval and the human types something free-form. "maybe", "ok I guess", "ask finance": the harness has to guess what that means, and a wrong guess moves money.

**The fix.** `interrupt()` takes a `response_schema`. Pass a Pydantic model and the client can render it as a form, and the resume value is validated against it. The graph continues only on a real answer, and `interrupt()` returns the typed object.

```bash
uv run approve.py
```

**Our run, 2 October 2026:** a $1,240 refund paused for a manager. Resuming with `decision: "maybe"` was rejected ("Input should be 'approve' or 'reject'"); resuming with `approve` from Asha completed it.

Needs: [uv](https://docs.astral.sh/uv/). No API key; no LLM in the loop.
