# One agent is too slow: fan out to parallel subagents

**Released** 29 September 2026 · [OpenAI changelog](https://developers.openai.com/api/docs/changelog) · [multi-agent guide](https://developers.openai.com/api/docs/guides/responses-multi-agent)

With multi-agent (beta) on the Responses API, one request splits the work across parallel subagents and the root agent reconciles what they find. `review.py` is OpenAI's own quickstart, run on `sample.diff`: a refund function with a SQL injection, a missing guard and no tests.

```bash
OPENAI_API_KEY=... uv run review.py
```

Status: written from OpenAI's guide on 2 October 2026 and not yet run by us; the recording is its first run.

Needs: an OpenAI API key with access to `gpt-6.1-sol` and [uv](https://docs.astral.sh/uv/).
