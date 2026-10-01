# The agent crashed at step 7 of 9: checkpoint and resume

[LangGraph persistence](https://github.com/langchain-ai/langgraph)

**The failure.** A long agent run dies halfway: a deploy, an out-of-memory kill, a timeout. Most harnesses start again from step 1, and every side effect before the crash (emails, API writes, charges) happens twice.

**The fix.** Compile the graph with a durable checkpointer and a `thread_id`. State is saved after every step. Run the same thread again and it resumes from the last checkpoint.

```bash
uv run resume.py   # crashes at step 7 on purpose
uv run resume.py   # resumes at step 7 and finishes
```

**Our run, 2 October 2026:** run 1 completed steps 1 to 6 and crashed at step 7. Run 2 reported "resuming from the checkpoint, next: s7", ran steps 7 to 9, and the log shows 9 emails in total, one per step.

> Resuming is only safe if each step is safe to retry. The crashed step runs again, so make side effects idempotent.

Needs: [uv](https://docs.astral.sh/uv/). No API key.
