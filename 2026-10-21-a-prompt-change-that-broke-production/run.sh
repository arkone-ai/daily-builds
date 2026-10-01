#!/usr/bin/env bash
# Run the eval set, add two cases, run it again: only the two new ones run.
# Uses Inspect's mock model, so no API key is needed; swap in a real model with --model.
set -euo pipefail
rm -rf logs
uvx --from 'inspect-ai>=0.3.270' inspect eval-set task.py --model mockllm/model --log-dir logs 2>&1 | tail -4
python3 - <<'PY'
import json
cases = json.load(open("cases.json"))
cases += [{"id": "case-11", "input": "Label this ticket billing, bug or account: API 500 on /orders", "target": "bug"},
          {"id": "case-12", "input": "Label this ticket billing, bug or account: Add a new admin user", "target": "account"}]
json.dump(cases, open("cases.json", "w"), indent=1)
PY
echo "--- dataset grew from 10 to 12 cases; running again"
uvx --from 'inspect-ai>=0.3.270' inspect eval-set task.py --model mockllm/model --log-dir logs 2>&1 | tail -6
