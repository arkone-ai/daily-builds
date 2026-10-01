# Ollama decision models: ticket triage with a confidence score

**Released** 28 September 2026 in Ollama v0.35.0 · [release notes](https://github.com/ollama/ollama/releases/tag/v0.35.0)

Decision models return a choice and a probability for each option instead of text, through the new `/v1/systemone` endpoint. No prompt to write, no output to parse. This script labels three support tickets as billing, bug or account and prints how sure the model was.

```bash
ollama pull nimble
./triage.sh
```

Needs: Ollama 0.35.0 or later, `jq`, about 10 GB of disk for Nimble. Runs fully on your machine; no API key.
