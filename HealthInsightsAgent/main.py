# === main.py ===
from typing import TypedDict, Optional
from agents import extract_agent_executor, doctor_agent_executor
from langgraph.graph import MessageGraph, StateGraph

class HealthInsightsState(TypedDict, total=False):
    messages: list
    report_text: Optional[str]
    insights: Optional[str]
    file_path: Optional[str]

def pdf_extractor_node(state):
    file_path = state.get("file_path")
    if not file_path:
        raise ValueError("No file path provided in state.")
    prompt = f"Extract the report from {file_path}"
    result = extract_agent_executor.invoke({"input": prompt})
    return {**state, "report_text": result["output"]}

def doctor_agent_node(state):
    report_text = state.get("report_text")
    if not report_text:
        raise ValueError("Missing report_text in state.")
    prompt = f"What insights can you derive from the following lab report?\n\n{report_text}"
    result = doctor_agent_executor.invoke({"input": prompt})
    return {**state, "insights": result["output"]}

# Define and run the graph
graph = StateGraph(HealthInsightsState)
graph.add_node("pdf_extractor", pdf_extractor_node)
graph.add_node("doctor_agent", doctor_agent_node)

graph.set_entry_point("pdf_extractor")
graph.add_edge("pdf_extractor", "doctor_agent")
graph.set_finish_point("doctor_agent")

app = graph.compile()

if __name__ == "__main__":
    input_state = {
        "file_path": "001000000000084296_001_250571278_C10_117_1.pdf",
        "messages": []
    }
    final_state = app.invoke(input_state)
    print("\n✅ Final Report Analysis:\n")
    print(final_state["insights"])