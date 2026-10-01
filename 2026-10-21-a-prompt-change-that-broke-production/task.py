"""An eval for a ticket router. Each sample has a stable id, so a grown dataset
can be topped up: only the new samples run, the rest are reused."""
import json
from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import includes
from inspect_ai.solver import generate


@task
def ticket_router():
    cases = json.load(open("cases.json"))
    return Task(dataset=[Sample(id=c["id"], input=c["input"], target=c["target"]) for c in cases], solver=generate(), scorer=includes())
