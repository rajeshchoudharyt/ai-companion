from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

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

checkpointer = InMemorySaver()
agent = graph.compile(checkpointer=checkpointer)


def run_agent(query: str, config: RunnableConfig):
    agent.invoke(WorkingState(query=query), config)
    return agent