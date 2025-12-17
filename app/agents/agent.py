import json
from langgraph.graph import StateGraph, START, END
from app.agents.schemas import WorkingState
from app.agents.nodes import input_normalizer, memory_extractor

 
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
    store = agent.invoke(WorkingState(query=query))
    print("store", json.dumps(store, indent=4))