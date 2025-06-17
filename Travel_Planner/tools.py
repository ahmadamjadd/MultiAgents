# tools.py
from langchain.chains.llm_math.base import LLMMathChain
from langchain.agents import Tool
from langchain_tavily import TavilySearch
from langchain_community.tools import DuckDuckGoSearchRun


def get_tools(llm):
    # Math tool using LLM MathChain
    problem_chain = LLMMathChain.from_llm(llm=llm)
    math_tool = Tool.from_function(
        name="Calculator",
        func=problem_chain.run,
        description="Useful for math questions. Only input math expressions."
    )

    # Tavily Search tool
    search_tool = TavilySearch()
    search = DuckDuckGoSearchRun()


    return {
        "calculator": math_tool,
        "search": search_tool,
        "search2": search
    }
