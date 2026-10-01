# Agent harness engineering, one fix a day

How production AI agents are built: one failure that real agent harnesses hit, and the code that fixes it. One folder per day, each with a README naming the problem, the fix, its source, and the numbers from our own run.

| Day | The failure | The fix | Folder |
|---|---|---|---|
| **Week 1** | **The loop and context** | | |
| 3 Oct | Max effort used 24x the tokens for almost the same answer | Set effort per step | [`2026-10-03-effort-is-a-cost-dial`](2026-10-03-effort-is-a-cost-dial) |
| 4 Oct | The bill jumps and nothing says why | Cache diagnostics name the change | [`2026-10-04-why-the-prompt-cache-missed`](2026-10-04-why-the-prompt-cache-missed) |
| 5 Oct | Long sessions outgrow the context | Compact on demand: 16,879 tokens to 226 | [`2026-10-05-long-sessions-outgrow-the-context`](2026-10-05-long-sessions-outgrow-the-context) |
| 6 Oct | A tool reply that eats the context | One page and the true total: 821,862 tokens to 846 | [`2026-10-06-a-tool-reply-that-eats-the-context`](2026-10-06-a-tool-reply-that-eats-the-context) |
| 7 Oct | A loop with no spending cap | A task budget the model can see | [`2026-10-07-a-loop-with-no-spending-cap`](2026-10-07-a-loop-with-no-spending-cap) |
| 8 Oct | Three hundred tools, one wrong pick | Deferred tools and tool search: 29,811 tokens to 673 | [`2026-10-08-three-hundred-tools-one-wrong-pick`](2026-10-08-three-hundred-tools-one-wrong-pick) |
| 9 Oct | Instructions written for older models | Audit the harness config | [`2026-10-09-instructions-written-for-older-models`](2026-10-09-instructions-written-for-older-models) |
| **Week 2** | **Memory and state** | | |
| 10 Oct | The agent forgets between sessions | A memory tool over storage you control | [`2026-10-10-the-agent-forgets-between-sessions`](2026-10-10-the-agent-forgets-between-sessions) |
| 11 Oct | Memory that answers to nobody | Store each judgement with its reason and author | [`2026-10-11-memory-that-answers-to-nobody`](2026-10-11-memory-that-answers-to-nobody) |
| 12 Oct | A human has to approve this step | A typed interrupt that rejects "maybe" | [`2026-10-12-a-human-has-to-approve-this-step`](2026-10-12-a-human-has-to-approve-this-step) |
| 13 Oct | The agent crashed at step 7 of 9 | Checkpoint every step, resume at 7 | [`2026-10-13-the-agent-crashed-at-step-7`](2026-10-13-the-agent-crashed-at-step-7) |
| 14 Oct | Write tools with no brakes | confirm must equal the exact id | [`2026-10-14-write-tools-with-no-brakes`](2026-10-14-write-tools-with-no-brakes) |
| 15 Oct | Nobody can say what the agent did | Log every tool call as an event | [`2026-10-15-nobody-can-say-what-the-agent-did`](2026-10-15-nobody-can-say-what-the-agent-did) |
| 16 Oct | Routing with a coin flip | A decision model with a probability; low confidence goes to a person | [`2026-10-16-routing-with-confidence`](2026-10-16-routing-with-confidence) |
| **Week 3** | **Scale and safety** | | Coming 17 to 23 Oct |

Folders for week 3 already here: [`multi-agent fan-out`](2026-10-17-multi-agent-fan-out) (17 Oct), [`MCP across frameworks`](2026-10-22-mcp-across-frameworks) (22 Oct).

**Watch them:** [Instagram @arkoneai](https://www.instagram.com/arkoneai/) · [X @arkone_ai](https://x.com/arkone_ai)
**One email a week with all of them:** [arkone.ai/go/builds](https://arkone.ai/go/builds?utm_source=github&utm_medium=readme&utm_campaign=builds-2026q4)

Every script runs with [uv](https://docs.astral.sh/uv/): `uv run <file>.py`. Built by [ArkOne AI](https://arkone.ai), an Anthropic Partner and OpenAI Select Partner. MIT licensed.
