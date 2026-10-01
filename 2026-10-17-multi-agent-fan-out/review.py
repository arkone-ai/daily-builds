# /// script
# requires-python = ">=3.10"
# dependencies = ["openai"]
# ///
"""One API call, three reviewers working on the same pull request at once.

GPT-6.1 Sol supports multi-agent in the Responses API (beta): one request splits
the work across parallel subagents and the root agent reconciles their findings.
This follows OpenAI's own quickstart and runs it on sample.diff.

Run:  OPENAI_API_KEY=... uv run review.py
"""
from openai import OpenAI

client = OpenAI()
diff = open("sample.diff", encoding="utf-8").read()

response = client.beta.responses.create(
    model="gpt-6.1-sol",
    input=(
        "Review the pull-request diff below with three agents: one for "
        "correctness, one for security, and one for missing tests. "
        "Reconcile duplicate or conflicting findings, then return a "
        "prioritized review with file and line references.\n\n"
        f"<diff>\n{diff}\n</diff>"
    ),
    multi_agent={"enabled": True, "max_concurrent_subagents": 3},
    betas=["responses_multi_agent=v1"],
)

agents = sorted({item.agent.agent_name for item in response.output if getattr(item, "agent", None)})
print("agents that worked on it:", ", ".join(agents), "\n")
print("".join(
    part.text
    for item in response.output
    if item.type == "message" and item.agent is not None
    and item.agent.agent_name == "/root" and item.phase == "final_answer"
    for part in item.content if part.type == "output_text"
))
