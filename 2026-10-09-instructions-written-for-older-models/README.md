# Instructions written for older models: audit the harness config

**Released** 25 September 2026 in Claude Code v2.1.283 · [release](https://github.com/anthropics/claude-code/releases/tag/v2.1.283)

**The failure.** A harness's instructions (`CLAUDE.md`, skills, agents, commands) pile up over model generations. Shouting, forced step-by-step thinking, "double-check three times", fixed progress reports every N tool calls: written to steer older models, they make newer ones slower, wordier or worse.

**The fix.** In Claude Code, run `/doctor prompt-audit`. It reads the configuration files and ranks the patterns written for older models, with a proposed fix for each.

This folder's `CLAUDE.md` is a deliberately dated example. To record:

```bash
cd 2026-10-09-instructions-written-for-older-models
claude
# then type:  /doctor prompt-audit
```

Accept one fix on screen and show the diff.

Needs: Claude Code v2.1.283 or later.
