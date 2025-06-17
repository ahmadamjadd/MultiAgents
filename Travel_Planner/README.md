# 🧭 Multi-Agent Travel Planner

This is a **Multi-Agent AI Travel Planner** powered by LangChain, LangGraph, and LangSmith. The goal is to simulate a team of intelligent agents collaborating to plan a personalized trip based on the user's preferences, destination, and budget.

Each agent performs a specialized task — just like a team of human travel consultants.

## 🛠️ Technologies Used

- [LangChain](https://www.langchain.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangSmith](https://smith.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [DuckDuckGo Search Tool](https://python.langchain.com/docs/integrations/tools/duckduckgo_search)
- [LLM Math Chain](https://python.langchain.com/docs/modules/chains/popular/math/)
- [Groq + Qwen3 32B model](https://groq.com/)
- Python 3.10+

---

## 🚀 Project Overview

### 👤 User Input:

> "I want to visit Islamabad with a budget of Rs5000"

### 🧠 How It Works:

This system involves **three main agents** working in a chain:

1. **Destination Expert** 🧭  
   Uses real-time search to suggest tourist destinations based on user's preferences.

2. **Budget Planner** 💰  
   Analyzes if the trip is feasible within the given budget using cost data from the internet and performs calculations.

3. **Itinerary Builder** 📅  
   Creates a detailed, hour-by-hour daily plan for the approved destination and budget.

The **Supervisor Agent** coordinates the workflow between all three.
