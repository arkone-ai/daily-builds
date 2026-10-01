# /// script
# requires-python = ">=3.10"
# dependencies = ["langgraph>=1.2.12", "pydantic"]
# ///
"""Free-text approvals let an agent read "maybe" as yes.

The fix: pause the graph with a typed interrupt. interrupt() takes a
response_schema; a Pydantic model is shown to the client as a form and the
resume value is validated against it, so the graph only continues on a real
answer. No LLM needed to see it.

Run:  uv run approve.py
"""
from typing import Literal, TypedDict
from pydantic import BaseModel, ValidationError
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class Approval(BaseModel):
    decision: Literal["approve", "reject"]
    approver: str


class State(TypedDict):
    refund: float
    status: str


def ask_manager(state: State):
    answer = interrupt(f"Refund of ${state['refund']:,.2f} needs a manager.", response_schema=Approval)
    return {"status": f"{answer.decision}d by {answer.approver}"}


graph = StateGraph(State)
graph.add_node("ask_manager", ask_manager)
graph.add_edge(START, "ask_manager")
graph.add_edge("ask_manager", END)
app = graph.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "refund-2291"}}

paused = app.invoke({"refund": 1240.0, "status": "pending"}, config)
print("paused:", paused["__interrupt__"][0].value)

for reply in ({"decision": "maybe", "approver": "Asha"}, {"decision": "approve", "approver": "Asha"}):
    try:
        result = app.invoke(Command(resume=reply), config)
        print("resumed with", reply, "->", result["status"])
    except ValidationError as e:
        print("rejected", reply, "->", e.errors()[0]["msg"])
