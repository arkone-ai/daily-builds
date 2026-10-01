# A prompt change that broke production: run the eval set, top it up

**Released** 25 September 2026 in Inspect 0.3.270 (UK AI Security Institute) · [changelog](https://github.com/UKGovernmentBEIS/inspect_ai/blob/main/CHANGELOG.md)

**The failure.** Agents regress quietly. A prompt edit, a model upgrade or a new tool changes behaviour, and the first report is a customer. Evals that are slow or costly to re-run stop being run.

**The fix.** Keep an eval set with a stable `id` on every sample and run it before every change ships. Since Inspect 0.3.270, `eval_set` tops up a grown dataset in place: adding cases runs only the new ones and reuses the rest.

```bash
./run.sh
```

`task.py` is a ticket-router eval over `cases.json`. `run.sh` runs it, adds two cases, and runs it again. It uses Inspect's mock model so it costs nothing; pass a real model with `--model` (for example `anthropic/claude-opus-5-5`) to measure accuracy.

**Our run, 2 October 2026:** after the dataset grew from 10 to 12 cases, the log held 12 samples. Cases 1 to 10 carried the first run's timestamp; only cases 11 and 12 ran again. (The mock model scores 0% because it returns placeholder text; it is here to show the mechanics.)

Needs: [uv](https://docs.astral.sh/uv/). No API key with the mock model.
