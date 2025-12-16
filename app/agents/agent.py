from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel

from app.agents.schemas import Fivetuple, Message
from app.agents.nodes import input_normalizer, memory_extractor

class WorkingState(BaseModel):
    memory: list[Fivetuple] = []
    messages: list[Message] = []
    query: str = ""
    

# Graph workflow
graph = StateGraph(WorkingState)

# Nodes
graph.add_node("input_normalizer", input_normalizer)
graph.add_node("memory_extractor", memory_extractor)

# Edges
graph.add_edge(START, "input_normalizer")
graph.add_edge("input_normalizer", "memory_extractor")
graph.add_edge("memory_extractor", END)

agent = graph.compile()

def run_agent(query: str):
    agent.invoke(WorkingState(query=query))