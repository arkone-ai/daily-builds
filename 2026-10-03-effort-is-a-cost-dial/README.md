# Effort is a cost dial: Claude Opus 5.5 at medium and max

**Released** 22 September 2026 · [Anthropic release notes](https://platform.claude.com/docs/en/release-notes/api)

Claude Opus 5.5 always thinks. You steer how much with `output_config.effort` (`low`, `medium`, `high`, `xhigh`, `max`); the default is `medium`. This script asks for the same code review at `medium` and at `max` and prints the tokens and time each used.

```bash
ANTHROPIC_API_KEY=... uv run effort.py
```

**Our run, 2 October 2026:** `max` used 13,414 output tokens and 149 seconds; `medium` used 546 and 9 seconds. Both found the same five core bugs. `max` added one (a generator breaks `len()`).

> Pick effort per task. Most everyday work does not need `max`.

Needs: an Anthropic API key and [uv](https://docs.astral.sh/uv/). Cost of one run at list price: about $0.28.
