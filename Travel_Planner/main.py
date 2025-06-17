# main.py
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel
from typing import Literal, Annotated, Sequence, TypedDict
import operator
from dotenv import load_dotenv
load_dotenv()


from agents import (
    llm, destination_expert_node, budget_planner_node,
    itinerary_builder_node
)
from prompts import supervisor_template, options, members

# ----- Supervisor Agent -----
class routeResponse(BaseModel):
    next: Literal[*options]

def supervisor_agent(state):
    chain = supervisor_template | llm.with_structured_output(routeResponse)
    return chain.invoke(state)

# ----- AgentState -----
class AgentState(TypedDict):
    messages: Annotated[Sequence[HumanMessage], operator.add]
    next: str

# ----- Build Graph -----
workflow = StateGraph(AgentState)
workflow.add_node("Destination Expert", destination_expert_node)
workflow.add_node("Budget Planner", budget_planner_node)
workflow.add_node("Itinerary Builder", itinerary_builder_node)
workflow.add_node("supervisor", supervisor_agent)

# Workflow edges
for member in members:
    workflow.add_edge(member, "supervisor")

workflow.add_conditional_edges("supervisor", lambda x: x["next"], {k: k for k in members} | {"FINISH": END})
workflow.add_edge(START, "supervisor")

graph = workflow.compile()

from langsmith import traceable

@traceable
def run_graph():
    for step in graph.stream({
        "messages": [
            HumanMessage(content="I want to visit Islamabad with a budget of Rs5000")
        ]
    }):
        if "__end__" not in step:
            print(step)
            print("----")

if __name__ == "__main__":
    run_graph()


