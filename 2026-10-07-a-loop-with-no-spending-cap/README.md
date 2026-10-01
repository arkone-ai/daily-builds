# A loop with no spending cap: give the agent a task budget

**Beta** · [Anthropic docs](https://platform.claude.com/docs/en/build-with-claude/task-budgets) · header `task-budgets-2026-03-13`

**The failure.** An agent loop has no idea what it costs. It keeps reading, calling and retrying until the task is done or someone notices the bill.

**The fix.** `output_config.task_budget` tells the model how many tokens the whole loop may use. It sees a countdown and paces itself. It is advisory, not a hard cap: `max_tokens` is still the per-response ceiling. The minimum is 20,000.

```bash
ANTHROPIC_API_KEY=... uv run budget.py
```

**Our run, 2 October 2026**, the same audit of 60 files:

| | Tokens over the loop | Tool calls | Answer |
|---|---|---|---|
| No budget | 161,329 | 61 | Complete: 40 modules flagged |
| 30,000-token budget | 63,386 | 23 | Partial, and it said which files it had not read |

> A budget does not make the work cheaper. It makes the agent stop and say what is left. Size it to the job, and pair it with paged tools (6 October) so each step costs less.

"Tokens over the loop" adds every request's input and output, so it counts re-sent history; the budget counts what the model generates and the tool results it reads.

Needs: an Anthropic API key and [uv](https://docs.astral.sh/uv/). Cost of one run at list price: about $1.20.
