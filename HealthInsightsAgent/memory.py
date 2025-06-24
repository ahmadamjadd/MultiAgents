from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
from agents import doctor_agent, tools

# Store memory objects per session
session_memory_store = {}

def get_memory_for_session(session_id: str):
    if session_id not in session_memory_store:
        session_memory_store[session_id] = ConversationBufferMemory(return_messages=True)
    return session_memory_store[session_id]

def get_doctor_agent_executor_with_memory(session_id: str):
    memory = get_memory_for_session(session_id)
    return AgentExecutor(
        agent=doctor_agent,
        tools=tools,
        memory=memory,
        verbose=True
    )
