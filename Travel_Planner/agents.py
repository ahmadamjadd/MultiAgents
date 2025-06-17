# agents.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
import functools

from tools import get_tools
from prompts import destination_expert_prompt, budget_planner_prompt, itinerary_builder_prompt

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# Instantiate LLM
llm = ChatGroq(model="qwen/qwen3-32b", temperature=0.5)

# Tools
tools = get_tools(llm)

# Create agents
destination_expert_agent = create_react_agent(llm, tools=[tools["search2"]], prompt=destination_expert_prompt)
budget_planner_agent = create_react_agent(llm, tools=[tools["calculator"], tools["search2"]], prompt=budget_planner_prompt)
itinerary_builder_agent = create_react_agent(llm, tools=[], prompt=itinerary_builder_prompt)

# Agent wrapper node
def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name=name)]
    }

# Agent node functions (for graph)
destination_expert_node = functools.partial(agent_node, agent=destination_expert_agent, name="Destination Expert")
budget_planner_node = functools.partial(agent_node, agent=budget_planner_agent, name="Budget Planner")
itinerary_builder_node = functools.partial(agent_node, agent=itinerary_builder_agent, name="Itinerary Builder")

__all__ = [
    "llm",
    "destination_expert_node",
    "budget_planner_node",
    "itinerary_builder_node"
]

