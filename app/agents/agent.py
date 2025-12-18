from langgraph.graph import StateGraph, START, END
from app.agents.schemas import WorkingState
from app.agents.nodes import input_normalizer, memory_extractor, personality_analyzer, personality_engine

 
# Graph workflow
graph = StateGraph(WorkingState)

# Nodes
graph.add_node("input_normalizer", input_normalizer)
graph.add_node("memory_extractor", memory_extractor)
graph.add_node("personality_analyzer", personality_analyzer)
graph.add_node("personality_engine", personality_engine)

# Edges
graph.add_edge(START, "input_normalizer")
graph.add_edge("input_normalizer", "memory_extractor")
graph.add_edge("memory_extractor", "personality_analyzer")
graph.add_edge("personality_analyzer", "personality_engine")
graph.add_edge("personality_engine", END)

store = {}
agent = graph.compile()

def run_agent(query: str, user_id: str):
    user_exist = user_id in store

    working_state:WorkingState
    if user_exist:
        store[user_id]["query"] = query
        working_state = WorkingState.model_validate(store[user_id])
    else:
        working_state = WorkingState(query=query)
    
    store[user_id] = agent.invoke(working_state)

    return store[user_id]
    