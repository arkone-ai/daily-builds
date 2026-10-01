# /// script
# requires-python = ">=3.10"
# dependencies = ["langgraph>=1.2.12", "langgraph-checkpoint-sqlite"]
# ///
"""Kill an agent halfway and most harnesses start again from step 1, repeating every side effect.

The fix: checkpoint the state after every step to durable storage, keyed by a
thread id. After a crash, the same thread id resumes from the last checkpoint.
The first run here crashes at step 7 of 9; the second run finishes without
redoing steps 1 to 6.

Run:  uv run resume.py   (twice: the first run crashes on purpose)
"""
import os
import sqlite3
from typing import Annotated, TypedDict
from operator import add
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

CRASH_FLAG = "crashed-once"


class State(TypedDict):
    done: Annotated[list[int], add]


def step(n):
    def run(state: State):
        if n == 7 and not os.path.exists(CRASH_FLAG):
            open(CRASH_FLAG, "w").close()
            raise RuntimeError("process killed at step 7")
        with open("side_effects.log", "a") as f:
            f.write(f"step {n} sent an email\n")
        print(f"step {n} done")
        return {"done": [n]}
    return run


graph = StateGraph(State)
for n in range(1, 10):
    graph.add_node(f"s{n}", step(n))
graph.add_edge(START, "s1")
for n in range(1, 9):
    graph.add_edge(f"s{n}", f"s{n + 1}")
graph.add_edge("s9", END)

saver = SqliteSaver(sqlite3.connect("checkpoints.db", check_same_thread=False))
app = graph.compile(checkpointer=saver)
config = {"configurable": {"thread_id": "invoice-run-42"}}
started = app.get_state(config).next
if started:
    print("resuming from the checkpoint, next:", started)
try:
    result = app.invoke(None if started else {"done": []}, config)
    print("finished, steps done:", result["done"])
    print(open("side_effects.log").read().count("sent an email"), "emails sent in total, one per step")
except RuntimeError as e:
    print(f"CRASH: {e}. Run the script again.")
