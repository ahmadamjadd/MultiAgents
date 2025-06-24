# === agents.py ===

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from tools import extract_report_text, load_health_retriever_tool
from prompts import extract_agent_prompt, doctor_agent_prompt

load_dotenv()


groq_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    api_key=groq_key
)



# Agent 1: Extractor
extract_agent = create_react_agent(
    llm=llm,
    tools=[extract_report_text],
    prompt=extract_agent_prompt
)
extract_agent_executor = AgentExecutor(agent=extract_agent, tools=[extract_report_text], verbose=True, handle_parsing_errors=True)

# Agent 2: Doctor
retriever_tool = load_health_retriever_tool()
pubmed_tool = PubmedQueryRun()

tools = [retriever_tool, pubmed_tool]
doctor_agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=doctor_agent_prompt
)
doctor_agent_executor = AgentExecutor(agent=doctor_agent, tools=tools, verbose=True, handle_parsing_errors=True)