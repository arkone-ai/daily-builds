#!/usr/bin/env bash
# Ticket triage on a laptop, with a confidence score and no prompt parsing.
#
# Ollama v0.35.0 added /v1/systemone: decision models that return a choice and a
# probability for each option instead of text. This sends three support tickets
# to Nimble, routes each to its queue, and sends any ticket the model is less
# than 80% sure about to a person instead.
#
# Needs: Ollama 0.35.0 or later, jq.   Run:  ollama pull nimble && ./triage.sh
set -euo pipefail

tickets=(
  "Our checkout has returned 500 errors since 9am."
  "I was charged twice for the same order last week."
  "The reset-password email never arrives."
)

for ticket in "${tickets[@]}"; do
  jq -n --arg state "$ticket" '{
    model: "nimble",
    state: $state,
    questions: { label: {
      type: "choice",
      instructions: "Which label fits this ticket?",
      criteria: {
        billing: "Payments and refunds",
        bug: "Software errors",
        account: "Login and account access"
      }
    } }
  }' \
  | curl -s http://localhost:11434/v1/systemone -H 'Content-Type: application/json' -d @- \
  | jq -r --arg t "$ticket" '.answers.label as $a
      | ($a.probabilities[$a.choice]) as $p
      | (if $p >= 0.8 then "queue:\($a.choice)" else "to a person" end) as $route
      | "\($route)\t\($p * 100 | floor)%\t\($t)"'
done
